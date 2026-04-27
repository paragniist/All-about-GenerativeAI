# pip install torch numpy==1.26.4

import numpy as np
import torch

print("NumPy version:", np.__version__)

# Create a simple array to verify
array = np.array([1, 2, 3])
print("Array:", array)

# Create a simple tensor
tensor = torch.tensor([1.0, 2.0, 3.0])

# Convert to NumPy array
try:
    np_array = tensor.cpu().numpy()
    print("NumPy array:", np_array)
except RuntimeError as e:
    print(f"RuntimeError: {e}")
