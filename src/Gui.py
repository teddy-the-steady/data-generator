# TODO in construction

import tkinter as tk
from tkinter import filedialog

class Gui(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title('SqlServer Data Generator')
        self.master.geometry('300x200')
        self.master.resizable(True, True)

        open_button = tk.Button(self.master, text='Open File', command=self.open_file_dialog)
        open_button.pack(padx=20, pady=20)

        open_button = tk.Button(self.master, text='Generate', command=self.gen_data)
        open_button.pack(padx=20, pady=50)

        selected_file_label = tk.Label(self.master, text='Selected File:')
        selected_file_label.pack()

        file_text = tk.Text(self.master, wrap=tk.WORD, height=10, width=40)
        file_text.pack(padx=20, pady=20)


    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title='Select a File', filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if file_path:
            self.selected_file_label.config(text=f'Selected File: {file_path}')
            self.process_file(file_path)


    def process_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.file_text.delete('1.0', tk.END)
                self.file_text.insert(tk.END, file_contents)
        except Exception as e:
            self.selected_file_label.config(text=f'Error: {str(e)}')


    def gen_data(self):
        self.selected_file_label.config(text='Gen btn clicked!')


if __name__ == '__main__':
    root = tk.Tk()
    app = Gui(master = root)
    app.mainloop()
