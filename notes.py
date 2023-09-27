import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
import os
import glob

is_notes_mode = True

def load_todos():
    todo_file = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
    try:
        if os.path.exists(todo_file):
            with open(todo_file, 'r') as f:
                return f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load To-dos: {e}")
    return ""

def switch_to_notes(event=None):
    global is_notes_mode
    is_notes_mode = True
    text_area.pack_forget()
    note_area.pack(fill=tk.BOTH, expand=True)
    note_area.focus_set()

def switch_to_todos(event=None):
    global is_notes_mode
    is_notes_mode = False
    note_area.pack_forget()
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", load_todos())
    text_area.focus_set()

def save_content(event=None):
    global is_notes_mode
    try:
        content = note_area.get("1.0", tk.END).strip() if is_notes_mode else text_area.get("1.0", tk.END).strip()
        current_time = datetime.now().strftime("[%H:%M] ")

        if is_notes_mode:
            save_note(content, current_time)
        else:
            save_todo(content)

        messagebox.showinfo("Saved", f"Saved content successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

def save_note(content, current_time):
    filename = datetime.now().strftime("%m-%d-%y") + ".txt"
    full_path = os.path.join(os.path.expanduser("~/Notes"), filename)

    if not os.path.exists(full_path):
        write_header(full_path)
    with open(full_path, 'a') as f:
        f.write(current_time + content + "\n")

    note_area.delete("1.0", tk.END)

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

def save_todo(content):
    full_path = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
    with open(full_path, 'w') as f:
        f.write(content + "\n")

def toggle_mode(event=None):
    if is_notes_mode:
        switch_to_todos()
    else:
        switch_to_notes()

def close_program(event=None):
    root.quit()

# search all the notes in the directory with the format for notes files (based on date)
def aggregate_notes():
    note_dir = os.path.expanduser("~/Notes")
    note_files = glob.glob(os.path.join(note_dir, "*.txt"))
    aggregated_data = []

    for note_file in note_files:
        with open(note_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                timestamp = line.split(" ")[0]  # Assuming the timestamp is the first part of the line
                aggregated_data.append((note_file, timestamp, line.strip()))

    return aggregated_data


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

# tkinter setup
root = tk.Tk()
root.title("Note and To-do Taker")
root.geometry("750x750")
root.configure(bg='#211672')
root.attributes("-alpha", 0.9)

note_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#211672', fg='white', insertbackground='white')
note_area.pack(fill=tk.BOTH, expand=True)
text_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#211672', fg='white', insertbackground='white')
text_area.pack_forget()

# keyboard shortcuts
for area in [text_area, note_area]:
    area.bind('<Control-w>', close_program)
    area.bind('<Return>', save_content)
    area.bind('<Alt-t>', toggle_mode)
    area.bind('<Control-s>', save_content)
    area.bind('<Alt-Return>', lambda event, area=area: area.insert(tk.INSERT, '\n') or "break")
    area.bind('<Control-f>', show_search_box)

note_area.focus_set()

# a bar at the bottom that provides the keybinds
footnote = tk.Label(root, text="Keybinds: Ctrl-w: Quit | Ctrl-s: Save | Ctrl-f: Search | Return: Save | Alt-Return: New Line | Alt-t: Toggle Mode", bg="#211672", fg="white")

footnote.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
