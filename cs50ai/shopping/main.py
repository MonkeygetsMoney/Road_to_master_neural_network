# this is where i'm experimenting with reading csv files
import csv

with open('shopping/test.csv', newline='') as file:
    mainfile = csv.reader(file)

    next(mainfile) # skip the first row
    
    # split by comma as default
    for values in mainfile:
        for i in range(len(values)):
            if i == 0:
                values[i] = int(values[i])

        print(values)
        