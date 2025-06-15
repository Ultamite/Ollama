import ollama
import _sqlite3
from tkinter import scrolledtext, messagebox
from tkinter import *
import tkinter as tk

conn = _sqlite3.connect("chathistory.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    user_input TEXT,
    ai_response TEXT
)
""")
conn.commit()

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Code Reviewer")
        self.root.resizable(False, False)
        self.root.geometry("500x500")

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=25)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.input = Entry(root, width=40)
        self.input.grid(row=1, column=0, padx=10, pady=5)
        self.input.bind("<Return>", lambda event: self.chat_with_ai())

        self.generate_button = Button(root, text="Enter", command=self.chat_with_ai)
        self.generate_button.grid(row=1, column=1, padx=5, pady=5)

    def chat_with_ai(self):
        user_input = self.input.get().strip()

        if not user_input:
            messagebox.showwarning("Empty Input", "Please enter a message.")
            return

        model = "llama3.3:latest"

        c.execute("SELECT * FROM history")
        rows = c.fetchall()

        conversation_history = []
        for row in rows:
            conversation_history.append({"role": "user", "content": row[0]})
            conversation_history.append({"role": "assistant", "content": row[1]})

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = ollama.chat(model=model, messages=conversation_history)
            ai_reply = response["message"]["content"]
        except Exception as e:
            messagebox.showerror("AI Error", f"Failed to get response from model.\n\n{e}")
            return

        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "You: " + user_input + "\n")
        self.chat_display.insert(tk.END, "AI: " + ai_reply + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

        self.input.delete(0, tk.END)

        c.execute("INSERT INTO history VALUES (?, ?)", (user_input, ai_reply))
        conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
