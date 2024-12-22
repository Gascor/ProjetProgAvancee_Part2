#include <stdio.h>
#include <stdlib.h>
#include <curand_kernel.h>
#include <cuda_runtime.h>
#include <math.h>
#include <corecrt_math_defines.h>

// Implémentation manuelle de atomicAdd pour les doubles
__device__ void atomicAddDouble(double* address, double val) {
    unsigned long long int* address_as_ull = (unsigned long long int*)address;
    unsigned long long int old = *address_as_ull, assumed;

    do {
        assumed = old;
        old = atomicCAS(address_as_ull, assumed,
                        __double_as_longlong(val + __longlong_as_double(assumed)));
    } while (assumed != old);
}

// Kernel pour initialiser les états RNG
__global__ void init_rng(curandState *states, unsigned long long seed, int n) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < n) {
        curand_init(seed, idx, 0, &states[idx]);
    }
}

// Kernel pour calculer Pi
__global__ void compute_pi(double *estimate, curandState *states, unsigned long long n_samples) {
    extern __shared__ unsigned long long local_counts[]; // Mémoire partagée
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;

    unsigned long long count = 0;
    double x, y, z;

    // Récupérez l'état RNG pré-initialisé
    curandState local_state = states[idx];

    // Calcul des points dans le cercle
    for (unsigned long long i = idx; i < n_samples; i += stride) {
        x = curand_uniform_double(&local_state);
        y = curand_uniform_double(&local_state);
        z = x * x + y * y;
        if (z <= 1.0) count++;
    }

    states[idx] = local_state;  // Sauvegardez l'état
    local_counts[threadIdx.x] = count;
    __syncthreads();

    // Réduction locale dans le bloc
    for (int offset = blockDim.x / 2; offset > 0; offset >>= 1) {
        if (threadIdx.x < offset) {
            local_counts[threadIdx.x] += local_counts[threadIdx.x + offset];
        }
        __syncthreads();
    }

    // Ajoutez le total du bloc au résultat global
    if (threadIdx.x == 0) {
        atomicAddDouble(estimate, (double)local_counts[0]);
    }
}

// Fonction principale
int main(int argc, char *argv[]) {
    FILE *fp = fopen("pi_results_optimized3suite.csv", "w");
    fprintf(fp, "PI;Difference;Error;Ntot;AvailableProcessors;TimeDuration(ms);\n");

    double *d_estimate, h_estimate;
    curandState *d_states;

    int threadsPerBlock = 1024;
    int numBlocks = 8096;

    cudaMalloc((void **)&d_estimate, sizeof(double));
    cudaMalloc((void **)&d_states, numBlocks * threadsPerBlock * sizeof(curandState));

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    // Initialisation des RNG
    init_rng<<<numBlocks, threadsPerBlock>>>(d_states, time(NULL), numBlocks * threadsPerBlock);
    cudaDeviceSynchronize();

    for (int power = 5; power <= 44; ++power) {
        unsigned long long n_samples = (1ULL << power);

        for (int test = 0; test < 5; ++test) {
            cudaMemset(d_estimate, 0, sizeof(double));

            cudaEventRecord(start);
            compute_pi<<<numBlocks, threadsPerBlock, threadsPerBlock * sizeof(unsigned long long)>>>(d_estimate, d_states, n_samples);
            cudaEventRecord(stop);

            cudaDeviceSynchronize();

            cudaMemcpy(&h_estimate, d_estimate, sizeof(double), cudaMemcpyDeviceToHost);
            printf("Estimate from GPU: %f\n", h_estimate); // Affiche le résultat brut

            h_estimate = (h_estimate / n_samples) * 4.0;
            printf("Calculated PI: %f\n", h_estimate);

            cudaEventSynchronize(stop);
            float milliseconds = 0;
            cudaEventElapsedTime(&milliseconds, start, stop);

            double pi_error = fabs(h_estimate - M_PI);
            fprintf(fp, "%.10f;%.10f;%.10f;%llu;1;%.3f;\n", h_estimate, h_estimate - M_PI, pi_error / M_PI, n_samples, milliseconds);
        }
    }

    cudaFree(d_estimate);
    cudaFree(d_states);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    fclose(fp);

    return 0;
}
