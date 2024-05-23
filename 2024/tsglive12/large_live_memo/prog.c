// gcc -Wl,-z,relro,-z,now -no-pie prog.c -o chall
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define NMAX 100

char FLAG1[NMAX];
unsigned *bufs[3];
unsigned sizes[3];

void menu() {
    puts("1. create");
    puts("2. put");
    puts("3. read");
    puts("4. exit");
    printf("> ");
}

unsigned get_val(const char *prompt) {
    unsigned x = 0;
    printf("%s > ", prompt);
    scanf("%u", &x);
    return x;
}

void setup() {
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);
    setbuf(stderr,NULL);
    int fd = open("./flag1", O_RDONLY);
    read(fd, FLAG1, NMAX);
    close(fd);
}

int main(void) {
    int x = 0;
    int index = 0;

    setup();

    while(1) {
        menu();
        scanf("%d", &x);
        if (x < 1 || x > 3) return 0;

        index = get_val("index");
        if (index < 0 || index >= 3 ) continue;

        switch (x) {
            case 1:
                x = get_val("size");
                if (NMAX <= x) continue;
                bufs[index] = malloc(x * sizeof(int));
                sizes[index] = x;
                break;
            case 2:
                x = get_val("pos");
                if (sizes[index] <= x) continue;
                bufs[index][x] = get_val("data");
                break;
            case 3:
                x = get_val("pos");
                if (sizes[index] <= x) continue;
                printf("data > %u\n", bufs[index][x]);
                break;
        }
    }
}
