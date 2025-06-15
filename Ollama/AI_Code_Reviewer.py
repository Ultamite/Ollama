import ollama
from tkinter import scrolledtext, messagebox
from tkinter import *
import tkinter as tk

model = "deepseek-coder:latest"


#C:\Users\Architect\OneDrive\Documents\Coding and programing\Python\Apps\AI\AL-AN.py



class Window:
    def __init__(self,root):
        self.root = root
        self.root.title("AI Code Reviewer")
        self.root.resizable(False,False)
        self.root.geometry("450x400")

        self.filepath_var= StringVar()


        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD,state='disabled',width=50,height=20)
        self.chat_display.grid(row=0,column=0)

        self.file_path = Entry(root,width=25,textvariable=self.filepath_var)
        self.file_path.grid(row=1,column=0)

        self.generate_button = Button(root,text="Enter",command=self.generate_response)
        self.generate_button.grid(row=2,column=0)

    def generate_response(self):
        path = self.file_path.get()
        path = rf"{path}"

        f = open(rf"{path}")
        file = f.read()

        prompt = f"""
        You are an assistant that reviews code, suggests improvements, detects bugs, and estimate time complexity.

        Here is the code file {file}

        Please:

        1. Review the code
        2. Suggests improvements to the code
        3. Highlight and point out bugs in the code
        4. Estimate time complexity of the code
        """

        try:
            response = ollama.generate(model=model, prompt=prompt)
            generated_text = response.get("response","")
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END,generated_text)
            self.chat_display.config(state='disabled')

        except Exception as e:
            print("An error occured:",str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()

