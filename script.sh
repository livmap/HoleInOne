#!bin/bash

SOURCE_FILE="./src/main.cpp"

echo "Compiling $SOURCE_FILE..."
clang++ $SOURCE_FILE -F/Library/Frameworks -framework SDL2 -framework SDL2_image -I/Library/Frameworks/SDL2.framework/Headers -I/Library/Frameworks/SDL2_image.framework/Headers
export DYLD_FRAMEWORK_PATH=/Library/Frameworks
./a.out
