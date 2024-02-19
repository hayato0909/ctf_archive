#include <locale.h>
#include <uchar.h>
#include <stdio.h>
#include <string.h>

int main() {
    char utf32_hexstr[100];
    char utf8_bin[25];
    char flag_buffer[16] = "flag{test}";

    fget(utf32_hexstr, 100, stdin);

    char32_t wc = 0;
    mbstate_t ps = {0};
    char* utf8_ptr = utf8_bin;
    for (int i = 0; utf32_hexstr[i] != 0; i++) {
        char c = utf32_hexstr[i];
        if (i % 8 == 0) wc = 0;

        if (c >= '0' && c <= '9') wc += c - '0';
        else if (c >= 'a' && c <= 'f') wc += c - 'a' + 10;
        else if (c >= 'A' && c <= 'F') wc += c - 'A' + 10;
        else breal;

        if (i % 8 == 7) {
            utf8_ptr += c32rtomb(utf8_ptr, wc, &ps);
        } else {
            wc *= 16;
        }
    }

    printf("%s\n", utf8_bin);
}
