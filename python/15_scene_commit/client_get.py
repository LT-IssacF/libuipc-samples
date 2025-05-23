import numpy as np
import polyscope as ps
from polyscope import imgui

from uipc import view
from uipc import Logger, Timer, Animation
from uipc import Vector3, Transform, Quaternion, AngleAxis
from uipc import builtin
from uipc.core import Engine, World, Scene, SceneIO, SceneSnapshot, Object
from uipc.geometry import GeometrySlot, SimplicialComplex, SimplicialComplexIO, label_surface, label_triangle_orient, flip_inward_triangles, ground
from uipc.constitution import AffineBodyConstitution, StableNeoHookean
from uipc.gui import SceneGUI
from uipc.unit import MPa, GPa
from asset_dir import AssetDir
import pathlib as pl

Logger.set_level(Logger.Level.Warn)

this_folder = AssetDir.folder(__file__)
output_path = AssetDir.output_path(this_folder)

# --------------------------------------------------------
# load from bson (binary json)
scene = SceneIO.load(f'{output_path}/scene/scene0.bson')
# OR use:
# SceneIO.from_json(...)
# to load the scene from a json
# --------------------------------------------------------

scene_io = SceneIO(scene)
sgui = SceneGUI(scene)

ground_objs:list[Object] = scene.objects().find('ground')
ground_obj = ground_objs[0]
ids = ground_obj.geometries().ids()
geo_slot, rest_geo_slot = scene.geometries().find(ids[0])
P = geo_slot.geometry().instances().find("P")
y = P.view()[0][1]

ps.init()
ps.set_ground_plane_height(y)
tri_surf, _, _ = sgui.register()
tri_surf.set_edge_width(1)

run = False
frame = 1
def on_update():
    global run
    global frame
    
    path = f'{output_path}/scene/scene{frame}.bson'
    
    if(imgui.Button('run & stop')):
        run = not run
    
    if(not pl.Path(path).exists()):
        run = False

    if(run):
        print(f'load update from {path}')
        
        # -----------------------------------------
        # update from the scene commit files
        scene_io.update(path)
        # OR use:
        # scene_io.update_from_json(...)
        # -----------------------------------------
        
        sgui.update()
        frame += 1

ps.set_user_callback(on_update)
ps.show()