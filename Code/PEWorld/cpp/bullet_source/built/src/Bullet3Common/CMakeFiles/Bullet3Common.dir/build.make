# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/2.8.12/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/2.8.12/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/local/Cellar/cmake/2.8.12/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built

# Include any dependencies generated for this target.
include src/Bullet3Common/CMakeFiles/Bullet3Common.dir/depend.make

# Include the progress variables for this target.
include src/Bullet3Common/CMakeFiles/Bullet3Common.dir/progress.make

# Include the compile flags for this target's objects.
include src/Bullet3Common/CMakeFiles/Bullet3Common.dir/flags.make

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/flags.make
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o: ../src/Bullet3Common/b3AlignedAllocator.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o -c /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3AlignedAllocator.cpp

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.i"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3AlignedAllocator.cpp > CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.i

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.s"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3AlignedAllocator.cpp -o CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.s

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.requires:
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.requires

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.provides: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.requires
	$(MAKE) -f src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build.make src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.provides.build
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.provides

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.provides.build: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/flags.make
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o: ../src/Bullet3Common/b3Vector3.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/Bullet3Common.dir/b3Vector3.o -c /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Vector3.cpp

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Bullet3Common.dir/b3Vector3.i"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Vector3.cpp > CMakeFiles/Bullet3Common.dir/b3Vector3.i

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Bullet3Common.dir/b3Vector3.s"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Vector3.cpp -o CMakeFiles/Bullet3Common.dir/b3Vector3.s

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.requires:
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.requires

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.provides: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.requires
	$(MAKE) -f src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build.make src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.provides.build
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.provides

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.provides.build: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/flags.make
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o: ../src/Bullet3Common/b3Logging.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/Bullet3Common.dir/b3Logging.o -c /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Logging.cpp

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Bullet3Common.dir/b3Logging.i"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Logging.cpp > CMakeFiles/Bullet3Common.dir/b3Logging.i

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Bullet3Common.dir/b3Logging.s"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common/b3Logging.cpp -o CMakeFiles/Bullet3Common.dir/b3Logging.s

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.requires:
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.requires

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.provides: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.requires
	$(MAKE) -f src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build.make src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.provides.build
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.provides

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.provides.build: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o

# Object files for target Bullet3Common
Bullet3Common_OBJECTS = \
"CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o" \
"CMakeFiles/Bullet3Common.dir/b3Vector3.o" \
"CMakeFiles/Bullet3Common.dir/b3Logging.o"

# External object files for target Bullet3Common
Bullet3Common_EXTERNAL_OBJECTS =

src/Bullet3Common/libBullet3Common.2.83.dylib: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o
src/Bullet3Common/libBullet3Common.2.83.dylib: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o
src/Bullet3Common/libBullet3Common.2.83.dylib: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o
src/Bullet3Common/libBullet3Common.2.83.dylib: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build.make
src/Bullet3Common/libBullet3Common.2.83.dylib: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library libBullet3Common.dylib"
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Bullet3Common.dir/link.txt --verbose=$(VERBOSE)
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && $(CMAKE_COMMAND) -E cmake_symlink_library libBullet3Common.2.83.dylib libBullet3Common.2.83.dylib libBullet3Common.dylib

src/Bullet3Common/libBullet3Common.dylib: src/Bullet3Common/libBullet3Common.2.83.dylib

# Rule to build all files generated by this target.
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build: src/Bullet3Common/libBullet3Common.dylib
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/build

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/requires: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3AlignedAllocator.o.requires
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/requires: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Vector3.o.requires
src/Bullet3Common/CMakeFiles/Bullet3Common.dir/requires: src/Bullet3Common/CMakeFiles/Bullet3Common.dir/b3Logging.o.requires
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/requires

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/clean:
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common && $(CMAKE_COMMAND) -P CMakeFiles/Bullet3Common.dir/cmake_clean.cmake
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/clean

src/Bullet3Common/CMakeFiles/Bullet3Common.dir/depend:
	cd /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/src/Bullet3Common /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common /Users/ksmith/Coding/btWorld/Code/btWorld/cpp/bullet_source/built/src/Bullet3Common/CMakeFiles/Bullet3Common.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/Bullet3Common/CMakeFiles/Bullet3Common.dir/depend
