from tkinter import *
import sqlite3

root = Tk()
root.title('ToDo List')
root.geometry('500x500')

conn = sqlite3.connect('todo.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE if not exists todo(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
               description TEXT NOT NULL,
               completed BOOLEAN NOT NULL
    );           
""")

conn.commit()

def render_todos():
    rows = cursor.execute("SELECT * FROM todo").fetchall()
    print(rows)

    for i in range(0, len(rows)):
        completed = rows[i][3]
        description = rows[i][2]
        checkbtn = Checkbutton(frame, text=description, width=42, anchor='w')
        checkbtn.grid(row=i, column=0, sticky='w')


def addTodo():
    todo = entry.get()
    if todo:
        cursor.execute("""
                    INSERT INTO todo (description, completed) VALUES (?, ?)
                   """, (todo, False))
        conn.commit()
        entry.delete(0, END)
        render_todos()
    else:
        pass
    

label = Label(root, text='Tarea')
label.grid(row=0, column=0)

entry = Entry(root, width=40)
entry.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

entry.focus()

render_todos()

root.bind('<Return>', lambda x:addTodo())
root.mainloop()