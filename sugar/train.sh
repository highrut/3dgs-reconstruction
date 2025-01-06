#!/usr/bin/bash

data_dir=$1
name=$(basename -- $data_dir)
model_path=./output/vanilla/$name/

echo "Backup original images before processing..."
cp -r $data_dir/input $data_dir/input_hd

echo "Resize images to max 1600 px..."
mogrify -resize 1600x1600 $data_dir/input/*.JPG

echo "Run COLMAP..."
python gaussian_splatting/convert.py --source_path $data_dir --no_gpu

echo "Run vanilla GS..."
python gaussian_splatting/train.py \
    --source_path $data_dir \
    --model_path $model_path \
    --iterations 7_000

echo "Run SuGaR..."
python train.py \
    --scene_path $data_dir \
    --checkpoint_path $model_path \
    --regularization dn_consistency \
    --high_poly True \
    --refinement_time long
