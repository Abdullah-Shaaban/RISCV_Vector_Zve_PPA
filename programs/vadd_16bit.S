
# a0 = n, a1 = *x, a2 = *y, a3 = *z

   .globl add_vec
add_vec:
    vsetvli t0, a0, e16, m1  # Set vector length based on 16-bit elements
    sub a0, a0, t0      # Decrement AVL
    slli t0, t0, 1      # Multiply number done by 2 (each element is 2 bytes)
    vle16.v v0, (a1)     # Get first vector
    add a1, a1, t0      # Bump pointer
    vle16.v v1, (a2)     # Get second vector
    add a2, a2, t0      # Bump pointer
    vadd.vv v2, v0, v1  # Sum vectors
    vse16.v v2, (a3)     # Store result
    add a3, a3, t0      # Bump pointer
    bnez a0, add_vec    # Loop back
    ret                 # Finished