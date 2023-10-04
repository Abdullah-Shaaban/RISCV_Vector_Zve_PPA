#include <stdio.h>
#include <math.h>
#include <stdlib.h>

// Define The Application Vector Length (i.r., Array Length = Loop Iterations)
#define AVL 10

void add_vec(int n, __int16_t*x, __int16_t*y, __int16_t*z);

void add_scal(int n, __int16_t*x, __int16_t*y, __int16_t*z){
    for (int i=0; i<n; i++){ 
        z[i]=x[i]+y[i]; 
    } 
}

int main(){
  __int16_t out_scalar[AVL], out_vector[AVL];
  __int16_t in1[AVL];
  __int16_t in2[AVL];
  // Fill the input arrays
  for (int i = 0; i < AVL; i++)
  {
    in1[i] = rand();
    in2[i] = rand();
  }
  
  
  add_scal(AVL, in1, in2, out_scalar);
  add_vec(AVL, in1, in2, out_vector);

  for (int i=0; i<AVL; ++i){
    if(out_scalar[i] != out_vector[i]){
      printf("ERROR!\n");
    }
  }
  return 0;
}
