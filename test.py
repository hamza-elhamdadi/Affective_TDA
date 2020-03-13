import csv

with open('Data/bottleneck_dissimilarities.csv', 'r') as file:
    csv_file = csv.reader(file, delimiter=',')
    next(csv_file)
    csv_formatted = map(lambda elem : [elem[0], elem[1], float(elem[2])], csv_file)
    for row in csv_formatted:
        print(row)