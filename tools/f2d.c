#include <stdio.h>
#include <stdlib.h>

typedef union {
  float f;
  int  i;
} fi;

int main(int argc, char *argv[]){
  if (argc < 2){
    printf("%s (a float ... e.g. 0.9)\n", argv[0]);
    exit(1);
  }
  fi f;
  f.f = strtof(argv[1], NULL);
  printf("%d", f.i);
}
