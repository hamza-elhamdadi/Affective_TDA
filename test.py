bottleneck_diss = []
wasserstein_diss = []

with open('Data/bottleneck_values.csv', 'r') as file:
    next(iter(file))
    # x = len(list(file))
    for i in range(3):
        row = []
        for j in range(3):
            row.append(0)
        bottleneck_diss.append(row)
    print(list(file))