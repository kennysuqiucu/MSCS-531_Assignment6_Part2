# MSCS-531 Assignment 6, Part 2

Exploring Thread-Level Parallelism (TLP) in shared-memory multiprocessors using gem5.

A multi-threaded daxpy kernel is run on gem5 23.0 (X86, MinorCPU) with six
FloatSimdFU designs (opLat + issueLat = 7) and 1, 2, 4 and 8 threads.

## Files

| File | Purpose |
|---|---|
| `daxpy_mt.c` | Multi-threaded daxpy kernel (POSIX threads) with m5 region-of-interest markers |
| `run_all.sh` | Runs all 24 simulations (6 designs x 4 thread counts) with gem5's standard `se.py`, setting opLat and issueLat through the `-P` option |
| `summarize.py` | Prints time, speedup, IPC, CPI and FloatSimdFU utilization for every run |

## How to run

```bash
# 1. Build the m5 library and compile daxpy as a static x86 binary
cd ~/gem5/util/m5
scons x86.CROSS_COMPILE=x86_64-linux-gnu- build/x86/out/libm5.a
cd -
x86_64-linux-gnu-gcc -O2 -fno-tree-vectorize -static -pthread \
    -I ~/gem5/include -o daxpy_mt daxpy_mt.c \
    ~/gem5/util/m5/build/x86/out/libm5.a

# 2. Run everything and summarize
chmod +x run_all.sh
./run_all.sh
python3 summarize.py
```
