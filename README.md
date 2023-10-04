# RISCV_Vector_Zve_PPA
PPA Estimation/Optimization of RISCV Zve Vector Extension
### Current way of performance estimation:
- give the script the binary program to be executed,
- give the DASM file of that binary,
- give it the symbols of the two functions (scalar and vector versions) that will be compared.
- The script will then locate the start and end PC of both functions, and it will count the number of cycles of each function based on the assumed weights for different instructions inside both functions.
### Dependency
This repository uses Spike, a RISCV ISA simulator. It also uses a modified version of Hammer, which provides an interface to Spike that enable interaction with the simulator using C++ or Python.
You can clone the modified Hammer version by executing:
`git clone https://github.com/Abdullah-Shaaban/hammer_vector.git`
