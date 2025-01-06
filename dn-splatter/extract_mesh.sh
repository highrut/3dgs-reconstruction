#!/usr/bin/bash

declare -A mesh_names
mesh_names["gaussians"]="GaussiansToPoisson_poisson_mesh"
mesh_names["dn"]="DepthAndNormalMapsPoisson_poisson_mesh"
mesh_names["sugar-coarse"]="smoothed_2_poisson_mesh_surface_level_0.3_closest_gaussian"
mesh_names["o3dtsdf"]="Open3dTSDFfusion_mesh"
#mesh_names["marching"]="marching_cubes_512"

data_dir=$1
config_file=$2

gs_name="masked_dn"
use_masks=True

#gs_name="dn"
#use_masks=False

poisson_depth=10
#poisson_depth=12

meshes_dir="mesh_exports"
mkdir -p $meshes_dir
echo "Saving mesh exports to '$meshes_dir'"

results_dir="final_results"
mkdir -p $results_dir
echo "Saving final meshes to '$results_dir'"


for method in "${!mesh_names[@]}"; do
    echo "method: $method"

    mesh_name=${mesh_names[$method]}
    echo "mesh: $mesh_name"

    output_name=${gs_name}_${method}_p${poisson_depth}
    echo "save as: $output_name"

    if [ $method == "o3dtsdf" ]; then
        gs-mesh $method --load-config $config_file --output-dir $meshes_dir/$output_name
    elif [ $method == "marching" ]; then
        gs-mesh $method --load-config $config_file --output-dir $meshes_dir/$output_name
    else
        gs-mesh $method --load-config $config_file --output-dir $meshes_dir/$output_name \
            --poisson_depth $poisson_depth --use_masks $use_masks
    fi

    python ../evaluate.py \
        --gt-file $data_dir/gt_mesh.ply \
        --reconstructed-file $meshes_dir/$output_name/$mesh_name.ply \
        --output-dir $results_dir/$output_name \
        --coords colmap
done
