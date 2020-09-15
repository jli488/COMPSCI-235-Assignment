import csv


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                print(f"Movie {index} with title: {title}, release year {release_year}")
                index += 1