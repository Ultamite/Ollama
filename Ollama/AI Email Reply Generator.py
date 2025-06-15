import tkinter as tk
from tkinter import ttk, messagebox
import ollama
import imaplib
import smtplib
import email
from email.header import decode_header
import ssl

ENABLE_EMAIL_INTEGRATION = False  

def generate_reply(email_text, tone):
    prompt = f"""
You are an AI trained to generate email replies.

Tone: {tone}
Original Email:
{email_text}

Reply:
"""
    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].strip()
    except Exception as e:
        return f"Error generating reply: {str(e)}"

def fetch_latest_email(username, password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        latest_email_id = data[0].split()[-1]
        result, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        message = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(message["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = message.get_payload(decode=True).decode()

        return f"Subject: {subject}\n\n{body}"
    except Exception as e:
        return f"Error fetching email: {str(e)}"

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Email Reply Generator")
        self.root.geometry("900x600")

        tk.Label(root, text="Received Email:", font=("Arial", 12, "bold")).pack()
        self.input_text = tk.Text(root, height=10, width=100)
        self.input_text.pack()

        tk.Label(root, text="Select Tone:", font=("Arial", 12)).pack(pady=(10, 0))
        self.tone = ttk.Combobox(root, values=["Formal", "Casual", "Apologetic", "Friendly", "Professional"])
        self.tone.current(0)
        self.tone.pack()

        tk.Button(root, text="Generate Reply", command=self.generate).pack(pady=10)

        tk.Label(root, text="Generated Reply:", font=("Arial", 12, "bold")).pack()
        self.output_text = tk.Text(root, height=10, width=100, bg="#f4f4f4")
        self.output_text.pack()

        if ENABLE_EMAIL_INTEGRATION:
            self.email_frame = tk.Frame(root)
            self.email_frame.pack(pady=10)
            tk.Label(self.email_frame, text="Email:").grid(row=0, column=0)
            tk.Label(self.email_frame, text="Password:").grid(row=1, column=0)
            self.email_entry = tk.Entry(self.email_frame, width=40)
            self.email_entry.grid(row=0, column=1)
            self.pass_entry = tk.Entry(self.email_frame, show="*", width=40)
            self.pass_entry.grid(row=1, column=1)
            tk.Button(self.email_frame, text="Fetch Latest Email", command=self.get_email).grid(row=0, column=2, rowspan=2, padx=10)

    def generate(self):
        text = self.input_text.get("1.0", tk.END).strip()
        tone = self.tone.get()
        if not text:
            messagebox.showwarning("Warning", "Please input the received email.")
            return
        response = generate_reply(text, tone)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, response)

    def get_email(self):
        email_ = self.email_entry.get()
        passwd = self.pass_entry.get()
        if not email_ or not passwd:
            messagebox.showwarning("Missing Info", "Enter your email credentials.")
            return
        fetched = fetch_latest_email(email_, passwd)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, fetched)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()
