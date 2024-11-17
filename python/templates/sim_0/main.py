import numpy as np
import polyscope as ps
from polyscope import imgui

from pyuipc_loader import pyuipc
from pyuipc import view
from pyuipc import Logger, Timer
from pyuipc import Vector3, Vector2, Transform, Quaternion, AngleAxis
from pyuipc import builtin
from pyuipc.core import *
from pyuipc.geometry import *
from pyuipc.constitution import *
from pyuipc_utils.gui import *

from asset_dir import AssetDir

if __name__ == '__main__':
    Timer.enable_all()
    Logger.set_level(Logger.Level.Info)
    
    workspace = AssetDir.output_path(__file__)
    this_folder = AssetDir.folder(__file__)

    engine = Engine('cuda', workspace)
    world = World(engine)

    config = Scene.default_config()
    config['dt'] = 0.01
    config['contact']['d_hat']              = 0.01
    print(config)
    
    scene = Scene(config)
