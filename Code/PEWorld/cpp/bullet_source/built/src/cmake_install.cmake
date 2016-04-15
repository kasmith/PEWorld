# Install script for directory: /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/bullet" TYPE FILE FILES
    "/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/btBulletCollisionCommon.h"
    "/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/btBulletDynamicsCommon.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3OpenCL/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Serialize/Bullet2FileLoader/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Dynamics/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Collision/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Geometry/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/BulletInverseDynamics/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/BulletSoftBody/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/BulletCollision/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/BulletDynamics/cmake_install.cmake")
  INCLUDE("/Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/LinearMath/cmake_install.cmake")

ENDIF(NOT CMAKE_INSTALL_LOCAL_ONLY)

