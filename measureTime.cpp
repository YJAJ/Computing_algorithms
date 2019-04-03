#include <time.h>
#include <stdio.h>


int main ()
{
    clock_t start_t, end_t;
    double cpu_time_used;

    start_t = clock();

    /* Do the work. */
    for(int i=0; i<32767; ++i)
    {

        /* do nothing */
    }

    end_t = clock();
    cpu_time_used = ((double) (end_t - start_t)) / CLOCKS_PER_SEC;

    printf("I have slept for %d seconds.", cpu_time_used);

 return 0;
}
