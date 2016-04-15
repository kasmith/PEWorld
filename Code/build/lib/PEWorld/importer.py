'''

Function for importing Blender worlds

'''

from .world import PEWorld
import os, json

def importWorld(worlddata,fps = 50.,stepsize = 0.001,gravity = 9.81, ERP = 0.2, CFM = 1e-5):
    if not os.path.exists(worlddata):
        raise IOError("World data file " + worlddata + " does not exist")

    pth, flnm = os.path.split(os.path.realpath(worlddata))
    flbase = flnm.rsplit('.',1)[0].rsplit('_',1)[0]
    stldir = os.path.join(pth,flbase+'_meshes')

    jsonfl = open(worlddata,'rU')
    jdat = json.load(jsonfl)
    jsonfl.close()

    W = PEWorld(fps,stepsize,gravity, ERP, CFM)

    for k in jdat.keys():
        j = jdat[k]
        if j['isplane']:
            # NEED TO ADD LOGIC FOR CORRECT PLACEMENT & LOCATION
            W.addPlane(j['name'],friction=j['friction'],restitution=j['restitution'])
        else:
            stlfl = os.path.join(stldir,j['name']+'.stl')
            if not os.path.exists(stlfl):
                raise IOError("Object stl file " + j['name'] + '.stl does not exist in the stl directory')

            if j['rbtype'] == 'PASSIVE': mass = 0
            else: mass = j['mass']
            W.loadMeshFromFile(stlfl,j['name'],j['position'],initquat=j['quaternion'],mass=mass, \
                               friction=j['friction'],restitution=j['restitution'])
    return W