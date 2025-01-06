# High-fidelity 3D mesh reconstruction using Gaussian Splatting (GS): Research and Evaluation

This repo contains utility and visualization scripts related to the mesh reconstruction based on Gaussian splatting.

![image](https://github.com/user-attachments/assets/032238cc-0e75-4464-a49f-9485bbdb1484)


## Methods

### SuGaR

For [SuGaR](https://github.com/Anttwo/SuGaR), there is a bash script for [training a Gaussian splatting model](https://github.com/highrut/3dgs-reconstruction/blob/main/sugar/train.sh)

Please clone the repository of dn-splatter, and follow the installation instructions. 
The training script should be placed in the root directory of SuGaR.

Under [notebooks](https://github.com/highrut/3dgs-reconstruction/blob/main/notebooks), you can find a Jupyter notebook for [SuGaR visualization and evaluation](https://github.com/highrut/3dgs-reconstruction/blob/main/notebooks/view_sugar_results.ipynb).


### dn-splatter

For [dn-splatter](https://github.com/maturk/dn-splatter/), there are bash scripts for [training a Gaussian splatting model](https://github.com/highrut/3dgs-reconstruction/blob/main/dn-splatter/train.sh) and [mesh extraction & evaluation](https://github.com/highrut/3dgs-reconstruction/blob/main/dn-splatter/extract_mesh.sh).

Please clone the repository of dn-splatter, and follow the installation instructions. 
The scripts should be placed under the root directory of dn-splatter.

I would recommend applying a [patch](https://github.com/highrut/3dgs-reconstruction/blob/main/dn-splatter.patch) to avoid segfault when extracting mesh using ```gaussians``` method.


## Evaluation

A [Python evaluation script](https://github.com/highrut/3dgs-reconstruction/blob/main/evaluate.py) can be used to calculate two variants of Normalized Chamfer distance between a ground truth and reconstructed mesh.

It should be placed in the parent directory of dn-splatter and SuGaR.

## Misc

### SAM2

Under [notebooks](https://github.com/highrut/3dgs-reconstruction/blob/main/notebooks), you can find a Jupyter notebook for
[object mask prediction using SAM2](https://github.com/highrut/3dgs-reconstruction/blob/main/notebooks/video_predictor_example.ipynb).
