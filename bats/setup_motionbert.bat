
REM Step 1: Create environment if not exists
call conda create -n motionbert_env python=3.7 anaconda -y

REM Step 2: Activate environment
call conda activate motionbert_env

git clone https://github.com/Walter0807/MotionBERT
cd MotionBERT

REM Step 3: Install PyTorch (CUDA 11.6 here, adjust if needed)
call conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

REM Step 4: Install Python requirements
call pip install -r requirements.txt

REM Step 5: Download the checkpoint
mkdir checkpoint
cd checkpoint
mkdir pose3d
cd pose3d
mkdir FT_MB_lite_MB_ft_h36m_global_lite
cd FT_MB_lite_MB_ft_h36m_global_lite
call pip install gdown
call gdown "https://drive.google.com/uc?id=1-Yataun9kSdSW6jkBeBom1nMaGs6rScn"
cd ../../..

REM Step 6: Copy modified files into MotionBERT source folder
move "..\custom_motionbert_files" "."
copy /Y "custom_motionbert_files\infer_wild.py" "infer_wild.py"
copy /Y "custom_motionbert_files\infer_wild_mesh.py" "infer_wild_mesh.py"
copy /Y "custom_motionbert_files\dataset_wild.py" "lib/data/dataset_wild.py"
copy /Y "custom_motionbert_files\utils_data.py" "lib/utils/utils_data.py"

cd ..

call bats/install_ffmpeg.bat

REM Deactivate
call conda deactivate

echo MotionBERT (3/3) setup completed.