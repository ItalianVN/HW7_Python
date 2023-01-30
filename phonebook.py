import tkinter as tk
import sqlite3
import csv
import json
from tkinter import ttk, messagebox, filedialog

class PhoneBook(tk.Tk):
    def __init__(self, db_name):
        super().__init__()
        self.title('Телефонный справочник')
        self.phones_table = ttk.Treeview(self, selectmode='browse', show='headings',
            columns=('#1', '#2', '#3', '#4', '#5'))
        self.phones_table.heading('#1', text='#')
        self.phones_table.heading('#2', text='Фамилия')
        self.phones_table.heading('#3', text='Имя')
        self.phones_table.heading('#4', text='Телефон')
        self.phones_table.heading('#5', text='Описание')
        self.first_name_entry = ttk.Entry()
        self.last_name_entry = ttk.Entry()
        self.phone_number_entry = ttk.Entry()
        self.description_entry = ttk.Entry()
        self.import_button = ttk.Button(self, text="Импорт", command=self.import_file)
        self.export_button = ttk.Button(self, text="Экспорт", command=self.export_file)
        self.clear_button = ttk.Button(self, text="Очистить", command=self.clear_table)
        self.delete_button = ttk.Button(self, text="Удалить", command=self.delete_row)
        self.insert_button = ttk.Button(self, text="Вставить", command=self.insert_row)
        self.import_button.grid(row=0, column=0)
        self.export_button.grid(row=0, column=1)
        self.clear_button.grid(row=0, column=6)
        self.phones_table.grid(row=1, column=0, columnspan=7)
        self.last_name_entry.grid(row=2, column=0)
        self.first_name_entry.grid(row=2, column=1)
        self.phone_number_entry.grid(row=2, column=2)
        self.description_entry.grid(row=2, column=3)
        self.insert_button.grid(row=2, column=4)
        self.delete_button.grid(row=2, column=6)
        self.conn = sqlite3.connect(db_name)
        self.prepare_db()
        self.phones_table.bind("<<TreeviewSelect>>", self.item_selected)
    def item_selected(self, event):
        for selected_item in self.phones_table.selection():
            item = self.phones_table.item(selected_item)
            person = item['values']
            return person[0]
    def import_file(self):
        file_name = filedialog.askopenfilename()
        c = self.conn.cursor()
        if file_name.endswith('.csv'):
            with open(file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    c.execute('INSERT INTO book VALUES (null, ?, ?, ?, ?)', row)
        elif file_name.endswith('.json'):
            with open(file_name, 'r') as jsonfile:
                reader = json.load(jsonfile)
                data = []
                for row in reader['data']:
                    c.execute('INSERT INTO book VALUES (null, ?, ?, ?, ?)',
                        (row['last_name'], row['first_name'], row['phone_number'], row['description'])
                    )
        self.conn.commit()
        self.update_table()
    def export_file(self):
        c = self.conn.cursor()
        with open('C:\python\sem8\export.maf', 'w') as export_file:
            for row in c.execute('SELECT * FROM book'):
                export_file.write(row[1] + '\n')
                export_file.write(row[2] + '\n')
                export_file.write(row[3] + '\n')
                export_file.write(row[4] + '\n')
                export_file.write('\n')
    def prepare_db(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS book
            (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [last_name] TEXT,
                [first_name] TEXT,
                [phone_number] TEXT,
                [description] TEXT
            )
            ''')
        self.conn.commit()
    def clear_table(self):
        if not messagebox.askyesno(title='Очистить', message='Удалить ВСЕ записи?'):
            return
        self.phones_table.delete(*self.phones_table.get_children())
        c = self.conn.cursor()
        c.execute('DELETE FROM book')
        self.conn.commit()
        self.update_table()
    def insert_row(self):
        row = (
            self.first_name_entry.get(),
            self.last_name_entry.get(),
            self.phone_number_entry.get(),
            self.description_entry.get())
        c = self.conn.cursor()
        c.execute('INSERT INTO book VALUES (null, ?, ?, ?, ?)', row)
        self.conn.commit()
        self.update_table()
    def delete_row(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM book WHERE id = ?', (self.item_selected('<<TreeviewSelect>>'),))
        self.conn.commit()
        self.phones_table.delete(self.phones_table.selection())
    def update_table(self):
        self.phones_table.delete(*self.phones_table.get_children())
        c = self.conn.cursor()
        for row in c.execute('SELECT * FROM book'):
            self.phones_table.insert('', tk.END, values=row)

if __name__ == '__main__':
    phone_book = PhoneBook('C:\python\sem8\phonebook.db')
    phone_book.update_table()
    phone_book.mainloop()
