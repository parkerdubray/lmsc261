import tkinter as tk
import json #json imported to create storage for tasks for the user to recall in later instances
import os  
from tkinter import ttk
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #creates file path and location for json file to be stored
task_file = os.path.join(BASE_DIR, "tasks.json") #names json file

#-----------------JSON-----------------#

# AI suggested using json file to store tasks between instances and provied some ways to integrate along these resources to learn when asked:
#  https://docs.python.org/3/library/json.html
#  https://www.geeksforgeeks.org/javascript/json/
def load_tasks(): #loads tasks json file at the start so the user can see tasks from previous instances of the program.
    global tasks
    try:
        with open(task_file, "r") as f:
            tasks = json.load(f)
        
        
    except FileNotFoundError:
        tasks = []


#---------------TKINTER---------------#

root = tk.Tk()

root.title("P-Assist")
root.geometry("750x450")

# ---------------- UI ---------------#
#Much of the tkinter knowlege used to create the UI was learned with the following sources:
#https://docs.python.org/3/library/tkinter.html#tkinter-modules
#https://youtu.be/ibf5cx221hk?si=nEXgfRUdAej7cORk
#https://youtu.be/6aKmTV6eYt8?si=P2m7ZZNyl2ow-nX3
#https://www.activestate.com/resources/quick-reads/how-to-position-widgets-in-tkinter/

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
#Source: https://www.geeksforgeeks.org/python/dropdown-menus-tkinter "Using ttk.combobox"used as resource to create prority dropdown and import ttk at start
options = ["low", "medium", "high", "urgent"]
priority_entry = ttk.Combobox(root, values= options, state="readonly") #ttk was imported at the start of code to add this combobox for priority entry
priority_entry.set("Select...")
priority_entry.place(relx=.73, y=80, anchor="center", relwidth=.15, height=40)


#List Legend
list_legend = tk.Label(root, text="# | Task | Date | Status")
list_legend.place(relx=0.5, rely=.4, anchor="center", relwidth=0.8, relheight=.075)

# List display
listbox = tk.Listbox(root, width=75, selectmode = tk.MULTIPLE)

listbox.place(relx=0.5, rely=.7, anchor="center", relwidth=0.8,relheight=0.5)

# ---------------- FUNCTIONS ---------------- #

def save_tasks(): #creates a save function to be recalled when information is added, changed, or removed. opens the json file and dumps new information
    with open(task_file, "w") as f:
        json.dump(tasks, f)

def add_task(event=None): #AI Assistance with formatting and troubleshooting
    task = task_entry.get().strip() #gets the users input from the task entry box
    due_date = date_entry.get().strip() #gets user input from date entry box
    etc = etc_entry.get().strip() #gets user input from ETC entry box
    priority = priority_entry.get().strip() #gets input from priority dropdown list


    if task == "":
        return

    tasks.append({"task": task, "done": False, "due": due_date, "etc": etc, "priority": priority})
    task_entry.delete(0, tk.END) # delete clears the input box after task has been added so that new information can be entered
    date_entry.delete(0,tk.END)
    etc_entry.delete(0,tk.END)
    priority_entry.delete(0,tk.END)

    save_tasks()
    update_list() 
#Binds Return Key to submit all task data
# Source: https://www.geeksforgeeks.org/python/python-binding-function-in-tkinter/
task_entry.bind("<Return>", add_task)
date_entry.bind("<Return>", add_task)
etc_entry.bind("<Return>", add_task)
priority_entry.bind("<Return>", add_task)


#Allows user to hide completed tasks so they dont clutter listbox
def toggle_completed():
    global show_completed
    show_completed = not show_completed
    update_list()

show_completed = False #False sets default to hide completed tasks
def get_visible_tasks(): #AI ASSISTED
    return [t for t in tasks if show_completed or not t["done"]]

def update_list(): #updates the list when new tasks are added, or the status of a task is changed
    listbox.delete(0, tk.END)

    visible_tasks = get_visible_tasks()

    for i, task in enumerate(visible_tasks): #Enumerate function learned from medium article by sarina nemati on building a python to-do list app https://medium.com/@sarinanemati/how-i-built-my-first-python-to-do-list-app-and-what-i-learned-ba5b75110ce6
        #AI assisted in integrating visible tasks function into the enumeration, so it only numerically lists visible tasks
        status = "Done" if task["done"] else "Not Done"
        due = task.get("due", "") # the second set of empty quotations accounts for no entry in the box, allowing the user to only add date, etc, and priority if they want
        etc = task.get("etc", "")
        priority = task.get("priority", "") 

        parts = [f"{i+1}. {task.get('task')}"] # AI assisted in the code to seperate each part of task and then add them at the end to allow for no input for some boxes
        if due:
            parts.append(f"Due: {due}") 
        if etc:
            parts.append(f"ETC: {etc}")
        if priority:
            parts.append(f"Priority: {priority}")
        parts.append(status)
        display = " | ".join(parts) #Joins all individual parts at the end to create a uniform task, allowing the other boxes to be optional
        
        listbox.insert(tk.END, display)

def mark_done(event=None):
    try:
        selected_indices = listbox.curselection() #creates a variable containing items selected by cursor so we can apply to all
        visible_tasks = get_visible_tasks() 

        for index in selected_indices:

             visible_tasks[index]["done"] = not visible_tasks[index]["done"] #second half allows the user to change tasks marked as done to not done if a mistake was made
            
        save_tasks()
        update_list()
    
    except IndexError:
        pass
listbox.bind("<Return>", mark_done) #binds Return key to toggling done/not done when there is a selection in the listbox


def delete_task(event=None): #delete function allows user to remove tasks that are incomplete or complete if the user decides they do not need them anymore
    #partially learned from user aran-fey on a stack overflow about removing items from arrays in addition to modifiyng original mark done function 
    #https://stackoverflow.com/questions/7118276/how-to-remove-specific-element-from-an-array-using-python
    try:

        selected_indecies = listbox.curselection() #selected indecies variable allows for the selection of multiple tasks just like the toggle done function
        visible_tasks = get_visible_tasks()

        for index in reversed(selected_indecies):
        
             tasks_to_delete = visible_tasks[index]
             tasks.remove(tasks_to_delete)
             
        save_tasks()
        update_list()
    
    except IndexError:
        pass

listbox.bind("<BackSpace>", delete_task) #Binds Backspace to removing tasks from the list

# ---------------- BUTTONS ---------------- #
#Source: https://docs.python.org/3/library/tkinter.html#tkinter-modules
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.place(relx=0.875, y=80, anchor="center")

done_button = tk.Button(root, text="Toggle Done", command=mark_done)
done_button.place(relx=0.5125, rely=.3, anchor="center")

show_completed_button = tk.Button(root, text= "Show/Hide Completed Tasks", command=toggle_completed)
show_completed_button.place(relx=0.75, rely=0.3, anchor="center")

delete_button = tk.Button(root, text= "Remove", command=delete_task)
delete_button.place(relx= 0.3555, rely= .3, anchor="center")




load_tasks()
update_list()

root.mainloop()

