from pyuipc_loader import pyuipc
from asset_dir import AssetDir


if __name__ == '__main__':
    print(f'pyuipc version: {pyuipc.__version__}')
    print(f'asset_path: {AssetDir.asset_path()}')
    print(f'tetmesh_path: {AssetDir.tetmesh_path()}')
    print(f'trimesh_path: {AssetDir.trimesh_path()}')
    print(f'this file output: {AssetDir.output_path(__file__)}')

