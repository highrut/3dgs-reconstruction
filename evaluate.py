import argparse
import copy
import os

import numpy as np
import open3d as o3d


def extract_point_cloud(mesh):
    pcd = o3d.geometry.PointCloud()
    pcd.points = copy.deepcopy(mesh.vertices)
    pcd.colors = copy.deepcopy(mesh.vertex_colors)
    pcd.normals = copy.deepcopy(mesh.vertex_normals)

    return pcd


def compute_normalized_cd(input1, input2):
    if isinstance(input1, o3d.geometry.TriangleMesh):
        input1 = extract_point_cloud(input1)

    assert isinstance(input1, o3d.geometry.PointCloud), input1

    if isinstance(input2, o3d.geometry.TriangleMesh):
        input2 = extract_point_cloud(input2)

    assert isinstance(input1, o3d.geometry.PointCloud), input2
    
    dists1 = np.array(input1.compute_point_cloud_distance(input2))
    dists2 = np.array(input2.compute_point_cloud_distance(input1))

    ncd = dists1.mean() + dists2.mean()

    return ncd


def preprocess(
        reconstructed_mesh,
        gt_mesh,
        output_dir=None,
        coords="open3d",
        debug=False
    ):
    T = np.array([
        [ 0.99690966, -0.07557869,  0.02126221,  0.17991995],
        [-0.0564357 , -0.50125159,  0.86347171, -0.36422869],
        [-0.0545966 , -0.86199765, -0.50394905, -0.50027813],
        [ 0.        ,  0.        ,  0.        ,  1.        ]
    ])

    if coords == "colmap":
        print("Using COLMAP coordinate system")

        CC = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0],
        ])
        T[:3, :3] = CC @ T[:3, :3]
    else:
        print("Using Open3D coordinate system") 

    print("Transformation matrix:")
    print(T)

    aligned_mesh = copy.deepcopy(reconstructed_mesh).transform(T)

    if output_dir is not None and debug:
        os.makedirs(output_dir, exist_ok=True)
        aligned_mesh_path = os.path.join(output_dir, f"{name}_aligned.ply")
        print("Save full reconstructed and aligned mesh to", aligned_mesh_path)
        o3d.io.write_triangle_mesh(aligned_mesh_path, aligned_mesh)

    # Scale mesh
    scale = 177.1121505336849
    print("Scale coefficient:", scale)
    scaled_mesh = aligned_mesh.scale(scale, np.zeros(3))

    # Crop region of interest
    cropped_mesh = scaled_mesh.crop(gt_mesh.get_axis_aligned_bounding_box())

    return cropped_mesh


def evaluate(
        reconstructed_mesh,
        gt_mesh,
        output_dir=None,
        num_points=100000,
        skip_preprocessing=False,
        coords="open3d",
        debug=False
    ):

    if not skip_preprocessing:
        # Align reconstructed mesh with ground truth
        final_mesh = preprocess(
            reconstructed_mesh=reconstructed_mesh,
            gt_mesh=gt_mesh,
            coords=coords,
            output_dir=output_dir,
            debug=debug
        )
    else:
        final_mesh = reconstructed_mesh

    # Extract point clouds and calculate metrics

    # Vertex-based NCD
    print(
        f"Extracting mesh vertices for "
        "vertex-based Normalized Chamfer distance..."
    )
    gt_pcd = extract_point_cloud(gt_mesh)
    final_pcd = extract_point_cloud(final_mesh)
    print(f"Ground truth: {gt_pcd}, reconstructed: {final_pcd}")

    ncd_v = compute_normalized_cd(gt_pcd, final_pcd)
    print(f"Normalized Chamfer distance (vertex): {ncd_v:.2f} mm")

    # Poisson-based NCD
    print(
        f"Sampling {num_points} points for "
        "Poisson-based Normalized Chamfer distance..."
    )
    gt_pcd = gt_mesh.sample_points_poisson_disk(num_points)
    final_pcd = final_mesh.sample_points_poisson_disk(num_points)
    print(f"Ground truth: {gt_pcd}, reconstructed: {final_pcd}")

    ncd_p = compute_normalized_cd(gt_pcd, final_pcd)
    print(f"Normalized Chamfer distance (poisson): {ncd_p:.2f} mm")

    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)

        name = os.path.basename(output_dir)
        final_mesh_path = os.path.join(
            output_dir, f"{name}_ncdv={ncd_v:.2f}_ncdp={ncd_p:.2f}.ply"
        )
        print("Save final mesh to", final_mesh_path)
        o3d.io.write_triangle_mesh(final_mesh_path, final_mesh)

    results = {"ncd_v": ncd_v, "ncd_p": ncd_p}

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluation of reconstructed meshes"
    )

    parser.add_argument("--gt-file", "-gt", type=str,
                        default="./data/test_data_demogorgon/gt_mesh.ply",
                        help="Path to GT mesh file")
    parser.add_argument("--reconstructed-file", "-r", type=str,
                        help="Path to reconstructed mesh file")
    parser.add_argument("--output-dir", "-o", type=str,
                        help="Path to save processed reconstructed mesh")

    parser.add_argument("--num-points", "-n", type=int, default=100000,
                        help="Number of points to sample from meshes")

    parser.add_argument("--coords", "-c", type=str,
                        default="open3d", choices=["colmap", "open3d"],
                        help="Coordinate system ('open3d' for SuGaR, 'colmap' for nerfstudio)")

    parser.add_argument("--skip-preprocessing", action="store_true",
                        help="Skip preprocessing for aligned, scaled & cropped meshes")
    parser.add_argument("--debug", action="store_true",
                        help="Save intermediate results for debugging")

    args = parser.parse_args()

    gt_mesh = o3d.io.read_triangle_mesh(args.gt_file)
    print("Ground truth", gt_mesh)

    reconstructed_mesh = o3d.io.read_triangle_mesh(args.reconstructed_file)
    print("Reconstructed", reconstructed_mesh)

    evaluate(
        reconstructed_mesh,
        gt_mesh,
        output_dir=args.output_dir,
        num_points=args.num_points,
        coords=args.coords,
        skip_preprocessing=args.skip_preprocessing,
        debug=args.debug
    )

