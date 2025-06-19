# PoseBrew

- English (chosen)  
- [Переключить на русский](README.md)
Вот перевод твоего README на английский, сохранил стиль и форматирование:

## Coursework, MSU Faculty of Computational Mathematics and Cybernetics (2025) <br>

During this work, an end-to-end tool was developed to estimate relative 3D human pose from arbitrary (in-the-wild) .mp4 videos. The theoretical description can be found in the [coursework text]().

#### Technical Requirements

The tool is developed for Windows OS. <br>
Required software: [python](https://www.python.org/downloads/), [git](https://git-scm.com/downloads), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

Tested system configuration:

* OS: Windows 11 x64
* CPU: AMD Ryzen 5 7535HS
* GPU: not used (CPU-only mode for compatibility with systems without CUDA support)
* RAM: 16 GB

### Installation Instructions <br>

Open Anaconda Prompt (or terminal with conda activated).
Then run:

```
git clone https://github.com/oscar-foxtrot/PoseBrew
cd PoseBrew
```

The next command will automatically install dependencies and configure the environment <br>
(estimated time \~20-30 minutes, disk space \~9 GB):

```
setup
```

### Pose Estimation <br>

##### Get animations and 3D points from a single video:

```
infer filename.mp4
```

This generates the following files and folders:

* mmpose\_output\output\_filename (2D keypoints)
* boxmot\_output\filename.mp4 (tracking animation)
* motionbert\_output\filename\_0 (3D points and animations before ensembling, no time shift)
* motionbert\_output\filename\_1 (3D points and animations before ensembling, 1-step time shift)
* motionbert\_output\filename\_2 (3D points and animations before ensembling, 2-step time shift)

Final results:

* animations\filename\_monocular\_animation.mp4 (output 3D keypoints animation)
* predictions\filename.npy (output 3D keypoints)

##### Predictions for multiview configuration:

```
infer file1 file2 [--npy] [--synced]
```

If file1 and file2 are .npy files obtained using **infer file1.mp4** and **infer file2.mp4**, no prediction is performed — only 3D keypoints fusion. In this case, use the flag **--npy**. <br>
If file1 and file2 are .mp4 files, prediction is done on both files first, then fusion. Then omit the **--npy** flag. <br>
If file1 and file2 are synchronized-in-time .mp4 or .npy files, specify the flag **--synced**. Automatic synchronization will not be done then.

This generates the following files and folders:

* predictions\file1\_aligned.npy (3D pose points from file1 aligned to file2)
* predictions\file2\_aligned.npy (3D pose points from file2 aligned to file1)
* predictions\file1\_file2\_fused.npy (3D points fused from poses in files 1 and 2)

##### Animate points:

```
animate file1.npy [file2.npy]
```

This generates:

* animations\file1\_monocular\_animation.npy (3D pose animation for a single file)
* animations\file1\_file2\_aligned\_animation.npy (animation of two poses together if two files provided)

### Example usage:

Put the directory `neurologist` with videos `file_469.mp4` and `file_474.mp4` into PoseBrew. This video pair is recorded in multiview configuration, without synchronization. <br> <br>
Predict pose for the first video:

```
D:\User\PoseBrew> infer neurologist\file_469.mp4
```

Predict pose for the second video:

```
D:\User\PoseBrew> infer neurologist\file_474.mp4
```

Get automatically time-synchronized and spatially best-aligned points:

```
D:\User\PoseBrew> fuse predictions\file_469.npy predictions\file_474.npy --npy
```

Animate the fused result:

```
D:\User\PoseBrew> animate predictions\file_469_aligned.npy predictions\file_474_aligned.npy
```

Result: the resulting animation (`file_469_aligned_file_474_aligned_aligned_animation.mp4`):
![Result](https://raw.githubusercontent.com/oscar-foxtrot/pose3d-coursework/main/assets/file_469_aligned_file_474_aligned_aligned_animation.gif)

### Dataset:

The dataset (11 videos) used in this work can be found [here](https://drive.google.com/drive/u/4/folders/1r1LvgzcUSsAGHxaXMExGOCglrXlOL6oI).

### Results:

Results of processing all 11 videos (including all intermediate steps) can be found [here](https://drive.google.com/drive/folders/1DfhZYNLys-Ts5_5sNaspMypEJd_I7sgN?usp=drive_link).

---

Если нужно, могу помочь и с формулировками, или адаптировать под более формальный стиль.
