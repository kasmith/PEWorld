cmake_minimum_required (VERSION 2.6)
project (cppTest)

find_package( Bullet REQUIRED)
include_directories(${BULLET_INCLUDE_DIR} )

LINK_LIBRARIES(
BulletDynamics BulletCollision
)

add_executable (test simple.cpp)