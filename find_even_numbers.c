#include <stdio.h>

int main() {
    printf("Even numbers from 1 to 10:\n");
    
    // Loop through numbers 1 to 10
    for (int i = 1; i <= 10; i++) {
        // Check if number is even (divisible by 2)
        if (i % 2 == 0) {
            printf("%d\n", i);
        }
    }
    
    return 0;
}