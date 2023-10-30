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

def remove(id):
    def _remove():
        cursor.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        render_todos()

    return _remove

# Currying!
def complete(id):
    def _complete():
        todo = cursor.execute("SELECT * from todo WHERE id = ?", (id,)).fetchone()
        cursor.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()

    return _complete

def render_todos():
    rows = cursor.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else '#000000'
        checkbtn = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=complete(id))
        checkbtn.grid(row=i, column=0, sticky='w')
        eliminarbtn = Button(frame, text='Eliminar', command=remove(id))
        eliminarbtn.grid(row=i, column=1)
        checkbtn.select() if completed else checkbtn.deselect

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