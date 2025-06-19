import os
import numpy as np
import argparse
from tqdm import tqdm
import imageio
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from lib.utils.tools import *
from lib.utils.learning import *
from lib.utils.utils_data import flip_data
from lib.data.dataset_wild import WildDetDataset
from lib.utils.vismo import render_and_save

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/pose3d/MB_ft_h36m_global_lite.yaml", help="Path to the config file.")
    parser.add_argument('-e', '--evaluate', default='checkpoint/pose3d/FT_MB_lite_MB_ft_h36m_global_lite/best_epoch.bin', type=str, metavar='FILENAME', help='checkpoint to evaluate (file name)')
    parser.add_argument('-j', '--json_path', type=str, help='alphapose detection result json path')
    parser.add_argument('-v', '--vid_path', type=str, help='video path')
    parser.add_argument('-o', '--out_path', type=str, help='output path')
    parser.add_argument('--pixel', action='store_true', help='align with pixel coordinates')
    parser.add_argument('--focus', type=int, default=None, help='target person id')
    parser.add_argument('--clip_len', type=int, default=243, help='clip length for network input')
    opts = parser.parse_args()
    return opts

def main():
    opts = parse_args()
    args = get_config(opts.config)

    model_backbone = load_backbone(args)
    if torch.cuda.is_available():
        model_backbone = nn.DataParallel(model_backbone)
        model_backbone = model_backbone.cuda()

    print('Loading checkpoint', opts.evaluate)
    checkpoint = torch.load(opts.evaluate, map_location=lambda storage, loc: storage)

    ################################

    # Step 2: Modify the state_dict to remove the 'module.' prefix if it exists
    state_dict = checkpoint['model_pos']  # or whichever key corresponds to your model state dict

    # Create a new state dict where 'module.' is removed from keys
    new_state_dict = {}
    for k, v in state_dict.items():
        # Remove 'module.' prefix
        if k.startswith('module.'):
            k = k[7:]  # Remove the 'module.' prefix (7 characters)
        new_state_dict[k] = v

    # Step 3: Load the modified state dict into your model
    model_backbone.load_state_dict(new_state_dict)

    # model_pos = model_backbone
    model_pos = model_backbone
    model_pos.eval()
    
    testloader_params = {
        'batch_size': 1,
        'shuffle': False,
        'num_workers': 1,
        'pin_memory': True,
        'prefetch_factor': 4,
        'persistent_workers': True,
        'drop_last': False
    }

    vid = imageio.get_reader(opts.vid_path,  'ffmpeg')
    fps_in = vid.get_meta_data()['fps']
    vid_size = vid.get_meta_data()['size']

    os.makedirs(opts.out_path, exist_ok=True)

    if opts.pixel:
        # Keep relative scale with pixel coordinates
        wild_dataset = WildDetDataset(opts.json_path, clip_len=opts.clip_len, vid_size=vid_size, scale_range=None, focus=opts.focus)
    else:
        # Scale to [-1,1]
        wild_dataset = WildDetDataset(opts.json_path, clip_len=opts.clip_len, vid_size=vid_size, scale_range=[1,1], focus=opts.focus)

    test_loader = DataLoader(wild_dataset, **testloader_params)

    results_all = []
    with torch.no_grad():
        for batch in tqdm(test_loader):
            batch_input, batch_centers, batch_scales = batch
            N, T = batch_input.shape[:2]
            if torch.cuda.is_available():
                batch_input = batch_input.cuda()
            if args.no_conf:
                batch_input = batch_input[:, :, :, :2]
            if args.flip:    
                batch_input_flip = flip_data(batch_input)
                predicted_3d_pos_1 = model_pos(batch_input)
                predicted_3d_pos_flip = model_pos(batch_input_flip)
                predicted_3d_pos_2 = flip_data(predicted_3d_pos_flip)  # Flip back
                predicted_3d_pos = (predicted_3d_pos_1 + predicted_3d_pos_2) / 2.0
            else:
                predicted_3d_pos = model_pos(batch_input)
            
            centers_ = batch_centers[:, None, None, :]  # (N,1,1,2)
            scales_ = batch_scales[:, None, None, None]  # (N,1,1,1)

            # predicted_3d_pos[..., :2] is in normalized [-1,1]
            predicted_3d_pos[..., :3] = (predicted_3d_pos[..., :3] / 2 + 0.5) * scales_ #+ centers_
            
            '''
            if args.rootrel:
                predicted_3d_pos[:,:,0,:] = 0  # [N,T,17,3]
            else:
                predicted_3d_pos[:,0,0,2] = 0

            '''

            if args.gt_2d:
                predicted_3d_pos[...,:2] = batch_input[...,:2]
            results_all.append(predicted_3d_pos.cpu().numpy())

    results_all = np.hstack(results_all)
    results_all = np.concatenate(results_all)
    render_and_save(results_all, '%s/X3D.mp4' % (opts.out_path), keep_imgs=False, fps=fps_in)
    if opts.pixel:
        # Convert to pixel coordinates
        results_all = results_all * (min(vid_size) / 2.0)
        results_all[:,:,:2] = results_all[:,:,:2] + np.array(vid_size) / 2.0
    np.save('%s/X3D.npy' % (opts.out_path), results_all)

if __name__ == '__main__':
    main()