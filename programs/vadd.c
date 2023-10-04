// #include <stdio.h>
// #include <math.h>
// #include <stdlib.h>

// Define The Application Vector Length (i.r., Array Length = Loop Iterations)
#define AVL 10

void add_vec(int n, char*x, char*y, char*z);

void __attribute__ ((noinline)) add_scal(int n, char*x, char*y, char*z){
    for (int i=0; i<n; i++){ 
        z[i]=x[i]+y[i]; 
    } 
}

int main(){
  // Enable V Unit -- Set mstatus.VS (bits 9 and 10) to 2 (Clean)
  __asm__ (
    "csrr t4, mstatus;"
    "li t5, 0x200;" 
    "or t4, t4, t5;"
    "csrw mstatus, t4;"
    );
  char out_scalar[AVL], out_vector[AVL];
  char in1[AVL];
  char in2[AVL];
  // Fill the input arrays
  for (int i = 0; i < AVL; i++)
  {
    in1[i] = i; //rand();
    in2[i] = i;   //rand();
  }
  
  add_scal(AVL, in1, in2, out_scalar);
  add_vec(AVL, in1, in2, out_vector);

  for (int i=0; i<AVL; ++i){
    if(out_scalar[i] != out_vector[i]){
      // printf("ERROR!\n");
      return -1;
      // break;
    }
  }
  return 0;
}