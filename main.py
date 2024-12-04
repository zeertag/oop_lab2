import csv
from xml.etree import ElementTree as ET
import time
import os


class InfoGetter:
    def __init__(self):
        self.file = None
        self.unique_info = {}
        self.houses = {}

    def check_file(self, file_name):
        if os.path.exists(file_name):
            self.file = file_name
            if file_name.endswith('.csv'):
                self.csv_read()
            elif file_name.endswith('.xml'):
                self.xml_read()
            else:
                return 2
        else:
            return 1
        return 3

    def get_data(self):
        if self.file.endswith('.csv'):
            self.csv_read()
        elif self.file.endswith('.xml'):
            self.xml_read()
        self.count_floors()

    def csv_read(self):
        with open(self.file, 'r', encoding="utf-8") as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=";")
            for row in reader:
                row_tuple = tuple(row)
                self.unique_info[row_tuple] = self.unique_info.get(row_tuple, 0) + 1

    def xml_read(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        for child in root.findall("item"):
            city, street, house, floor = child.get("city"), child.get("street"), child.get("house"), child.get("floor")
            row_tuple = (city, street, house, floor)
            self.unique_info[row_tuple] = self.unique_info.get(row_tuple, 0) + 1

    def count_floors(self):
        for i in self.unique_info:
            row_tuple = (i[0], i[3])
            self.houses[row_tuple] = self.houses.get(row_tuple, 0) + 1
        self.houses = dict(sorted(self.houses.items()))


class InfoPrinter:
    @staticmethod
    def print_unics(unique_info):
        for i in unique_info:
            print("Строка - ", *i, "\t|\tКоличетсво повторений: ", unique_info[i])

    @staticmethod
    def print_floors(houses):
        c = 0
        for i in houses:
            print(*i, " - ", houses[i])


class UserInteraction:
    @staticmethod
    def run():
        while True:
            while True:
                path = input("Введите имя файла: ")
                InfGet = InfoGetter()
                var = InfGet.check_file(path)
                if var == 1:
                    if len(path.strip()) == 0:
                        print("Введена пустая строка.")
                    elif "." not in path:
                        print("Название должно содержать формат файла! (Пример: 'name.csv').")
                    else:
                        print("Файла с таким названием не найдено.")
                if var == 2:
                    print("Программа не работает с таким типом файлов.")
                if var == 3:
                    print("Файл обработан успешно! Сейчас последует вывод на экран.")
                    break
                print("Попробуйте снова.\n")

            start_time = time.time()

            InfGet.get_data()
            InfPrint = InfoPrinter
            InfPrint.print_unics(InfGet.unique_info)
            InfPrint.print_floors(InfGet.houses)

            end_time = time.time()

            print(f"Время обработки файла: {end_time - start_time}\n")

            while True:
                ans = input("Продолжаем работу? (y/n): ")
                if ans == 'y':
                    print()
                    break
                elif ans == 'n':
                    print()
                    print("Программа завершила работу!")
                    exit()
                else:
                    print("\nОтвет введен некорректно.\n")


if __name__ == '__main__':
    UserInteraction.run()
