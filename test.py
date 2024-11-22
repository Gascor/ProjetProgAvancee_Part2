# %%
from numba import cuda, types
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np

# %%
@cuda.jit
def sim_pi_cuda(out, rng_state, iterations):
    grid_idx = cuda.grid(1)
    warp_size = 32

    counts = cuda.shared.array(warp_size, dtype=types.uint64)

    counts[cuda.threadIdx.x] = 0
    for _ in range(iterations):
        x = xoroshiro128p_uniform_float32(rng_state, grid_idx)
        y = xoroshiro128p_uniform_float32(rng_state, grid_idx)
        counts[cuda.threadIdx.x] += 1 - int(x*x + y*y)
    
    cuda.syncthreads()

    if cuda.threadIdx.x == 0:
        out[cuda.blockIdx.x] = 0

        for i in range(warp_size):
            out[cuda.blockIdx.x] += counts[i]

# %%
def sim_pi(iterations):
    blocks = 10496
    warp_size = 32

    out = cuda.device_array(blocks, dtype=np.uint64)

    seed = np.random.randint(0, 2**64, dtype=np.uint64)
    rng_state = create_xoroshiro128p_states(warp_size * blocks, seed=seed)

    sim_pi_cuda[blocks, warp_size](out, rng_state, iterations)
    data = out.copy_to_host()
    data.sort()
    
    return (4.0 * data.sum()) / (iterations*blocks*warp_size)

# %%
N = 1_000_000_0
print(sim_pi(N))