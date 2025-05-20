# LWPC v2.1

SPAWAR LWPC (Longwave Propagation Code) v2.1 has been
[described](http://www.spawar.navy.mil/sti/publications/pubs/td/3030/td3030.pdf),
[validated](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2010JA016248),
and
[used](https://journals.ametsoc.org/doi/full/10.1175/JTECH-D-11-00174.1)
by numerous researchers.

This repository provides a modern CMake-based build of the original Fortran code, along with a minimal Python interface. The Fortran source has been modified slightly to compile with modern compilers like `gfortran`.

## Build Instructions (Ubuntu/Linux)

Install required tools:

```bash
sudo apt update
sudo apt install cmake gfortran make build-essential
```

Configure and build the project:

```bash
cmake -B build
cmake --build build
```

This compiles all Fortran binaries and places them in the `build/` directory.

## Important: Path Handling

The original Fortran source contains hardcoded path expectations, notably to `LWPCv21/data/`. On case-sensitive filesystems (like Ubuntu), the code internally converts paths to lowercase.

To work around this, you must create a lowercase symlink to the `LWPCv21` folder:

```bash
ln -s LWPCv21 lwpcv21
```

Place this symlink in the **project root** (same level as `build/`). This ensures that runtime references like `lwpcv21/data/xmtr.lis` are resolved correctly.

## Run the Code

Change into the build directory and run the programs using relative paths to the input files:

```bash
cd build
./lwpc.bin ../LWPCv21/lwpm
```

Output will be written to the location specified in the input files (e.g., `.lwf` files).

## Example Input Files

You can try running the following examples:

```bash
./lwpc.bin ../LWPCv21/gcpath
./lwpc.bin ../LWPCv21/jammer
./lwpc.bin ../LWPCv21/bearings
./lwpc.bin ../LWPCv21/lwflds
```

Make sure that `LWPCv21/data/` contains all necessary `.lis` and `.fmt` data files.

## Viewing Output

To scan and print simulation results:

```bash
./scan ../LWPCv21/output/lwpc.lwf
```

This will generate a `scan.log` text file with readable output from the simulation.

## Notes

* If you encounter runtime errors such as `I/O error 2 occurred trying to open file`, ensure you're launching the binary from the correct directory and that the symlink `lwpcv21/` exists.
* You may need to set `LD_LIBRARY_PATH` if `liblwpc.so` is not found:

```bash
export LD_LIBRARY_PATH=$PWD/LWPCv21/lib:$LD_LIBRARY_PATH
```

## Troubleshooting

* Ensure your working directory matches the structure expected by the hardcoded Fortran paths.
* Verify that `lwpcDAT.loc` points to the correct data path.
* Use `make VERBOSE=1` or `cmake --build build --verbose` to debug build issues.
