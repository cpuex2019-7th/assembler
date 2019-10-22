#include <stdio.h>
#include <stdlib.h>

typedef union {
  float f;
  int  i;
} fi;

int main(int argc, char *argv[]){
  fi f;
  if (argc < 2){
    scanf("%d", &(f.i));
  } else {
    f.i = atoi(argv[1]);  
  }
  printf("%f", f.f);
}
