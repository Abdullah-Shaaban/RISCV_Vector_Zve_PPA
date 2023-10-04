# ******************************************************************
# This script analyses the trace from Spike (dynamic estimation)
# It assumes different weights for different insructions
# ******************************************************************

import sys
import re

# Files to analyse
dasm_file = sys.argv[1] # # # 'vadd_8bit.dasm'#
trace_file = sys.argv[2] # # #'vadd_8bit_trace.txt'#
# Program Dependent: Element Width (32, 16, or 8 bits) and Application Vector Length
SEW = int(sys.argv[3])
AVL = int(sys.argv[4])
update_AVL_inst = 'Decrement AVL' #'sub     a0, a0, t0'   # Hardcoded until now.
# Machine Dependent: Vector Length in bits, and Max Element Width in bits
VLEN = int(sys.argv[5]) #64
ELEN = 32
# Maximum Vector Length, given a SEW
MVL = VLEN/SEW
# V unit's current VL
VL = MVL if (AVL>MVL) else AVL
# Number of cycles within the Vector Function
V_cycle_cnt = 0.00
# Number of cycles within the Scalar Function
S_cycle_cnt = 0.00
# List of Scalar Instructions.
scalar_inst_list = { 
    'lui' : 1, 
    'auipc' : 1, 
    'li' : 1,
    'mv' : 1,
    'not' : 1,
    'neg' : 1,
    'negw' : 1,
    'slt' : 1,  
    'sltu' : 1,
    'sext' : 1,
    'seqz' : 1,
    'snez' : 1,
    'sltz' : 1,
    'sgtz' : 1,
    'beq' : 2,
    'bne' : 2, 
    'blt' : 2, 
    'bltu' : 2, 
    'bge' : 2, 
    'bgeu' : 2, 
    'blez' : 2, 
    'bnez' : 2,
    'beqz' : 2,
    'bgez' : 2,
    'bltz' : 2,
    'bgtz' : 2,
    'bgt' : 2,
    'ble' : 2,
    'bgtu' : 2,
    'bleu' : 2,
    'j' : 2,
    'jr' : 2,
    'jal' : 2,
    'jalr' : 2,
    'ret' : 2,
    'call' : 2,
    'tail' : 2,
    'lb' : 2,
    'lh' : 2,
    'lw' : 2,
    'lbu' : 2,
    'lhu' : 2,
    'lwu' : 2, 
    'sb' : 2, 
    'sh' : 2, 
    'sw' : 2,   
    'addi' : 1, 
    'slti' : 1, 
    'sltiu' : 1, 
    'xori' : 1, 
    'ori' : 1, 
    'andi' : 1,
    'xor' : 1,
    'or' : 1,
    'and' : 1,
    'slli' : 1, 
    'srli' : 1, 
    'srai' : 1, 
    'sll' : 1,  
    'srl' : 1,  
    'sra' : 1,
    'add' : 1,  
    'sub' : 1, 
    'fence.i' : 1,
    'fence' : 1,
    'fence.tso' : 1,
    'pause' : 1,
    'ecall' : 1,
    'ebreak' : 1,
    'csrrw' : 1,
    'csrrs' : 1,
    'csrrc' : 1,
    'csrrwi' : 1,
    'csrrsi' : 1,
    'csrrci' : 1,
    'csrr' : 1,
    'csrw' : 1,
    'csrs' : 1,
    'csrc' : 1,
    'csrwi' : 1,
    'csrsi' : 1,
    'csrci' : 1,
    'mul' : 1,
    'mulh' : 1,
    'mulhsu' : 1,
    'mulhu' : 1,
    'div' : 1,
    'divu' : 1,
    'rem' : 1,
    'remu' : 1,

    }
