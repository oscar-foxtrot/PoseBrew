import numpy as np
import matplotlib.pyplot as plt
import argparse
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

# Define your skeleton edges (H36M format)
h36m_pts = [(3,2), (2,1), (1, 0), (0, 4), (4, 5), (5, 6), \
    (13, 12), (12, 11), (11, 8), (8, 14), (14, 15), (15, 16), \
    (8, 9), (9, 10), (8, 7), (7, 0)]

parser = argparse.ArgumentParser(description='3D Human Keypoints Animation')
parser.add_argument('--input_file_1', type=str, required=True, help='Input npy file (main)')
parser.add_argument('--input_file_2', type=str, default=None, help='Optional second npy file for comparison')
args = parser.parse_args()

file_name_1 = args.input_file_1
file_name_2 = args.input_file_2

keypoints_3d = np.load(file_name_1, allow_pickle=True)
keypoints_3d = np.asarray(keypoints_3d).astype(float)

if file_name_2:
    keypoints_3d_2 = np.load(file_name_2, allow_pickle=True)
    keypoints_3d_2 = np.asarray(keypoints_3d_2).astype(float)
else:
    keypoints_3d_2 = None

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Z')
ax.set_ylabel('X')
ax.set_zlabel('Y')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

xticks = ax.get_xticks()
xlabels = [f"{-tick:.1f}" for tick in xticks]
ax.set_xticklabels(xlabels)

zticks = ax.get_zticks()
# Create labels as the negative of tick positions, formatted nicely
zlabels = [f"{-tick:.1f}" for tick in zticks]
# Set these labels on the x-axis
ax.set_zticklabels(zlabels)

# Main skeleton
scatter = ax.scatter([], [], [], color='blue')
lines = [ax.plot([], [], [], color='blue')[0] for _ in h36m_pts]

# Second skeleton if provided
if keypoints_3d_2 is not None:
    scatter2 = ax.scatter([], [], [], color='red')
    lines2 = [ax.plot([], [], [], color='red')[0] for _ in h36m_pts]
else:
    scatter2, lines2 = None, []

def update(frame):
    x, y, z = keypoints_3d[frame, :, 0], keypoints_3d[frame, :, 1], keypoints_3d[frame, :, 2]
    scatter._offsets3d = (-z, x, -y)
    for line, (i, j) in zip(lines, h36m_pts):
        line.set_data([-z[i], -z[j]], [x[i], x[j]])
        line.set_3d_properties([-y[i], -y[j]])

    if keypoints_3d_2 is not None:
        x2, y2, z2 = keypoints_3d_2[frame, :, 0], keypoints_3d_2[frame, :, 1], keypoints_3d_2[frame, :, 2]
        scatter2._offsets3d = (-z2, x2, -y2)
        for line, (i, j) in zip(lines2, h36m_pts):
            line.set_data([-z2[i], -z2[j]], [x2[i], x2[j]])
            line.set_3d_properties([-y2[i], -y2[j]])

    return [scatter] + lines + ([scatter2] + lines2 if scatter2 else [])

base_1 = os.path.splitext(os.path.basename(file_name_1))[0]
if file_name_2:
    base_2 = os.path.splitext(os.path.basename(file_name_2))[0]
# Run animation
frame_count = min(len(keypoints_3d), len(keypoints_3d_2)) if keypoints_3d_2 is not None else len(keypoints_3d)
ani = FuncAnimation(fig, update, frames=frame_count, interval=8.33, blit=False)

if file_name_2:
    ani.save(f"animations/{base_1}_{base_2}_aligned_animation.mp4", writer="ffmpeg", fps=30)
else:
    # ani.save(f"animations/{base_1}_monocular_animation.gif", writer="Pillow", fps=30)  # RAM-inefficient version
    ani.save(f"animations/{base_1}_monocular_animation.mp4", writer="ffmpeg", fps=30)