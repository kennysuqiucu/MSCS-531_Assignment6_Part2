#!/bin/bash
# run_all.sh - run each FloatSimdFU design (opLat + issueLat = 7)
# with 1, 2, 4 and 8 threads on MinorCPU cores.
GEM5=~/gem5
N=65536
FU="system.cpu[:].executeFuncUnits.funcUnits[4]"   # the FloatSimdFU
mkdir -p results

for lat in "1 6" "2 5" "3 4" "4 3" "5 2" "6 1"; do
  set -- $lat
  for t in 1 2 4 8; do
    name=op$1_is$2_t$t
    echo "Running $name ..."
    $GEM5/build/X86/gem5.opt -d results/$name \
      $GEM5/configs/deprecated/example/se.py \
      --cpu-type=X86MinorCPU --num-cpus=$t --caches --l2cache \
      -P "$FU.opLat = $1" -P "$FU.issueLat = $2" \
      -c ./daxpy_mt -o "$t $N" > results/$name.log 2>&1
    tail -1 results/$name.log
  done
done
