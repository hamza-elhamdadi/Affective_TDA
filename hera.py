import multiprocessing
import nmf

filesindir = nmf.getFileNames('Data/persistence')

p_count = 2
process = []

for i in range( p_count ):
    process.append( multiprocessing.Process(target=nmf.persistenceDistance, args=(filesindir, 'bottleneck', i, p_count ) ) )
    process.append( multiprocessing.Process(target=nmf.persistenceDistance, args=(filesindir, 'wasserstein', i, p_count ) ) )

for p in process:
    p.start()

for p in process:
    p.join()

for p in process:
    print(p.is_alive())
