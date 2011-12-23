import sys
import cPickle as pickle

if len(sys.argv) != 3:
    print 'Usage: script.py input output'
    sys.exit()

in_path, out_path = sys.argv[1:]
benchmarks = pickle.load(open(in_path))

results = {}
for bmk in benchmarks:
    try:
        res = bmk.run()
    except Exception:
        continue
    results[bmk.checksum] = res

benchmarks = pickle.dump(results, open(out_path, 'w'))
