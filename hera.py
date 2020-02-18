import multiprocessing
import nmf

filesindir = nmf.getFileNames('../Data')

process1 = multiprocessing.Process(target=nmf.persistenceDistance(filesindir, 'bottleneck'))
process2 = multiprocessing.Process(target=nmf.persistenceDistance(filesindir, 'wasserstein'))

process1.start()
process2.start()