# List of Vector Instructions
vector_inst_list = {
    'vadd' : 'VL',
    'vsub' : 'VL',
    'vrsub' : 'VL',
    'vminu' : 'VL',
    'vmin' : 'VL',
    'vmaxu' : 'VL',
    'vmax' : 'VL',
    'vand' : 'VL',
    'vor' : 'VL',
    'vxor' : 'VL',
    'vrgather' : 'VL',
    'vslideup' : 'VL',
    'vrgatherei16' : 'VL',
    'vslidedown' : 'VL',
    'vadc' : 'VL',
    'vmadc' : 'VL',
    'vsbc' : 'VL',
    'vmsbc' : 'VL',
    'vmerge' : 'VL',
    'vmv' : 'VL',
    'vmseq' : 'VL',
    'vmsne' : 'VL',
    'vmsltu' : 'VL',
    'vmslt' : 'VL',
    'vmsleu' : 'VL',
    'vmsle' : 'VL',
    'vmsgtu' : 'VL',
    'vmsgt' : 'VL',
    'vmsge' : 'VL',
    'vmsgeu' : 'VL',
    'vsaddu' : 'VL',
    'vsadd' : 'VL',
    'vssubu' : 'VL',
    'vssub' : 'VL',
    'vsll' : 'VL',
    'vsmul' : 'VL',
    'vmvnrr' : 'VL',
    'vmvr' : 'VL',
    'vsrl' : 'VL',
    'vsra' : 'VL',
    'vssrl' : 'VL',
    'vssra' : 'VL',
    'vnsrl' : 'VL',
    'vnsra' : 'VL',
    'vnclipu' : 'VL',
    'vnclip' : 'VL',
    'vwredsumu' : 'VL',
    'vwredsum' : 'VL',
    'vredsum' : 'VL',
    'vredand' : 'VL',
    'vredor' : 'VL',
    'vredxor' : 'VL',
    'vredminu' : 'VL',
    'vredmin' : 'VL',
    'vredmaxu' : 'VL',
    'vredmax' : 'VL',
    'vaaddu' : 'VL',
    'vaadd' : 'VL',
    'vasubu' : 'VL',
    'vasub' : 'VL',
    'vslide1up' : 'VL',
    'vslide1down' : 'VL',
    'vcompress' : 'VL',
    'viota' : 'VL',
    'vid' : 'VL',
    'vdivu' : 'VL',
    'vdiv' : 'VL',
    'vremu' : 'VL',
    'vrem' : 'VL',
    'vmulhu' : 'VL',
    'vmul' : 'VL',
    'vmulhsu' : 'VL',
    'vmulh' : 'VL',
    'vmadd' : 'VL',
    'vnmsub' : 'VL',
    'vmacc' : 'VL',
    'vnmsac' : 'VL',
    'vwaddu' : 'VL',
    'vwadd' : 'VL',
    'vwsubu' : 'VL',
    'vwsub' : 'VL',
    'vwaddu.w' : 'VL',
    'vwadd.w' : 'VL',
    'vwsubu.w' : 'VL',
    'vwsub.w' : 'VL',
    'vwmulu' : 'VL',
    'vwmulsu' : 'VL',
    'vwmul' : 'VL',
    'vwmaccu' : 'VL',
    'vwmacc' : 'VL',
    'vwmaccus' : 'VL',
    'vwmaccsu' : 'VL',
    'vzext' : 'VL',
    'vsext' : 'VL',
    'vzext' : 'VL',
    'vsext' : 'VL',
    'vzext' : 'VL',
    'vsext' : 'VL',
    'vle8' : 'VL+2',
    'vle16' : 'VL+2',
    'vle32' : 'VL+2',
    'vse8' : 'VL+2',
    'vse16' : 'VL+2',
    'vse32' : 'VL+2',
    'vlse8' : 'VL+2',
    'vlse16' : 'VL+2',
    'vlse32' : 'VL+2',
    'vsse8' : 'VL+2',
    'vsse16' : 'VL+2',
    'vsse32' : 'VL+2',
    'vluxei8' : 'VL+2',
    'vluxei16' : 'VL+2',
    'vluxei32' : 'VL+2',
    'vluxei64' : 'VL+2',
    'vloxei8' : 'VL+2',
    'vloxei16' : 'VL+2',
    'vloxei32' : 'VL+2',
    'vsuxei8' : 'VL+2',
    'vsuxei16' : 'VL+2',
    'vsuxei32' : 'VL+2',
    'vsoxei8' : 'VL+2',
    'vsoxei16' : 'VL+2',
    'vsoxei32' : 'VL+2',
    'vle8ff' : 'VL+2',
    'vle16ff' : 'VL+2',
    'vle32ff' : 'VL+2',
    'vlseg' : 'VL+2',
    'vsseg' : 'VL+2',
    'vlsseg' : 'VL+2',
    'vssseg' : 'VL+2',
    'vluxseg': 'VL+2',
    'vloxseg': 'VL+2',
    'vsuxseg': 'VL+2',
    'vsoxseg': 'VL+2',
    'vl1r' : 'VL+2',
    'vl2r' : 'VL+2',
    'vl4r' : 'VL+2',
    'vl8r' : 'VL+2',
    'vs1r' : 'VL+2',
    'vs2r' : 'VL+2',
    'vs4r' : 'VL+2',
    'vs8r' : 'VL+2',
    'vsetvli' : '1',
    'vsetvl' : '1',
    'vsetivli' : '1',
    'vmandnot' : '1',
    'vmand' : '1',
    'vmor' : '1',
    'vmxor' : '1',
    'vmornot' : '1',
    'vmnand' : '1',
    'vmnor' : '1',
    'vmxnor' : '1',
    'vmmv' : '1', 
    'vmclr' : '1',
    'vmset' : '1',
    'vmnot' : '1',  
    'vcpop' : '1',
    'vfirst' : '1',
    'vmsbf' : '1',
    'vmsif' : '1',
    'vmsof' : '1',
    'vlm' : '2'
    }   


