import numpy as np
import argparse
import os

# Ensure that the first file in a pair is always a shorter video (without the margins (see lines 32, 35))
# than the second file AND the person in that first video moves TOWARDS the camera

parser = argparse.ArgumentParser(description='Run 3D pose inference with MMPose')
parser.add_argument('--input_1', '-i1', type=str, required=True, help='First npy file')
parser.add_argument('--input_2', '-i2', type=str, default=None, help='Second npy file')
parser.add_argument('--synced', action='store_true', help='Indicates the videos/npy files are already synced')
args = parser.parse_args()

file_1 = args.input_1
file_2 = args.input_2

window_size = 100  # You can change this to any value ≥ 1

def similarity_procrustes(X, Y):
    '''
    Procrustes analysis with scaling to align Y to X.
    Both X and Y are (N, 3) arrays.
    Returns: aligned_Y, rotation_matrix, scale, translation
    '''
    X_mean = X.mean(axis=0)
    Y_mean = Y.mean(axis=0)
    X0 = X - X_mean
    Y0 = Y - Y_mean

    U, _, Vt = np.linalg.svd(Y0.T @ X0)
    R = U @ Vt

    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = U @ Vt

    s = 1  # No scaling, s = norm_X / norm_Y could be added here
    aligned_Y = s * Y0 @ R + X_mean

    return aligned_Y, R, s, X_mean - s * Y_mean @ R

margins = 50

# --- Load keypoints
if args.synced:
    kpts0 = np.load(file_1, allow_pickle=True)[:]
else:
    kpts0 = np.load(file_1, allow_pickle=True)[margins: -margins]
kpts1 = np.load(file_2, allow_pickle=True)[:]
kpts0 = np.array(kpts0, dtype=np.float64)
kpts1 = np.array(kpts1, dtype=np.float64)

diff_len = len(kpts1) - len(kpts0)


if args.synced:
    # skip offset search, files are synced
    i = 0
else:
    # run offset search and alignment
    norms = []
    # --- Try different offsets
    for i in range(diff_len + 1):
        kpts1_new = kpts1[i: len(kpts1) - diff_len + i]
        aligned_acc = np.zeros_like(kpts0)
        counts = np.zeros((len(kpts0), 1, 1))

        for j in range(len(kpts0) - window_size + 1):
            X_win = kpts1_new[j:j + window_size].reshape(-1, 3)
            Y_win = kpts0[j:j + window_size].reshape(-1, 3)

            Y_win_aligned, R, scale, translation = similarity_procrustes(X_win, Y_win)
            Y_win_aligned = Y_win_aligned.reshape(window_size, -1, 3)

            aligned_acc[j:j + window_size] += Y_win_aligned
            counts[j:j + window_size] += 1

        counts[counts == 0] = 1
        new_kpts0 = aligned_acc / counts

        diff = kpts1_new - new_kpts0
        diff = np.array(diff, dtype=np.float64)
        score = np.average(np.linalg.norm(diff, axis=2))
        norms.append(score)

    # --- Find the best offset
    i = np.argmin(norms)
    print("Best alignment offset index:", i)


# --- Final alignment with best offset
kpts1_new = kpts1[i: len(kpts1) - diff_len + i]
aligned_acc = np.zeros_like(kpts0)
counts = np.zeros((len(kpts0), 1, 1))

for j in range(len(kpts0) - window_size + 1):
    X_win = kpts1_new[j:j + window_size].reshape(-1, 3)
    Y_win = kpts0[j:j + window_size].reshape(-1, 3)

    Y_win_aligned, R, scale, translation = similarity_procrustes(X_win, Y_win)
    Y_win_aligned = Y_win_aligned.reshape(window_size, -1, 3)

    aligned_acc[j:j + window_size] += Y_win_aligned
    counts[j:j + window_size] += 1

counts[counts == 0] = 1
kpts0_aligned = aligned_acc / counts

os.makedirs("predictions", exist_ok=True)
base_1 = os.path.splitext(os.path.basename(file_1))[0]
base_2 = os.path.splitext(os.path.basename(file_2))[0]
# --- Save results
np.save(f'predictions/{base_1}_aligned.npy', kpts0_aligned)
np.save(f'predictions/{base_2}_aligned.npy', kpts1_new)
d0 = len(kpts1_new) // 2

k = 0.00
weights = np.array([1 / (1 + np.exp(-k * (d - d0))) for d in range(len(kpts1_new))])
#weights = np.array([(1 / 2) for d in range(len(kpts1_new))])

os.makedirs("predictions", exist_ok=True)

keypoints = np.array([kpts0_aligned[i] * weights[i] + kpts1_new[i] * (1 - weights[i]) for i in range(len(kpts1_new))])
np.save(f'predictions/{base_1}_{base_2}_fused.npy', keypoints)

# Points may be animated next