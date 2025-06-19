@echo off

call conda create --name boxmot_env python=3.10 -y
call conda activate boxmot_env

call pip install boxmot

call conda deactivate

echo boxmot_env (2/3) setup completed.