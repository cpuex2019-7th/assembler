#include <stdio.h>
#include <stdlib.h>

typedef union {
  float f;
  int  i;
} fi;

int main(int argc, char *argv[]){
  if (argc < 2){
    printf("%s i\n", argv[0]);
    exit(1);
  }
  fi f;
  f.i = atoi(argv[1]);  
  printf("%f", f.f);
}
