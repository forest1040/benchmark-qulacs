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
