import subprocess as sp
import os

with open('Data/bottleneck_values.csv', 'w') as file:
    echostream = [
        os.popen('echo 000,001'), 
        os.popen('echo 000,002'), 
        os.popen('echo 001,002'), 
    ]
    herastream = [
        os.popen('./hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_001.txt'),
        os.popen('./hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_002.txt'),
        os.popen('./hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_001.txt ./Data/persistence_diagram_002.txt')
    ]
    file.write('file1,file2,bottleneck_distance\n')
    for i in range(len(echostream)):
        file.write(echostream[i].read()[:-1] + ',' + herastream[i].read()[:-1])
        file.write('\n')

with open('Data/wasserstein_values.csv', 'w') as file:
    echostream = [
        os.popen('echo 000,001'), 
        os.popen('echo 000,002'), 
        os.popen('echo 001,002'), 
    ]
    herastream = [
        os.popen('./hera/geom_matching/wasserstein/wasserstein_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_001.txt'),
        os.popen('./hera/geom_matching/wasserstein/wasserstein_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_002.txt'),
        os.popen('./hera/geom_matching/wasserstein/wasserstein_dist ./Data/persistence_diagram_001.txt ./Data/persistence_diagram_002.txt')
    ]
    file.write('file1,file2,wasserstein_distance\n')
    for i in range(len(echostream)):
        file.write(echostream[i].read()[:-1] + ',' + herastream[i].read()[:-1])
        file.write('\n')