import tkinter as tk
import json
import os  
import datetime as dt
from tkinter import ttk
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
task_file = os.path.join(BASE_DIR, "tasks.json")

tasks = []
#-----------------JSON-----------------#


def load_tasks():
    global tasks
    try:
        with open(task_file, "r") as f:
            tasks = json.load(f)
        
        for task in tasks:
            if "due" not in task:
                task["due"] = ""
    except FileNotFoundError:
        tasks = []


#---------------TKINTER---------------#

root = tk.Tk()
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))

root.title("P-Assist")
root.geometry("750x450")

# ---------------- UI ---------------#

title = tk.Label(root, text="P-Assist", font=("Arial", 24))
title.pack(fill="x", padx=10, pady=5)

task_box = tk.Label(root, text= "Task", font=("Arial", 18))
task_box.place(relx=0.3, y=50, anchor="center")

date_box = tk.Label(root, text= "Date",font=("Arial", 18))
date_box.place(relx=0.5, y=50, anchor="center")

etc_box = tk.Label(root, text= "ETC",font=("Arial", 18))
etc_box.place(relx=0.6, y=50, anchor="center")

priority_box = tk.Label(root,text= "Priority",font=("Arial", 18))
priority_box.place(relx=0.73, y=50, anchor="center")


# Task Entry box
task_entry = tk.Entry(root, width=30)
task_entry.place(relx=0.3, y=80, anchor="center" ,relwidth=0.4, height="40")

# Task Date Box
date_entry = tk.Entry(root, width=15)
date_entry.place(relx=0.5, y=80, anchor="center" , relwidth=0.1, height=40)

#ETC Box
etc_entry = tk.Entry(root, width=15)
etc_entry.place(relx=0.6, y=80, anchor="center" , relwidth=0.1, height=40)

#Priority Box
options = ["low", "medium", "high", "urgent"]
priority_entry = ttk.Combobox(root, values= options, state="readonly")
priority_entry.set("Select...")
priority_entry.place(relx=.73, y=80, anchor="center", relwidth=.15, height=40)


#List Legend
list_legend = tk.Label(root, text="# | Task | Date | Status")
list_legend.place(relx=0.5, rely=.4, anchor="center", relwidth=0.8, relheight=.075)

# List display
listbox = tk.Listbox(root, width=75)
listbox.place(relx=0.5, rely=.7, anchor="center", relwidth=0.8,relheight=0.5)

# ---------------- FUNCTIONS ---------------- #

def save_tasks():
    with open(task_file, "w") as f:
        json.dump(tasks, f)

def add_task(event=None):
    task = task_entry.get().strip()
    due_date = date_entry.get().strip()
    etc = etc_entry.get().strip()
    priority = priority_entry.get().strip()


    if task == "":
        return

    tasks.append({"task": task, "done": False, "due": due_date, "etc": etc, "priority": priority})
    task_entry.delete(0, tk.END)
    date_entry.delete(0,tk.END)
    etc_entry.delete(0,tk.END)
    priority_entry.delete(0,tk.END)

    save_tasks()
    update_list()
task_entry.bind("<Return>", add_task)
date_entry.bind("<Return>", add_task)
etc_entry.bind("<Return>", add_task)
priority_entry.bind("<Return>", add_task)

def toggle_completed():
    global show_completed
    show_completed = not show_completed
    update_list()

show_completed = False
def get_visible_tasks():
    return [t for t in tasks if show_completed or not t["done"]]

def update_list():
    listbox.delete(0, tk.END)

    visible_tasks = get_visible_tasks()

    for i, task in enumerate(visible_tasks):
        status = "Done" if task["done"] else "Not Done"
        due = task.get("due", "")
        etc = task.get("etc", "")
        priority = task.get("priority", "") 

        parts = [f"{i+1}. {task.get('task', 'Untitled')}"]
        if due:
            parts.append(f"Due: {due}")
        if etc:
            parts.append(f"ETC: {etc}")
        if priority:
            parts.append(f"Priority: {priority}")
        parts.append(status)
        display = " | ".join(parts)
        
        listbox.insert(tk.END, display)

def mark_done():
    try:
        index = listbox.curselection()[0]
        visible_tasks = get_visible_tasks()

        visible_tasks[index]["done"] = True
        save_tasks()
        update_list()
    
    except IndexError:
        pass



# ---------------- BUTTONS ---------------- #

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.place(relx=0.875, y=80, anchor="center")

done_button = tk.Button(root, text="Mark Done", command=mark_done)
done_button.place(relx=0.525, rely=.3, anchor="center")



show_completed_button = tk.Button(root, text= "Show/Hide Completed Tasks", command= toggle_completed)
show_completed_button.place(relx=0.75, rely=0.3, anchor="center")


load_tasks()
update_list()

root.mainloop()

