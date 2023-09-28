import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
import os
import glob

# global variable to keep track of which mode is active, notes or todos
is_notes_mode = True

def load_todos():
    # todo file path, not the dog thats with a 't' smh
    todo_file = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
    try:
        # check for existing todo file
        if os.path.exists(todo_file):
            with open(todo_file, 'r') as f:
                return f.read()
    except Exception as e:
        # exception handling for loading errors
        messagebox.showerror("Error", f"Could not load To-dos: {e}")
    return ""

# switch to notes mode
def switch_to_notes(event=None):
    global is_notes_mode
    is_notes_mode = True
    text_area.pack_forget()
    note_area.pack(fill=tk.BOTH, expand=True)
    note_area.focus_set()

# switch to todo mode
def switch_to_todos(event=None):
    global is_notes_mode
    is_notes_mode = False
    note_area.pack_forget()
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", load_todos())
    text_area.focus_set()

# save the current content
def save_content(event=None):
    global is_notes_mode
    try:
        # grab the current content
        content = note_area.get("1.0", tk.END).strip() if is_notes_mode else text_area.get("1.0", tk.END).strip()
        current_time = datetime.now().strftime("[%H:%M] ")

        if is_notes_mode:
            save_note(content, current_time)
        else:
            save_todo(content)

        messagebox.showinfo("Saved", f"Saved content successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

# note saving
def save_note(content, current_time):
    filename = datetime.now().strftime("%m-%d-%y") + ".txt"
    full_path = os.path.join(os.path.expanduser("~/Notes"), filename)

    if not os.path.exists(full_path):
        write_header(full_path)
    with open(full_path, 'a') as f:
        f.write(current_time + content + "\n")

    note_area.delete("1.0", tk.END)

# my fancy header, the unicorn is named steve and he's chill
def write_header(full_path):
    ascii_art = '''
                                /
                           ,.. /
                         ,'   ';
              ,,.__    _,' /';  .
             :','  ~~~~    '. '~'
            :' (   )         )::,
            '; '~~~~~~~~~~~~ .;'
    '''
    header = f"------------------------------------------------\n{ascii_art}\n------------------------------------------------\n              Notes for {datetime.now().strftime('%m-%d-%y')}\n------------------------------------------------\n"
    with open(full_path, 'w') as f:
        f.write(header)

# save the todo list
def save_todo(content):
    full_path = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
    with open(full_path, 'w') as f:
        f.write(content + "\n")

# toggle between notes mode and todos mode
def toggle_mode(event=None):
    if is_notes_mode:
        switch_to_todos()
    else:
        switch_to_notes()

# quit it
def close_program(event=None):
    root.quit()

# aggregate all the notes in the directory
def aggregate_notes():
    note_dir = os.path.expanduser("~/Notes")
    note_files = glob.glob(os.path.join(note_dir, "*.txt"))
    aggregated_data = []

    for note_file in note_files:
        with open(note_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                timestamp = line.split(" ")[0]  # assuming the timestamp is the first part of the line
                aggregated_data.append((note_file, timestamp, line.strip()))

    return aggregated_data

# show a search box
def show_search_box(event=None):
    search_term = simpledialog.askstring("Search", "Enter the search term:")
    if search_term:
        all_notes = aggregate_notes()
        occurrences = 0
        found_in_files = []

        for filename, timestamp, line in all_notes:
            if search_term.lower() in line.lower():
                occurrences += 1
                found_in_files.append(f"Found in {filename} at {timestamp}")

        if occurrences > 0:
            detailed_info = "\n".join(found_in_files)
            messagebox.showinfo("Search Result", f"Found '{search_term}' {occurrences} times.\n{detailed_info}")
        else:
            messagebox.showinfo("Search Result", f"'{search_term}' not found.")

# tkinter settings
root = tk.Tk()
root.title("Note and To-do Taker")
root.geometry("750x750") # windows size
root.configure(bg='#211672') # background color, purple because obviously
root.attributes("-alpha", 0.9)

note_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#211672', fg='white', insertbackground='white')
note_area.pack(fill=tk.BOTH, expand=True)
text_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#211672', fg='white', insertbackground='white')
text_area.pack_forget()

# set up keyboard shortcuts
for area in [text_area, note_area]:
    area.bind('<Control-w>', close_program)
    area.bind('<Return>', save_content)
    area.bind('<Alt-t>', toggle_mode)
    area.bind('<Control-s>', save_content)
    area.bind('<Alt-Return>', lambda event, area=area: area.insert(tk.INSERT, '\n') or "break")
    area.bind('<Control-f>', show_search_box)

note_area.focus_set()

# bar on the bottom so I can remember the keybinds
footnote = tk.Label(root, text="Keybinds: Ctrl-w: Quit | Ctrl-s: Save | Ctrl-f: Search | Return: Save | Alt-Return: New Line | Alt-t: Toggle Mode", bg="#211672", fg="white")

footnote.pack(side=tk.BOTTOM, fill=tk.X)

# run the main loop, shocker I know
root.mainloop()
