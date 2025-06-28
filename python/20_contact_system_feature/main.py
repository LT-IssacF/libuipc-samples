import numpy as np
import polyscope as ps
from polyscope import imgui

from uipc import view
from uipc import Logger, Timer, Animation
from uipc import Vector3, Transform, Quaternion, AngleAxis
from uipc import builtin
from uipc.core import Engine, World, Scene, ContactSystemFeature
from uipc.geometry import (GeometrySlot, SimplicialComplex, SimplicialComplexIO, Geometry,
                            label_surface, label_triangle_orient, flip_inward_triangles, ground)
from uipc.constitution import AffineBodyConstitution, StableNeoHookean
from uipc.gui import SceneGUI
from uipc.unit import MPa, GPa
from asset_dir import AssetDir

Logger.set_level(Logger.Level.Warn)

workspace = AssetDir.output_path(__file__)
engine = Engine('cuda', workspace)
world = World(engine)

config = Scene.default_config()
dt = 0.02
config['dt'] = dt
config['gravity'] = [[0.0], [-9.8], [0.0]]
config['contact']['friction']['enable'] = True
scene = Scene(config)

# friction ratio and contact resistance
scene.contact_tabular().default_model(0.5, 1.0 * GPa)
default_element = scene.contact_tabular().default_element()

# create constitution and contact model
abd = AffineBodyConstitution()
snk = StableNeoHookean()

# load cube mesh
io = SimplicialComplexIO()
cube_mesh = io.read(f'{AssetDir.tetmesh_path()}/cube.msh')
# label the surface, enable the contact
label_surface(cube_mesh)
# label the triangle orientation to export the correct surface mesh
label_triangle_orient(cube_mesh)
cube_mesh = flip_inward_triangles(cube_mesh)

geo_slot_list:list[GeometrySlot] = []

# ABD
abd_cube_obj = scene.objects().create('abd')
abd_mesh = cube_mesh.copy()
abd.apply_to(abd_mesh, 10.0 * MPa)
t = Transform.Identity()
t.translate(Vector3.UnitY() * 1.1)
view(abd_mesh.transforms())[:] = t.matrix()
abd_geo_slot, abd_rest_geo_slot = abd_cube_obj.geometries().create(abd_mesh)
geo_slot_list.append(abd_geo_slot)

# FEM
fem_cube_obj = scene.objects().create('fem')
fem_mesh = cube_mesh.copy()
snk.apply_to(fem_mesh)
velocity = fem_mesh.vertices().find(builtin.velocity)
fem_geo_slot, fem_rest_geo_slot = fem_cube_obj.geometries().create(fem_mesh)
geo_slot_list.append(fem_geo_slot)

ground_height = -1.5
ground_obj = scene.objects().create('ground')
g = ground(ground_height)
g_geo_slot, g_rest_geo_slot = ground_obj.geometries().create(g)
geo_slot_list.append(g_geo_slot)

world.init(scene)
csf:ContactSystemFeature = world.features().find(ContactSystemFeature)

sgui = SceneGUI(scene, 'split')

ps.init()
sgui.register()
sgui.set_edge_width(1)

# contact primitives geometry
ph_geo = Geometry() # point halfplane
pp_geo = Geometry() # point-point
pe_geo = Geometry() # point-edge
pt_geo = Geometry() # point-triangle
ee_geo = Geometry() # edge-edge

# contact gradient and hessian
cg_geo = Geometry()
ch_geo = Geometry()

run = False
def on_update():
    global run
    global geo_slot_list
    global ph_geo

    if(imgui.Button('run & stop')):
        run = not run
    
    for geo_slot in geo_slot_list:
        geo = geo_slot.geometry()
        gvo = geo.meta().find(builtin.global_vertex_offset)
        if gvo is not None:
            imgui.Text(f'[{geo_slot.id()}] Global Vertex Offset: {gvo.view()}')
        else:
            imgui.Text(f'[{geo_slot.id()}] This version dont support global vertex offset!')
    
    types = csf.contact_primitive_types()
    imgui.Text(f'Contact Primitive Types: {types}')
    
    csf.contact_primitives('PH', ph_geo)
    PH = ph_geo.instances().find('topo')
    imgui.Text(f'[PH] Contact Primitives: {PH.view().reshape(-1,2)}')

    csf.contact_primitives('PP', pp_geo)
    PP = pp_geo.instances().find('topo')
    imgui.Text(f'[PP] Contact Primitives: {PP.view().reshape(-1,2)}')

    csf.contact_primitives('PE', pe_geo)
    PE = pe_geo.instances().find('topo')
    imgui.Text(f'[PE] Contact Primitives: {PE.view().reshape(-1,3)}')

    csf.contact_primitives('PT', pt_geo)
    PT = pt_geo.instances().find('topo')
    imgui.Text(f'[PT] Contact Primitives: {PT.view().reshape(-1,4)}')

    csf.contact_primitives('EE', ee_geo)
    EE = ee_geo.instances().find('topo')
    imgui.Text(f'[EE] Contact Primitives: {EE.view().reshape(-1,4)}')

    csf.contact_gradient(cg_geo)
    gi = cg_geo.instances().find('i')
    grad = cg_geo.instances().find('grad')
    imgui.Text(f'[CG] Contact Gradient:{gi.view()} {grad.view().reshape(-1,3)}')

    csf.contact_hessian(ch_geo)
    hi = ch_geo.instances().find('i')
    hj = ch_geo.instances().find('j')
    hess = ch_geo.instances().find('hess')
    imgui.Text(f'[CH] Contact Hessian: {hi.view()} {hj.view()} {hess.view()}')

    if(run):
        world.advance()
        world.retrieve()
        sgui.update()

ps.set_user_callback(on_update)
ps.show()