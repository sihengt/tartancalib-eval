cd kaess-apriltags
rm -rf build
mkdir build && cd build
cmake .. && make -j8
cd ../../apriltag
rm -rf build
mkdir build && cd build
cmake .. & make -j8
cd ../../deltille
rm -rf build
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_APPS=ON && make -j8

