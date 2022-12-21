#!/usr/bin/python3

# TODO: 
# - Fachsemester Fehler Behandlung
# - Bestimmte Felder dürfen nicht leer bleiben

import tkinter as tk
from csv_editor import CSV_FILE

class Edit(tk.Frame):

    LABELS = ["Kuerzel:", "Name:", "Bereich:", "Fachsemester:", "Credit Points:", "Note:"]
    BUTTONS = ["Reset", "OK", "Abbrechen"]
    DATA = ["EMB", "Embedded Systems", "Eingebette Systeme", "4", "6", "2.1"]
    # DATA = []
    POSSIBLE_GRADES = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 4.3, 4.7, 5.0]

    def __init__(self, master=None, data=DATA):        # Master ist später das Main Fenster
        tk.Frame.__init__(self, master)
        self.data = data
        self.new_entries = []
        self.create_widgets()
        self.excset = {self.LABELS[i]: False for i in range(3,6)}
        # self.pack(expand=True, fill=tk.BOTH)


    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


    def save(self):
        for entry in self.entries.items():
            try:
                self.insert_data(entry)

            except EditException as msg:
                self.entries[str(msg)]["bg"] = "red"
                print(f"Fehler in der {str(msg)[:-1]} Eingabe")
                self.excset[str(msg)] = True
            
        if len(self.new_entries) < 6:
                self.new_entries.clear()
        else:
            print(self.new_entries)
            CSV_FILE.edit(self.data, self.new_entries)
            CSV_FILE.write()
            self._root().destroy()


    def insert_data(self, entry):
        if entry[0] == self.LABELS[4]:
            try:
                test = int(entry[1].get())
                self.new_entries.append(entry[1].get())
                if self.excset[self.LABELS[4]]:
                    self.excset[self.LABELS[4]] = False
                    self.entries[entry[0]]["bg"] = "white"
            except ValueError:
                raise EditException(entry[0])
        elif entry[0] == self.LABELS[5]:
            try:
                if float(entry[1].get()) in self.POSSIBLE_GRADES: 
                    self.new_entries.append(entry[1].get())
                else:
                    raise EditException(entry[0])
                if self.excset[self.LABELS[5]]:
                    self.excset[self.LABELS[5]] = False
                    self.entries[entry[0]]["bg"] = "white"
            except ValueError:
                raise EditException(entry[0])
        else:
            self.new_entries.append(entry[1].get())


    def insert_existing_data(self):
        if self.data != []:
            for i, entry in enumerate(self.entries.values()):
                entry.insert(0, self.data[i])


    def create_widgets(self):
        label_frame = tk.Frame(root, bg="lightblue")
        label_frame.pack(fill=tk.BOTH, expand=True)
        labels = [tk.Label(label_frame, bg="red", text=self.LABELS[i]) for i in range(6)]
        for i in range(6):
            labels[i].grid(row=i, column=0, sticky=tk.W+tk.E)

        self.entries = {self.LABELS[i]: tk.Entry(label_frame) for i in range(6)}
        self.insert_existing_data()
        for i, val in enumerate(self.entries.values()):
            val.grid(row=i, column=1, sticky=tk.W+tk.E)
        
        label_frame.columnconfigure(0,weight=1)
        label_frame.columnconfigure(1,weight=2)

        button_frame = tk.Frame(root, bg="blue")
        button_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)

        buttons = [tk.Button(button_frame, text=self.BUTTONS[i]) for i in range(3)]
        for i in range(3):
            buttons[i].grid(row=0, column=i, sticky=tk.E+tk.W)

        buttons[0]["command"] = self.reset
        buttons[1]["command"] = self.save
        buttons[2]["command"] = root.destroy

        button_frame.columnconfigure(0, weight=3)
        button_frame.columnconfigure(1, weight=4)
        button_frame.columnconfigure(2, weight=5)


class EditException(Exception):
    "Bei allen Fehlern der Edit Klasse geworfen"
    pass


if __name__ == '__main__':
    root = tk.Tk()
    main = Edit(root, CSV_FILE.data[0])
    root.mainloop()