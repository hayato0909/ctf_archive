#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/random.h>

char password[0x20];

int main() {
    if (getrandom(password, sizeof(password), 0) != sizeof(password)) {
        perror("getrandom");
        return 1;
    }
    printf("get password: %s\n", password);

    for (size_t i = 0; i < 9; i++) {
        password[i] = 0x21 + ((unsigned char)password[i] % (0x7e - 0x21));
    }
    printf("password: %s\n", password);
}
