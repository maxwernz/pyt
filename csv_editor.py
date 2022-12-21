#!/usr/bin/python3

# TODO: Sinnvolles open der Dateien

import csv
import os
import shutil

class CSV:
    """
    CSV Editor Klasse\n
    Speichert Daten einer CSV Datei als Liste von Listen\n
    """

    sort_key = {'krz': 0, 'name': 1, 'bereich': 2, 'fachsem': 3, 'cp': 4, 'note': 5}
    param_string = ['krz; name; bereich; fachsem; cp; note']
    path = ".datafiles"
    csv_data_len = 6

    def __init__(self, filename, key='krz'):
        self._filename = CSV.path + '/' + filename
        self._key = key

        file = open(filename, 'r')
        
        # Reader erzeugt eine gesplittete Liste mit Leerzeichen -> Strip für jeden String jedes Elements
        self._csv_data = [list(map(lambda s: s.strip(), lis)) for lis in list(csv.reader(file, delimiter=';'))[1:]]
        file.close()
        shutil.copy(filename, CSV.path)

            
    @property
    def data(self):
        "CSV Datei als Liste von Listen"
        return self._csv_data

    
    def __insert(self, lis: list):
        "Fügt einen neuen Eintrag(Liste von Strings) sortiert in die vorhandenen Daten ein"
        if lis not in self.data:
            self.data.append(lis)
            self.sort(self._key)


    def remove(self, lis: list):
        "Entfernt einen Eintrag aus den Daten"
        if type(lis) != list:
            raise CSVException("no list type")
        if len(lis) != CSV.csv_data_len:
            raise CSVException("list too short")
        self.data.remove(lis)

    
    def edit(self, index_lis: list, lis: list):
        "Ändert einen Eintrag in der Liste"
        if type(lis) != list or type(index_lis) != list:
            raise CSVException("no list type")
        if len(lis) != CSV.csv_data_len:
            raise CSVException("list too short")

        if index_lis == []:
            self.__insert(lis)
            return
        if len(index_lis) != CSV.csv_data_len:
            raise CSVException("list too short")
        
        self.data[self.data.index(index_lis)] = lis

         
    def write(self):
        "Schreibt die vorhandenen Daten neu in die CSV Datei"
        try:
            file = open(self._filename, 'w')
        except FileNotFoundError:
            file = open(self._filename, 'x')
        file.seek(0)
        self.sort('krz')
        csv_writer = csv.writer(file)
        csv_writer.writerow(CSV.param_string)
        for ele in self.data:
            csv_writer.writerow(["; ".join(ele)])


    def sort(self, key):
        "Sortiert die Daten nach angegebenem Schlüssel(Kürzel)"
        self._key = key
        self.data.sort(key=lambda lis: (lis[CSV.sort_key[self._key]], lis[0])) 


if not os.path.exists(CSV.path):
    os.mkdir(CSV.path)
        

class CSVException(Exception):
    "Wird bei allen Fehlern der CSV Klasse geworfen"
    pass


CSV_FILE = CSV("mtb_curriculum.csv")

if __name__ == '__main__':
    csv_file = CSV("mtb_curriculum.csv", 'fachsem')
    try:
        csv_file.edit(['MA1', 'Mathematik 1', 'Mathematik und Naturwissenschaften', '1', '5', '-'], ['MA1', 'Mathematik 1', 'Mathematik und Naturwissenschaften', '1', '5', '1.7'])
        csv_file.edit([], ['PYP', 'Python', 'Software', '4', '5', '-'])
        csv_file.write()
        print(csv_file.data)
    except CSVException:
        print("geht")