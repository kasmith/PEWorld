'''

NOTE: This script runs in Python 3.4 - the default Blender python
It should not be run except as a command line script for Blender
  (or imported from other Blender Python scripts)

'''

from mathutils import *
from math import *
import bpy
import json
import os, sys

def SelectObj(obj):
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        raise Exception('Cannot set mode to select')

def SelectObjByName(onm):
    obj = bpy.data.objects[onm]
    SelectObj(obj)

def ExportMesh(objnm, directory, check_existing = False):
    SelectObjByName(objnm)
    filename = os.path.join(bpy.path.abspath("//"),directory,objnm+'.stl')
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.export_mesh.stl(filepath=filename,check_existing=check_existing, \
                                use_scene_unit = True)
        bpy.ops.object.mode_set(mode="OBJECT")

def GetObjProperties(obj):
    props = dict()
    props['name'] = obj.name
    props['position'] = list(obj.location)
    props['quaternion'] = list(obj.rotation_quaternion)
    rbt = obj.rigid_body.type
    props['rbtype'] = rbt
    if rbt:
        props['mass'] = obj.rigid_body.mass
    else:
        props['mass'] = 0.
    props['friction'] = obj.rigid_body.friction
    props['restitution'] = obj.rigid_body.restitution
    props['dimensions'] = list(obj.dimensions)
    props['isplane'] = obj.dimensions[2] == 0.0
    return props

def ExportScene(savename, excludelist = []):
    objdict = dict()
    flnm = os.path.join(bpy.path.abspath("//"),savename + '_data.json')
    dirnm = os.path.join(bpy.path.abspath("//"),savename + '_meshes')
    if not os.path.exists(dirnm):
        os.mkdir(dirnm)
    for o in bpy.data.objects:
        if o.name not in excludelist and o.type == "MESH":
            ps = GetObjProperties(o)
            if not ps['isplane']: ExportMesh(o.name,dirnm)
            objdict[o.name] = ps
    fl = open(flnm,'w')
    fl.write(json.dumps(objdict))
    fl.close()


if __name__ == '__main__':
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    snm = argv[0]
    excls = argv[1:]
    ExportScene(snm,excls)
