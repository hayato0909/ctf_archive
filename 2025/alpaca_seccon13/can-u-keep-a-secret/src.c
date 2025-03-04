#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main() {
    srand(time(NULL));
    unsigned int secret = rand(), input;
    printf("secret: %u\n", secret);

    // can u keep a secret??/
    secret *= rand();
    secret *= 0x5EC12E7;
    scanf("%u", &input);
    if(input == secret)
        printf("Alpaca{REDACTED}\n");
    return 0;
}

__attribute__((constructor)) void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);
}
