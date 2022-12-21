#!/usr/bin/python3
import csv_editor
from csv_editor import CSV

# with open("test.csv", 'r+') as csvfile:
#     data = list(csv.reader(csvfile))
#     csvfile.seek(0)

#     data.append(['PYP; Programmierung in Python; Softwaretechnik; 4; 5'])

#     csv_writer = csv.writer(csvfile, dialect='excel')
#     for line in data:
#         csv_writer.writerow(line)





csv_file = CSV("test.csv")
print(csv_file.data)
try:
    csv_file.insert(['a'])
except csv_editor.CSVException:
    print("geht")