# Analyse the dasm file and find the Start and End PC of Vector and Scalar functions
# The Start and End PC values are used to navigate the trace file from Spike.
DASM = open(dasm_file, 'r')
# read all lines using readline()
lines = DASM.readlines()
funct_scalar = '<add_scal>:'
funct_vector = '<add_vec>:'
search_for_scalar_ret = 0
search_for_vector_ret = 0
# Iterate through lines of the file
for line in lines:
    # When you find the start of scalar function, start counting instructions until ret is found
    if search_for_scalar_ret == 1:
        if line.find('ret') != -1:
            scalar_end_PC = line.split()[0].replace(':','')
            search_for_scalar_ret = 0
    if line.find(funct_scalar) != -1:
        scalar_start_PC = line.split()[0]
        search_for_scalar_ret = 1
    # When you find the start of vector function, start counting instructions until ret is found
    if search_for_vector_ret == 1: 
        if line.find('ret') != -1:
            vector_end_PC = line.split()[0].replace(':','')
            search_for_vector_ret = 0
    if line.find(funct_vector) != -1:
        vector_start_PC = line.split()[0]
        search_for_vector_ret = 1
DASM.close()


# Analyse the trace file from Spike. Indentify the Scalar and Vector functions and count the cycles used by both, one instruction at a time.
TRACE = open(trace_file, 'r')
# read all lines using readline()
lines = TRACE.readlines()
scalar_count_en = 0
vector_count_en = 0
# Iterate through lines of the file
for line in lines:
    # Count cycles between scalar_start_PC and scalar_end_PC
    if line.find(scalar_start_PC) != -1:
        scalar_count_en = 1
    if scalar_count_en == 1:
        for inst in scalar_inst_list:   # Figure out type of instruction by looping on the scalar list
            if re.search(r'\b' + inst + r'\b', line):
                S_cycle_cnt = S_cycle_cnt + scalar_inst_list[inst]   # Add the weight of this particular insruction
                break
    if line.find(scalar_end_PC) != -1:
        scalar_count_en = 0
    # Count Cycles between vector_start_PC and vector_end_PC
    if line.find(vector_start_PC) != -1:
        vector_count_en = 1
    if vector_count_en == 1:
        V_cycle_cnt_OLD = V_cycle_cnt
        # Determine the instruction type. Note that Vector code includes scalar insructions as well
        for inst in vector_inst_list:   
            if re.search(r'\b' + inst + r'\b', line):
                # Update current VL when you hit vsetvli
                if inst == 'vsetvli' : 
                    VL = MVL if (AVL>MVL) else AVL
                # Update cycle count
                if vector_inst_list[inst]=='VL':
                    V_cycle_cnt = V_cycle_cnt + VL
                elif  vector_inst_list[inst]=='VL+2':
                    V_cycle_cnt = V_cycle_cnt + VL+2
                else:
                    V_cycle_cnt = V_cycle_cnt + int(vector_inst_list[inst])
                break  
        # Seach for Scalar instruction only if it's not a Vector instructions (V_cycle_cnt not incremented)
        if V_cycle_cnt == V_cycle_cnt_OLD:
            for inst in scalar_inst_list:
                if re.search(r'\b' + inst + r'\b', line): 
                    # Update AVL when you hit instruction that does AVL = AVL - VL
                    if line.find(update_AVL_inst) !=-1 : 
                        AVL = AVL - VL
                    # Update cycle count
                    V_cycle_cnt = V_cycle_cnt + scalar_inst_list[inst]
                    break  
    if line.find(vector_end_PC) != -1:
        vector_count_en = 0
TRACE.close()


print('Number of cycles in Scalar Function ~', S_cycle_cnt)
print('Number of cycles in Vector Function ~', V_cycle_cnt)
print('Speedup ~', format(S_cycle_cnt/V_cycle_cnt, '.2f'), 'x')