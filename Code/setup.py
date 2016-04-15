#!/usr/bin/env python
import distutils
from distutils.core import setup, Extension
import os

setup(name = 'PEWorld',
      version = '0.1',
      description = 'Simple noisy rigid body world for simulation & visualization',
      author = 'Kevin A Smith',
      author_email = 'k2smith@mit.edu',
      url = 'https://github.com/kasmith/PEWorld',
      packages = ['PEWorld','PEWorld.utils','PEWorld.objects','PEWorld.viewer'],
      requires = ['numpy','scipy','dill','ode','OpenGL','trimesh']
      )