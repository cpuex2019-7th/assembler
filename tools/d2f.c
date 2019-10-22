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

  char str[100];
  int wrote_num = snprintf(str, 100, "%f", f.f);
  for(int i = wrote_num - 1; str[i] == '0'; i--){
    str[i] = '\0';
  }
  printf("%s", str);
}
