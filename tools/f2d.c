#include <stdio.h>
#include <stdlib.h>

typedef union {
  float f;
  int  i;
} fi;

int main(int argc, char *argv[]){
  fi f;
  if (argc < 2){
    scanf("%f", &(f.f));
  } else {
    f.f = strtof(argv[1], NULL);
  }
  printf("%d", f.i);
}
