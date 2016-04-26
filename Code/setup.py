#!/usr/bin/env python
import distutils
from distutils.core import setup, Extension
import os

try:
    import ode
except:
    raise ImportError('Cannot open PyODE - may need to be installed with pip')

try:
    import OpenGL
except:
    raise ImportError('Cannot open OpenGL - may need to be installed with pip')

try:
    import trimesh
except:
    raise ImportError('Cannot open trimesh - may need to be installed with pip')

try:
    import scipy
except:
    raise ImportError('Cannot open scipy - may need to be installed with pip')

try:
    import dill
except:
    raise ImportError('Cannot open dill - may need to be installed with pip')

setup(name = 'PEWorld',
      version = '0.11',
      description = 'Simple noisy rigid body world for simulation & visualization',
      author = 'Kevin A Smith',
      author_email = 'k2smith@mit.edu',
      url = 'https://github.com/kasmith/PEWorld',
      packages = ['PEWorld','PEWorld.utils','PEWorld.objects','PEWorld.viewer'],
      requires = ['numpy','scipy','dill','ode','OpenGL','trimesh']
      )