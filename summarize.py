# summarize.py - pull the key numbers out of every run in results/
# Only the first stats block is used (the daxpy region of interest).
import re, os

designs = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]
threads = [1, 2, 4, 8]

def roi_stats(path):
    stats = {}
    for line in open(path):
        if "End Simulation Statistics" in line:
            break                      # stop after the first block
        parts = line.split()
        if len(parts) >= 2:
            try:
                stats[parts[0]] = float(parts[1])
            except ValueError:
                pass
    return stats

print("design     thr  simSeconds    speedup  avgIPC  avgCPI  FPops/cpu  FU_util")
base_time = {}
for op, iss in designs:
    for t in threads:
        f = f"results/op{op}_is{iss}_t{t}/stats.txt"
        if not os.path.exists(f):
            print(f"missing {f}")
            continue
        s = roi_stats(f)
        sec = s["simSeconds"]
        if t == 1:
            base_time[(op, iss)] = sec
        speedup = base_time[(op, iss)] / sec
        ipcs, cpis, fps, utils = [], [], [], []
        for c in range(t):
            cpu = "system.cpu" if t == 1 else f"system.cpu{c}"
            ipcs.append(s.get(cpu + ".ipc", 0))
            cpis.append(s.get(cpu + ".cpi", 0))
            # count instructions that ran on the FloatSimdFU on this core
            # (FloatMemRead/FloatMemWrite run on the memory unit, so skip them)
            fp = sum(v for k, v in s.items()
                     if re.match(re.escape(cpu) + r"\..*committedInstType.*::(Float(?!Mem)|SimdFloat)", k))
            cycles = s.get(cpu + ".numCycles", 1)
            fps.append(fp)
            utils.append(fp * iss / cycles)   # share of cycles the FU is busy issuing
        n = len(ipcs)
        print(f"op{op}_is{iss}   {t:>2}  {sec:.8f}  {speedup:7.2f}  {sum(ipcs)/n:6.3f}  "
              f"{sum(cpis)/n:6.2f}  {sum(fps)/n:9.0f}  {100*sum(utils)/n:6.1f}%")
