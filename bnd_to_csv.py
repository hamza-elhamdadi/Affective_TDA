filename = input('Please enter the file name:')

infile = open('Data/' + str(filename) + '.bnd', 'r')
outfile = open('Data/' + str(filename) + '.csv', 'w')

outfile.write('x,y,z\n')

for inline in infile:
    vals = inline.split(' ')
    outline = vals[1] + ',' + vals[2] + ',' + vals[3]
    outfile.write(outline)

outfile.close()