# RISCV_Vector_Zve_PPA
PPA Estimation/Optimization of RISCV Zve Vector Extension
### Current way of performance estimation:
- give the script the binary program to be executed,
- give the DASM file of that binary,
- give it the symbols of the two functions (scalar and vector versions) that will be compared.
- The script will then locate the start and end PC of both functions, and it will count the number of cycles of each function based on the assumed weights for different instructions inside both functions.
