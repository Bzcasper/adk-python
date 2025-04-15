"""Test script for ContentFlow AI GPU access in Modal Labs.

This script tests GPU access in Modal Labs by running a simple PyTorch operation
on the GPU and measuring the performance.
"""

import modal
import time
import torch
from datetime import datetime

# Define a simple Modal stub for GPU testing
stub = modal.Stub("contentflow-ai-gpu-test")

# Define the image with PyTorch
gpu_image = modal.Image.debian_slim().pip_install([
    "torch>=2.2.0",
    "numpy>=1.26.0",
])

@stub.function(
    image=gpu_image,
    gpu="A100",  # Request an A100 GPU
    timeout=300,
)
def test_gpu_performance():
    """Test GPU performance by running a simple PyTorch operation."""
    print(f"Testing GPU performance at {datetime.now().isoformat()}...")
    
    # Check if CUDA is available
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. GPU access failed.")
    
    # Print GPU information
    device_count = torch.cuda.device_count()
    print(f"Number of available GPUs: {device_count}")
    
    for i in range(device_count):
        device_name = torch.cuda.get_device_name(i)
        print(f"GPU {i}: {device_name}")
    
    # Create a large tensor on the GPU
    size = 10000
    print(f"Creating {size}x{size} matrices for multiplication...")
    
    # Measure CPU performance
    start_time = time.time()
    a_cpu = torch.randn(size, size)
    b_cpu = torch.randn(size, size)
    c_cpu = torch.matmul(a_cpu, b_cpu)
    cpu_time = time.time() - start_time
    print(f"CPU matrix multiplication time: {cpu_time:.4f} seconds")
    
    # Measure GPU performance
    start_time = time.time()
    a_gpu = torch.randn(size, size, device="cuda")
    b_gpu = torch.randn(size, size, device="cuda")
    c_gpu = torch.matmul(a_gpu, b_gpu)
    # Synchronize to ensure operation is complete
    torch.cuda.synchronize()
    gpu_time = time.time() - start_time
    print(f"GPU matrix multiplication time: {gpu_time:.4f} seconds")
    
    # Calculate speedup
    speedup = cpu_time / gpu_time
    print(f"GPU speedup: {speedup:.2f}x")
    
    return {
        "gpu_available": True,
        "device_count": device_count,
        "device_names": [torch.cuda.get_device_name(i) for i in range(device_count)],
        "cpu_time": cpu_time,
        "gpu_time": gpu_time,
        "speedup": speedup,
        "timestamp": datetime.now().isoformat(),
    }

def main():
    """Run the GPU test."""
    print("Starting GPU test...")
    with stub.run():
        result = test_gpu_performance.remote()
    
    print("\nGPU Test Results:")
    print(f"GPU Available: {result['gpu_available']}")
    print(f"Number of GPUs: {result['device_count']}")
    print(f"GPU Names: {', '.join(result['device_names'])}")
    print(f"CPU Time: {result['cpu_time']:.4f} seconds")
    print(f"GPU Time: {result['gpu_time']:.4f} seconds")
    print(f"Speedup: {result['speedup']:.2f}x")
    print(f"Test completed at: {result['timestamp']}")
    
    print("\nGPU test completed successfully!")

if __name__ == "__main__":
    main()
