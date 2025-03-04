#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void wakekko() {
    const char *word = "alpaca";
    char ans[0x10];
    int pos = rand() % (strlen(word) - 1) + 1;
    printf("%.*s ", pos, word);
    gets(ans);
    if(strcmp(ans, word + pos) != 0) {
        system("echo ':('\n");
        exit(1);
    }
}

int main() {
    srand(time(NULL));
    while(1)
        wakekko();
    return 0;
}

__attribute__((constructor)) void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);
}
