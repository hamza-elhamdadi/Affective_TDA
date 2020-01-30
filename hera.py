import subprocess as sp

sp.call(['touch', 'bottleneck_values.csv'])
sp.call(['touch', 'wasserstein_values.csv'])

# bottleneck distances

cmd_1 = 'echo "000,001" > bottleneck_values.csv'
cmd_2 = './hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_001.txt >> bottleneck_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])

cmd_1 = 'echo "000,002" > bottleneck_values.csv'
cmd_2 = './hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_002.txt >> bottleneck_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])

cmd_1 = 'echo "001,002" > bottleneck_values.csv'
cmd_2 = './hera/geom_bottleneck/build/bottleneck_dist ./Data/persistence_diagram_001.txt ./Data/persistence_diagram_002.txt >> bottleneck_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])

# wasserstein distances

cmd_1 = 'echo "000,001" > wasserstein_values.csv'
cmd_2 = './hera/geom_matching/wasserstein/build/wasserstein_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_001.txt >> wasserstein_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])

cmd_1 = 'echo "000,002" > wasserstein_values.csv'
cmd_2 = './hera/geom_matching/wasserstein/build/wasserstein_dist ./Data/persistence_diagram_000.txt ./Data/persistence_diagram_002.txt >> bottleneck_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])

cmd_1 = 'echo "001,002" > wasserstein_values.csv'
cmd_2 = './hera/geom_matching/wasserstein/build/wasserstein_dist ./Data/persistence_diagram_001.txt ./Data/persistence_diagram_002.txt >> bottleneck_values.csv'

sp.call(['sh', '-c', cmd_1])
sp.call(['sh', '-c', cmd_2])