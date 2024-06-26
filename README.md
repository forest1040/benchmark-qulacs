# Benchmark codes for Qulacs

fork by https://github.com/qulacs/benchmark-qulacs

A100 vs H100

# Setup
```
pip install pytest pytest-benchmark
```

# Build Qulacs for GPU
```
USE_GPU=Yes ./script/build_gcc_with_gpu.sh
USE_GPU=Yes pip install .
```

# Qulacs multithread
`export QULACS_PARALLEL_NQUBIT_THRESHOLD=1`

# PennyLane Lightning
```
pip install pennylane --upgrade
pip install pennylane-lightning pennylane-lightning[gpu]
```

## cuQuantum install
```
pip install custatevec-cu11
```

# QIBO
```
pip install qibo qibojit
```

# Execute Bench
```
cd benchmark/singlethread
sh execall.sh

cd benchmark/multithread
sh execall.sh

cd benchmark/gpu
sh execall.sh
```

# plot result
```
python plot.py
```
