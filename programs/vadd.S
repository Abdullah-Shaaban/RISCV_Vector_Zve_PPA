  .text

    .global _start
_start:
    j main
infinity_loop:
    nop
    j infinity_loop
    

# a0 = n, a1 = *x, a2 = *y, a3 = *z
    .global add_vec
add_vec:
    # Do the computation
    vsetvli t0, a0, e8, m1  # Set vector length based on 8-bit elements
    sub a0, a0, t0      # Decrement AVL
#    slli t0, t0, 2     # Multiply number done by 4 bytes
    vle8.v v0, (a1)     # Get first vector
    add a1, a1, t0      # Bump pointer
    vle8.v v1, (a2)     # Get second vector
    add a2, a2, t0      # Bump pointer
    vadd.vv v2, v0, v1  # Sum vectors
    vse8.v v2, (a3)     # Store result
    add a3, a3, t0      # Bump pointer
    bnez a0, add_vec    # Loop back
    ret                 # Finished