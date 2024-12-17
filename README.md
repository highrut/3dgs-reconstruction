<div align="center">

# SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Mesh Rendering

<font size="4">
CVPR 2024
</font>
<br>

<font size="4">
<a href="https://anttwo.github.io/" style="font-size:100%;">Antoine Guédon</a>&emsp;
<a href="https://vincentlepetit.github.io/" style="font-size:100%;">Vincent Lepetit</a>&emsp;
</font>
<br>

<font size="4">
LIGM, Ecole des Ponts, Univ Gustave Eiffel, CNRS
</font>
</div>


## Overview

SuGaR optimization starts with first optimizing a 3D Gaussian Splatting model for 7k iterations with no additional regularization term. Consequently, the current implementation contains a version of the original <a href="https://github.com/graphdeco-inria/gaussian-splatting">3D Gaussian Splatting code</a>, and we the model is built as a wrapper of a vanilla 3D Gaussian Splatting model.

The full SuGaR pipeline consists of 4 main steps, and an optional one:
1. **Short vanilla 3DGS optimization**: optimizing a vanilla 3D Gaussian Splatting model for 7k iterations, in order to let Gaussians position themselves in the scene.
2. **SuGaR optimization**: optimizing Gaussians alignment with the surface of the scene.
3. **Mesh extraction**: extracting a mesh from the optimized Gaussians.
4. **SuGaR refinement**: refining the Gaussians and the mesh together to build a hybrid Mesh+Gaussians representation.
5. **Textured mesh extraction (Optional)**: extracting a traditional textured mesh from the refined SuGaR model.

## Installation

### 0. Requirements

The software requirements are the following:
- Conda (recommended for easy setup)
- C++ Compiler for PyTorch extensions
- CUDA toolkit 11.8 for PyTorch extensions
- C++ Compiler and CUDA SDK must be compatible

Please refer to the original <a href="https://github.com/graphdeco-inria/gaussian-splatting">3D Gaussian Splatting repository</a> for more details about requirements.

### 1. Clone the repository

Start by cloning this repository:

```shell
# HTTPS
git clone https://github.com/Anttwo/SuGaR.git --recursive
```

or

```shell
# SSH
git clone git@github.com:Anttwo/SuGaR.git --recursive
```

### 2. Creating the Conda environment

To create and activate the Conda environment with all the required packages, go inside the `SuGaR/` directory and run the following command:

```shell
python install.py
conda activate sugar
```

This script will automatically create a Conda environment named `sugar` and install all the required packages. It will also automatically install the <a href="https://github.com/graphdeco-inria/gaussian-splatting">3D Gaussian Splatting</a> rasterizer as well as the <a href="https://nvlabs.github.io/nvdiffrast/">Nvdiffrast</a> library for faster mesh rasterization.

If you encounter any issues with the installation, you can try to follow the detailed instructions below to install the required packages manually.

<details>
<summary><span style="font-weight: bold;">
Detailed instructions for manual installation
</span></summary>

#### a) Install the required Python packages
To install the required Python packages and activate the environment, go inside the `SuGaR/` directory and run the following commands:

```shell
conda env create -f environment.yml
conda activate sugar
```

If this command fails to create a working environment, you can try to install the required packages manually by running the following commands:
```shell
conda create --name sugar -y python=3.9
conda activate sugar
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.8 -c pytorch -c nvidia
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install pytorch3d==0.7.4 -c pytorch3d
conda install -c plotly plotly
conda install -c conda-forge rich
conda install -c conda-forge plyfile==0.8.1
conda install -c conda-forge jupyterlab
conda install -c conda-forge nodejs
conda install -c conda-forge ipywidgets
pip install open3d
pip install --upgrade PyMCubes
```

#### b) Install the Gaussian Splatting rasterizer

Run the following commands inside the `SuGaR` directory to install the additional Python submodules required for Gaussian Splatting:

```shell
cd gaussian_splatting/submodules/diff-gaussian-rasterization/
pip install -e .
cd ../simple-knn/
pip install -e .
cd ../../../
```
Please refer to the <a href="https://github.com/graphdeco-inria/gaussian-splatting">3D Gaussian Splatting repository</a> for more details.

#### c) (Optional) Install Nvdiffrast for faster Mesh Rasterization

Installing Nvdiffrast is optional but will greatly speed up the textured mesh extraction step, from a few minutes to less than 10 seconds.

```shell
git clone https://github.com/NVlabs/nvdiffrast
cd nvdiffrast
pip install .
cd ../
```

</details>

## Quick Start

Create data folder in the root folder of this repository and move your images to data/SCENE_NAME/input.

Then, run
```shell
python ./run_sh SCENE_NAME
```

The `view_sugar_results.ipynb` notebook provides examples of how to load SuGaR reconstruction, render a scene from Gaussian and mesh representation, and assess the quality of a reconstructed mesh.
