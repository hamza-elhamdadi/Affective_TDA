import multiprocessing
import nmf

filesindir = nmf.getFileNames('Data/persistence')

process1 = multiprocessing.Process(target=nmf.persistenceDistance, args=(filesindir, 'bottleneck', ))
process2 = multiprocessing.Process(target=nmf.persistenceDistance, args=(filesindir, 'wasserstein', ))

process1.start()
process2.start()

process1.join()
process2.join()

print(process1.is_alive())
print(process2.is_alive())