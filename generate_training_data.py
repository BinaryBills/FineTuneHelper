#Author: BinaryBills
#Creation Date: August 23, 2023
#Date Modified: September 11, 2023
#Purpose: Generates training data into the proper JSONL format that can get passed into the OpenAI API.
import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json

class UM_Dearborn_DB_GUI:
    def __init__(self, root):
        self.db_name = "um_dearborn_data.db"
        self._initialize_db()

        #Main frame
        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        #Display dialogues
        self.listbox = tk.Listbox(self.mainframe, height=40, width=275)
        self.listbox.grid(column=0, row=0, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._load_dialogues()
        
        #Add and delete buttons
        ttk.Button(self.mainframe, text="Add Dialogue", command=self.add_dialogue).grid(column=1, row=0, sticky=(tk.W, tk.E))
        ttk.Button(self.mainframe, text="Delete Dialogue", command=self.delete_dialogue).grid(column=1, row=1, sticky=(tk.W, tk.E))
        ttk.Button(self.mainframe, text="Exit", command=root.quit).grid(column=1, row=2, sticky=(tk.W, tk.E))
        ttk.Button(self.mainframe, text="Generate JSONL", command=self.generate_jsonl).grid(column=1, row=4, sticky=(tk.W, tk.E))

        #Padding
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def _initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dialogues (
                    id INTEGER PRIMARY KEY,
                    user_message TEXT NOT NULL,
                    assistant_message TEXT NOT NULL
                )
            """)
            conn.commit()

    def _load_dialogues(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_message, assistant_message FROM dialogues")
            rows = cursor.fetchall()
            for row in rows:
                item_id, user_msg, assistant_msg = row
                self.listbox.insert(tk.END, f"ID: {item_id} | User: {user_msg} | Assistant: {assistant_msg}")

    def add_dialogue(self):
        user_message = simpledialog.askstring("Input", "Enter user message:")
        if user_message:
            # Check if user_msg already exists in the database (case-insensitive)
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM dialogues WHERE UPPER(user_message) = UPPER(?)", (user_message,))
                existing_message = cursor.fetchone()

                if existing_message:
                    messagebox.showerror("Error", "This message already exists in the database!")
                    return

                assistant_message = simpledialog.askstring("Input", "Enter assistant's response:")
                cursor.execute("INSERT INTO dialogues (user_message, assistant_message) VALUES (?, ?)", (user_message, assistant_message))
                conn.commit()

            self.listbox.insert(tk.END, f"User: {user_message} | Assistant: {assistant_message}")

#Checks if the user's message already exists in the database, and if it does, an error is shown and the function returns early.

    def delete_dialogue(self):
        try:
            index = self.listbox.curselection()[0]
            item = self.listbox.get(index)
            item_id = int(item.split("|")[0].split(":")[1].strip())
            
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM dialogues WHERE id = ?", (item_id,))
                conn.commit()
                
            self.listbox.delete(index)
        except IndexError:
            messagebox.showerror("Error", "No dialogue selected.")
            
            
    def generate_jsonl(self):
        dialogues = []
        system_message = {
            "role": "system",
            "content": "You are a wise and polite AI assistant, speaking like Master Yoda, and knowledgeable about the University of Michigan-Dearborn, ending every response with 'my young padawan.'"
        }
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_message, assistant_message FROM dialogues")
            rows = cursor.fetchall()
            for row in rows:
                user_msg, assistant_msg = row
                dialogues.append([
                    system_message,
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg}
                ])
        with open("um_dearborn_data.jsonl", 'w') as f:
            for dialogue in dialogues:
                formatted_data = json.dumps({"messages": dialogue})
                f.write(formatted_data + '\n')
        messagebox.showinfo("Info", "JSONL file generated successfully!")


#Create the main application window
root = tk.Tk()
root.title("UM-Dearborn Training Data GUI with Database")

app = UM_Dearborn_DB_GUI(root)
root.geometry("1920x1080")
root.mainloop()
