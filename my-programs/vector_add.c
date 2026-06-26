#include <stdio.h>
#include <stdlib.h>

#define VECTOR_SIZE 16

int
main()
{
    int *vecA = (int *)malloc(VECTOR_SIZE * sizeof(int));
    int *vecB = (int *)malloc(VECTOR_SIZE * sizeof(int));
    int *vecC = (int *)malloc(VECTOR_SIZE * sizeof(int));

    // Initialize vectors
    for (int i = 0; i < VECTOR_SIZE; i++) {
        vecA[i] = i;
        vecB[i] = i * 2;
    }

    // Vector Addition
    for (int i = 0; i < VECTOR_SIZE; i++) {
        vecC[i] = vecA[i] + vecB[i];
    }

    // Print a few results to verify
    printf("Vector addition complete.\n");
    printf("vecC[0] = %d\n", vecC[0]);
    printf("vecC[10] = %d\n", vecC[10]);

    free(vecA);
    free(vecB);
    free(vecC);

    return 0;
}
