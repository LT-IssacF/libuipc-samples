import numpy as np
import polyscope as ps
from polyscope import imgui


from uipc import view
from uipc import Logger, Timer
from uipc import Vector3, Vector2, Transform, Quaternion, AngleAxis
from uipc import builtin
from uipc.core import *
from uipc.geometry import *
from uipc.constitution import *
from uipc.gui import *

from asset_dir import AssetDir

Timer.enable_all()
Logger.set_level(Logger.Level.Info)

workspace = AssetDir.output_path(__file__)
this_folder = AssetDir.folder(__file__)

engine = Engine('cuda', workspace)
world = World(engine)

config = Scene.default_config()
config['dt'] = 0.01
config['contact']['d_hat'] = 0.01
print(config)
scene = Scene(config)

# begin setup the scene


# end setup the scene

world.init(scene)

ps.init()
ps.set_ground_plane_height(0.0)
sgui = SceneGUI(scene)
tri_surf, lines, points = sgui.register()
tri_surf.set_edge_width(1)

run = False
def on_update():
    global run
    if(imgui.Button('run & stop')):
        run = not run
        
    if(run):
        world.advance()
        world.retrieve()
        sgui.update()

ps.set_user_callback(on_update)
ps.show()