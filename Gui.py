# TODO in construction

import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        process_file(file_path)

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            file_text.delete('1.0', tk.END)
            file_text.insert(tk.END, file_contents)
    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")

root = tk.Tk()
root.title('SqlServer Data Generator')

root.geometry('300x200')
root.resizable(True,True)

open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack(padx=20, pady=20)

selected_file_label = tk.Label(root, text="Selected File:")
selected_file_label.pack()

file_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
file_text.pack(padx=20, pady=20)

root.mainloop()
