import json
import numpy as np
import polyscope as ps
from polyscope import imgui

import uipc 
from uipc import view
from uipc import Vector3, Vector2, Transform, Logger, Quaternion, AngleAxis, Timer
from uipc import builtin
from uipc.core import Engine, World, Scene, SceneIO, Object
from uipc.gui import SceneGUI

from asset_dir import AssetDir

workspace = AssetDir.output_path(__file__)
folder = AssetDir.folder(__file__)
engine = Engine("cuda", workspace=workspace)
world = World(engine)

scene = SceneIO.load(f'{folder}/scene.json')

ground_objs:list[Object] = scene.objects().find('ground')
ground_obj = ground_objs[0]
ids = ground_obj.geometries().ids()
geo_slot, rest_geo_slot = scene.geometries().find(ids[0])
P = geo_slot.geometry().instances().find("P")
y = P.view()[0][1]

world.init(scene)
sgui = SceneGUI(scene)

Logger.set_level(Logger.Level.Warn)

ps.init()
ps.set_ground_plane_height(y)
tri_surf, _, _ = sgui.register()
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

