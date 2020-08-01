import nmf, os

h0Dir = '../outputData/nonmetric/F001/subsections/persistence/h0/'
h1Dir = '../outputData/nonmetric/F001/subsections/persistence/h1/'

directories = os.listdir(h0Dir)

filesH0 = [nmf.getFileNames(h0Dir + d, '.txt') for d in directories]
filesH1 = [nmf.getFileNames(h1Dir + d, '.txt') for d in directories]

print(len(filesH0[133]))

"""for i in range(len(filesH0)):
    outputFileH0 = f'{h0Dir}{directories[i]}_fileList.txt'
    outputFileH1 = f'{h1Dir}{directories[i]}_fileList.txt'

    with open(outputFileH0, 'w') as file:
        file.write('\n'.join(filesH0[i]))
    
    with open(outputFileH1, 'w') as file:
        file.write('\n'.join(filesH1[i]))"""



