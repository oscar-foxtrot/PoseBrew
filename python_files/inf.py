
import argparse
from mmpose.apis import MMPoseInferencer

def main():
    parser = argparse.ArgumentParser(description='Run 3D pose inference with MMPose')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input video file path')
    parser.add_argument('--out_dir', '-o', type=str, default=None, help='Output directory')
    parser.add_argument('--show', action='store_true', help='Show visualizations during inference')
    args = parser.parse_args()

    inferencer = MMPoseInferencer(
        pose2d='rtmpose-l_8xb512-700e_body8-halpe26-384x288'
    )

    result_generator = inferencer(
        inputs=args.input,
        show=args.show,
        out_dir=args.out_dir if args.out_dir else 'default_mmpose_output',
        return_vis=True,
        save_pred=True
    )

    while True:
        try:
            result = next(result_generator)
            print(f"Processed frame {result['frame_id']}")
        except StopIteration:
            print("No more results.")
            break

if __name__ == '__main__':
    main()
