import csv

with open('./review_info_cleaned.csv', 'r') as file, open('./review_info_cleaned_2.csv', 'w') as file2:
    csv_reader = csv.reader(file, delimiter='~')
    for row in csv_reader:
      date = row[2].split()
      if len(date) == 3:
        day = date[1].rstrip(',')
        year = date[2]
        match date[0]:
          case 'Jan':
              month = '01'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Feb':
              month = '02'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Mar':
              month = '03'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Apr':
              month = '04'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'May':
              month = '05'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Jun':
              month = '06'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Jul':
              month = '07'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Aug':
              month = '08'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Sep':
              month = '09'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Oct':
              month = '10'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Nov':
              month = '11'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case 'Dec':
              month = '12'
              file2.write(f'\n{row[0]}~{row[1]}~{year}-{month}-{day}~{row[3]}')
          case _:
              file2.write(f'\n{row[0]}~{row[1]}~~{row[3]}')
      else:
        file2.write(f'\n{row[0]}~{row[1]}~~{row[3]}')