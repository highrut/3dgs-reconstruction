#!/usr/bin/bash

data_dir=$1

pip install setuptools==69.5.1
pip install -e .

echo "Estimate normals"
python dn_splatter/data/download_scripts/download_omnidata.py
python dn_splatter/scripts/normals_from_pretrain.py --data-dir $data_dir --resolution low

echo "Estimate depth maps"
pip install torch==2.0.1 torchvision --index-url https://download.pytorch.org/whl/cu118
python dn_splatter/scripts/align_depth.py \
    --data $data_dir \
    --sparse-path sparse/0 \
    --no-skip-colmap-to-depths --no-skip-mono-depth-creation
pip install torch==2.1.2 torchvision --index-url https://download.pytorch.org/whl/cu118

echo "Train dn-splatter model"
ns-train dn-splatter \
    --pipeline.model.use-depth-loss True \
    --pipeline.model.depth-loss-type PearsonDepth \
    --pipeline.model.depth-lambda 0.2 \
    --pipeline.model.use-normal-loss True \
    --pipeline.model.use-normal-tv-loss True \
    --pipeline.model.normal-supervision mono \
    --pipeline.datamanager.cache_images cpu \
    coolermap --data $data_dir --colmap_path sparse/0 --normals-from pretrained --load-normals True --masks_path masks
