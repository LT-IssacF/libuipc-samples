import numpy as np
import polyscope as ps
from polyscope import imgui

from uipc import view
from uipc import Vector3, Vector2, Transform, Logger, Quaternion, AngleAxis
from uipc import builtin
from uipc.core import Engine, World, Scene, ContactElement
from uipc.geometry import GeometrySlot, SimplicialComplex, SimplicialComplexIO, ground, label_surface, label_triangle_orient, flip_inward_triangles
from uipc.constitution import AffineBodyConstitution
from uipc.gui import SceneGUI

from asset_dir import AssetDir

Logger.set_level(Logger.Level.Warn)
workspace = AssetDir.output_path(__file__)
folder = AssetDir.folder(__file__)

engine = Engine("cuda", workspace)
world = World(engine)

config = Scene.default_config()
config["dt"] = 0.01
config["contact"]["d_hat"] = 0.01
print(config)

scene = Scene(config)
abd = AffineBodyConstitution()
scene.constitution_tabular().insert(abd)
contact_tabular = scene.contact_tabular()
contact_tabular.default_model(0.5, 1e9)
default_element = scene.contact_tabular().default_element()

io = SimplicialComplexIO()
N = 8
friction_rate_step = 1.0 / (N - 1)
contact_elements:list[ContactElement] = []

for i in range(N):
    friction_rate = i * friction_rate_step
    e = contact_tabular.create(f'element_{i}')
    contact_tabular.insert(e, default_element, 
                           friction_rate=friction_rate,
                           resistance=1e9)
    contact_elements.append(e)


pre_transform = Transform.Identity()
pre_transform.scale(0.3)
io = SimplicialComplexIO(pre_transform)
cube_mesh = io.read(f'{AssetDir.trimesh_path()}/cube.obj')
label_surface(cube_mesh)

abd.apply_to(cube_mesh, 1e8)
step = 0.5
start_x = - step * (N - 1) / 2

# create cubes
cube_obejct = scene.objects().create("cubes")
for i in range(N):
    cube = cube_mesh.copy()
    contact_elements[i].apply_to(cube)
    t = Transform.Identity()
    t.translate(Vector3.Values([start_x + i * step, 1, -0.7]))
    t.rotate(AngleAxis(30 * np.pi / 180, Vector3.UnitX()))
    view(cube.transforms())[0] = t.matrix()
    cube_obejct.geometries().create(cube)

# create ramp
ramp_object = scene.objects().create("ramp")
pre_transform = Transform.Identity()
pre_transform.scale(Vector3.Values([0.5 * N, 0.1, 5]))
io = SimplicialComplexIO(pre_transform)
ramp_mesh = io.read(f'{AssetDir.trimesh_path()}/cube.obj')
label_surface(ramp_mesh)
default_element.apply_to(ramp_mesh)
abd.apply_to(ramp_mesh, 1e8)

# rotate by 30 degrees
t = Transform.Identity()
t.rotate(AngleAxis(30 * np.pi / 180, Vector3.UnitX()))
view(ramp_mesh.transforms())[0] = t.matrix()

is_fixed = ramp_mesh.instances().find(builtin.is_fixed)
view(is_fixed).fill(1)
ramp_object.geometries().create(ramp_mesh)
ground_height = -2

g = ground(ground_height)
scene.objects().create("ground").geometries().create(g)

sgui = SceneGUI(scene, 'split')
world.init(scene)

ps.init()
ps.set_ground_plane_height(-2)
sgui.register()
sgui.set_edge_width(1)

run = False
def on_update():
    global run
    if(imgui.Button("run & stop")):
        run = not run
        
    if(run):
        world.advance()
        world.retrieve()
        sgui.update()

ps.set_user_callback(on_update)
ps.show()