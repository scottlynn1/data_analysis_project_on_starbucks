import csv

file = open('./review_info_cleaned_copy.csv', mode='r')
file2 = open('./review_info_cleaned_2.csv', mode='a')

csv_reader = csv.reader(file, delimiter='~')
for row in csv_reader:
  items = row[0].split()
  for item in items:
    if len(item) == 2:
      file2.write(f'\n{item}~{row[1]}~{row[2]}~{row[3]}')
file.close()
file2.close()