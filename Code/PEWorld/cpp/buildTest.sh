#!/bin/sh

#  buildTest.sh
#  
#
#  Created by Kevin Smith on 4/11/16.
#

gcc -c test.cpp cpp_PEObj.cpp
gcc test.o -o test -I PEObj.o bullet/BulletCollision/libBulletCollision.a bullet/BulletDynamics/libBulletDynamics.a