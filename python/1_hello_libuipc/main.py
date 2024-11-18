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
from pyuipc.unit import MPa, GPa
from asset_dir import AssetDir

Timer.enable_all()
Logger.set_level(Logger.Level.Warn)
engine = Engine('cuda')
world = World(engine)
config = Scene.default_config()
config['dt'] = 0.01
config['gravity'] = [[0.0], [-9.8], [0.0]]
scene = Scene(config)

# create constitution and contact model
abd = AffineBodyConstitution()

# friction ratio and contact resistance
scene.contact_tabular().default_model(0.5, 1.0 * GPa)
default_element = scene.contact_tabular().default_element()

# create a regular tetrahedron
Vs = np.array([[0,1,0],
               [0,0,1],
               [-np.sqrt(3)/2, 0, -0.5],
               [np.sqrt(3)/2, 0, -0.5]])
Ts = np.array([[0,1,2,3]])

# setup a base mesh to reduce the later work
base_mesh = tetmesh(Vs, Ts)
# apply the constitution and contact model to the base mesh
abd.apply_to(base_mesh, 100 * MPa)
# apply the default contact model to the base mesh
default_element.apply_to(base_mesh)

# label the surface, enable the contact
label_surface(base_mesh)
# label the triangle orientation to export the correct surface mesh
label_triangle_orient(base_mesh)

mesh1 = base_mesh.copy()
pos_view = view(mesh1.positions())
# move the mesh up for 1 unit
pos_view += Vector3.UnitY() * 1.5

mesh2 = base_mesh.copy()
is_fixed = mesh2.instances().find(builtin.is_fixed)
is_fixed_view = view(is_fixed)
is_fixed_view[:] = 1

# create objects
object1 = scene.objects().create("upper_tet")
object1.geometries().create(mesh1)

object2 = scene.objects().create("lower_tet")
object2.geometries().create(mesh2)

world.init(scene)
sgui = SceneGUI(scene)

ps.init()
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
        Timer.report()
        sgui.update()

ps.set_user_callback(on_update)
ps.show()