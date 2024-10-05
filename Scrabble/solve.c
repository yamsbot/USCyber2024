#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, uint8_t *argv[]) {
    int fs_o, i;
    uint8_t v1;
    
    FILE *fs = fopen(argv[1], "rb");
    
    fseek(fs,0,SEEK_END);
    size_t fo = ftell(fs);
    fseek(fs,0,SEEK_SET);
    
    srand((unsigned int)fo);
    fs_o = (int)fo;

    int r0[fs_o];
    int r1[fs_o];
    int r2[fs_o];
    
    void* mem = malloc(fo);
    fread(mem,1,fo,fs);
    fclose(fs);

    for (i = fs_o-1; i >= 0; i--) {
        r0[i] = rand() % fs_o;
        r1[i] = rand();
        r2[i] = rand();
        fs_o = i;
    }

    fs_o = (int)fo;
    for (i = 0; i <= fs_o-1; i++) {
       *((uint8_t*)((uintptr_t)mem + i)) ^= r2[i];
       *((uint8_t*)((uintptr_t)mem + r0[i])) ^= r1[i];

       v1 = *((uint8_t*)((uintptr_t)mem + i));
       *((uint8_t*)((uintptr_t)mem + i)) = *((uint8_t*)((uintptr_t)mem + r0[i]));
       *((uint8_t*)((uintptr_t)mem + r0[i])) = v1;
    }

    fwrite(mem,1,fo,stdout);
    free(mem);

    return 0;
}
