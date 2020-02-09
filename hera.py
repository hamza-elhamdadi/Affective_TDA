import multiprocessing
import os

filesindir = os.listdir('../Data')

def file_1():
    with open('Data/bottleneck_values.csv', 'w') as file:
        file.write('file1,file2,bottleneck_distance\n')
        for i in range(len(filesindir)):
            for j in range(i+1,len(filesindir)):
                command_1 = 'echo ' + filesindir[i][0:3] + ',' + filesindir[j][0:3]
                command_2 = './hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence/persistence_diagram_' + filesindir[i][0:3] + '.txt ./Data/persistence/persistence_diagram_' + filesindir[j][0:3] + '.txt'
                echostream = os.popen(command_1)
                herastream = os.popen(command_2)
                file.write(echostream.read()[:-1] + ',' + herastream.read()[:-1] + '\n')

def file_2():
    with open('Data/wasserstein_values.csv', 'w') as file:
        file.write('file1,file2,wasserstein_distance\n')
        for i in range(len(filesindir)):
            for j in range(i+1,len(filesindir)):
                command_1 = 'echo ' + filesindir[i][0:3] + ',' + filesindir[j][0:3]
                command_2 = './hera/geom_matching/wasserstein/wasserstein_dist ./Data/persistence/persistence_diagram_' + filesindir[i][0:3] + '.txt ./Data/persistence/persistence_diagram_' + filesindir[j][0:3] + '.txt'
                echostream = os.popen(command_1)
                herastream = os.popen(command_2)
                file.write(echostream.read()[:-1] + ',' + herastream.read()[:-1] + '\n') 


process1 = multiprocessing.Process(target=file_1)
process2 = multiprocessing.Process(target=file_2)

process1.start()
process2.start()