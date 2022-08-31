file = 'ex4.txt'

tokeep = set()
tokeep.add('|')
tokeep.add('-')
tokeep.add('+')

with open(file, 'r') as fh:
    lines = fh.readlines()
    for i,l in enumerate(lines):
        llist = []
        for j,e in enumerate(l):
            if e not in tokeep:
                llist.append(' ')
            else:
                llist.append(e)
        lines[i] = ''.join(llist)

with open('boxes_output.txt', 'w') as fh:
    for l in lines:
        fh.write(l)
        fh.write('\n')