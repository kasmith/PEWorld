'''

Helper functions for applying rotations

'''

import numpy as np

def quaternionToRot(quat):
    w,x,y,z = quat
    x2 = x*x
    y2 = y*y
    z2 = z*z
    xy = x*y
    xz = x*z
    yz = y*z
    wx = w*x
    wy = w*y
    wz = w*z
    return np.matrix(((1-2*y2 - 2*z2, 2*xy - 2*wz, 2*xz + 2*wy),
                      (2*xy + 2*wz, 1-2*x2 - 2*z2, 2*yz - 2*wx),
                      (2*xz - 2*wy, 2*yz + 2*wx, 1-2*x2 - 2*y2)))


def quaternionProduct(q1,q2):
    w1,x1,y1,z1 = q1
    x2,x2,y2,z2 = q2
    return np.array((w1*w2 - x1*x2 - y1*y2 - z1*z2,
                     w1*x2 + w2*x1 + y1*z2 - y2*z1,
                     w1*y2 + w2*y1 - x1*z2 + x2*z1,
                     w1*z2 + w2*z1 + x1*y2 - x2*y1))

# Rotates a single point (ignoring rotation
def rotatePointAroundOrigin(normal = (0.,0.,1.), angle = 0., initpos = (0.,0.,0.)):
    normal = np.array(normal)
    normal = normal / np.linalg.norm(normal) # Ensure normal is normalized
    u,v,w = normal
    ca = np.cos(angle)
    sa = np.sin(angle)
    x,y,z = initpos
    iterm = (u*x+v*y+w*z)*(1-ca)
    # Equation from http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
    newpos = np.array((u*iterm+x*ca+(-w*y+v*z)*sa,
                       v*iterm+y*ca+(w*x-u*z)*sa,
                       w*iterm+z*ca+(-v*x+u*y)*sa))
    return newpos

# Returns (newposition, newquaternion) for rotation
def rotateAroundOrigin(normal = (0.,0.,1.), angle = 0., initpos = (0.,0.,0.), initquat = (1.,0.,0.,0.)):
    newpos = rotatePointAroundOrigin(normal,angle,initpos)
    pass # NOT YET DONE WITH THE QUATERNION ROTATION