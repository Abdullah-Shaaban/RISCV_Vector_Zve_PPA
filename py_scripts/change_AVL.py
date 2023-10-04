import sys
C_file = sys.argv[1]
new_AVL = sys.argv[2]
with open(C_file) as file:
    lines = file.readlines()
    for line in lines:
        if line.find('#define AVL') != -1:
            index = lines.index(line)
            lines[index] = '#define AVL ' + new_AVL + '\n'

with open(C_file, 'w') as file:
    for line in lines:
        file.write(line)