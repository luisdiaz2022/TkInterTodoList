from tkinter import *
import sqlite3

root = Tk()
root.title('ToDo List')
root.geometry('500x500')

conn = sqlite3.connect('todo.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE if not exists todo(
               id INTERGET PRIMARY GEY AUTOINCREMENT,
               created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
               description TEXT NOT NULL,
               completed BOOLEAN NOT NULL
    );           
""")

conn.commit()