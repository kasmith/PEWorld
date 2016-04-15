#!/bin/sh

#  makeBullet_osx.sh
#  
#
#  Created by Kevin Smith on 4/11/16.
#
#
#  Runs makefiles and installs Bullet
#


cd PEWorld/cpp/bullet_source/built
cmake -DBUILD_SHARED_LIBS=on ../
make
make install
cd ../../../..