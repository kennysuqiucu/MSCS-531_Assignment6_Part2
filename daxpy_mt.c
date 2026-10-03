// daxpy_mt.c - multi-threaded daxpy kernel: y = a * x + y
// Each thread handles an equal slice of the vectors.
// Usage: ./daxpy_mt <threads> <N>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <gem5/m5ops.h>

#define MAX_THREADS 8

int N;              // vector length
int T;              // number of threads
double a = 2.0;
double *x, *y;

void daxpy_part(long id)
{
    int chunk = N / T;
    int start = id * chunk;
    int end = (id == T - 1) ? N : start + chunk;
    for (int i = start; i < end; i++)
        y[i] = a * x[i] + y[i];
}

void *worker(void *arg)
{
    daxpy_part((long)arg);
    return NULL;
}

int main(int argc, char *argv[])
{
    T = (argc > 1) ? atoi(argv[1]) : 1;
    N = (argc > 2) ? atoi(argv[2]) : 65536;
    if (T < 1 || T > MAX_THREADS) T = 1;

    x = malloc(N * sizeof(double));
    y = malloc(N * sizeof(double));
    for (int i = 0; i < N; i++) { x[i] = 1.0; y[i] = 2.0; }

    pthread_t th[MAX_THREADS];

    m5_reset_stats(0, 0);                   // start of region of interest
    for (long t = 1; t < T; t++)            // main thread works as thread 0
        pthread_create(&th[t], NULL, worker, (void *)t);
    daxpy_part(0);
    for (long t = 1; t < T; t++)
        pthread_join(th[t], NULL);
    m5_dump_stats(0, 0);                    // end of region of interest

    printf("threads=%d N=%d y[0]=%.1f y[N-1]=%.1f\n", T, N, y[0], y[N - 1]);
    return 0;
}
