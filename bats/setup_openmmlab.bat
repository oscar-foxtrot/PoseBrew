@echo off
REM Initialize and set up MMPose environment on Windows

REM Create and activate conda environment
call conda create --name openmmlab_env python=3.8 -y
call conda activate openmmlab_env

REM Install PyTorch + torchvision for CPU
call conda install pytorch torchvision cpuonly -c pytorch -y

REM Install OpenMMLab dependencies
call pip install -U openmim
call mim install mmengine
call mim install "mmcv==2.1.0"
call mim install "mmdet>=3.1.0"

git clone https://github.com/open-mmlab/mmpose.git

REM Install MMPose
cd mmpose
call pip install -r requirements.txt
call pip install -v -e .

cd ..

REM Deactivate
call conda deactivate

echo MMPose (1/3) setup completed.