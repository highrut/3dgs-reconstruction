#!/usr/bin/bash

name=$1

data_dir=../data/$name/
model_path=output/vanilla/$name/

python gaussian_splatting/convert.py \
    --source_path $data_dir \
    --no_gpu

python gaussian_splatting/train.py \
    --source_path $data_dir \
    --model_path $model_path \
    --iterations 7_000

python train.py \
    -s $data_dir \
    -c $model_path \
    -r dn_consistency \
    --headless True \
    --high_poly True
