# TODO in construction

import tkinter as tk
from tkinter import filedialog

class Gui(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title('SqlServer Data Generator')
        self.master.geometry('300x200')
        self.master.resizable(True, True)

        # empty rows
        self.empty_row0 = tk.Label(self.master, text = '')
        self.empty_row0.grid(row = 0, column = 0)

        self.empty_row2 = tk.Label(self.master, text = '')
        self.empty_row2.grid(row = 2, column = 0)

        # file row (row=1)
        self.file_info = tk.Label(self.master, text = 'File:')
        self.file_entry = tk.Entry(self.master, width = 20)
        self.open_button = tk.Button(self.master, text='Open', command=self.open_file_dialog)

        self.file_info.grid(row = 1, column = 0)
        self.file_entry.grid(row = 1, column = 1, sticky=tk.EW)
        self.open_button.grid(row = 1, column = 2)

        self.master.grid_rowconfigure(1, minsize=10)
        self.master.grid_columnconfigure(0, pad=30)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, pad=30)

        # gen button row (row=3)
        self.gen_button = tk.Button(self.master, text='Generate', command=self.gen_data)
        self.gen_button.grid(row = 3, column = 2)


    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title='Select a File', filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if file_path:
            self.file_entry.insert(tk.END, file_path)


    def gen_data(self):
        self.file_entry.insert(tk.END, 'Gen btn clicked!')


if __name__ == '__main__':
    root = tk.Tk()
    app = Gui(master = root)
    app.mainloop()
