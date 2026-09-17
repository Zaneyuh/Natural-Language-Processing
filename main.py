import tkinter as tk
from tkinter import scrolledtext
import threading

from cebuanodoc_models import (
    translate_to_english,
    get_medical_response,
    translate_to_cebuano,
)


def process_message(query):
    try:
        english = translate_to_english(query)
        medical = get_medical_response(english)
        cebuano = translate_to_cebuano(medical)

        root.after(0, show_response, cebuano)

    except Exception as e:
        root.after(0, show_response, f"Error: {e}")


def send_message(event=None):
    query = input_box.get().strip()

    if not query:
        return

    chat.config(state="normal")
    chat.insert(tk.END, "Ikaw\n", "user_name")
    chat.insert(tk.END, query + "\n\n")

    chat.insert(tk.END, "Cebuano Doctor\n", "doctor_name")
    chat.insert(tk.END, "Naghunahuna...\n\n", "loading")

    chat.config(state="disabled")
    chat.see(tk.END)

    input_box.delete(0, tk.END)
    send_button.config(state="disabled")

    threading.Thread(
        target=process_message,
        args=(query,),
        daemon=True
    ).start()


def show_response(response):
    chat.config(state="normal")

    start = chat.search("Naghunahuna...", "1.0", tk.END)

    if start:
        end = f"{start}+{len('Naghunahuna...')}c"
        chat.delete(start, end)

    chat.insert(tk.END, response + "\n\n")

    chat.config(state="disabled")
    chat.see(tk.END)

    send_button.config(state="normal")
    input_box.focus()


root = tk.Tk()
root.title("Cebuano Doctor")
root.geometry("700x600")
root.configure(bg="#f6f7f9")


header = tk.Frame(root, bg="#f6f7f9")
header.pack(fill="x", padx=30, pady=(25, 15))

tk.Label(
    header,
    text="Cebuano Doctor",
    font=("Segoe UI", 22, "bold"),
    bg="#f6f7f9",
    fg="#1f2937"
).pack(anchor="w")

tk.Label(
    header,
    text="Pangutana bahin sa imong panglawas sa Cebuano.",
    font=("Segoe UI", 10),
    bg="#f6f7f9",
    fg="#6b7280"
).pack(anchor="w", pady=(4, 0))


input_frame = tk.Frame(root, bg="#f6f7f9")
input_frame.pack(side="bottom", fill="x", padx=30, pady=(10, 25))

disclaimer = tk.Label(
    input_frame,
    text="Educational use only • Dili kapuli sa tambag sa doktor.",
    font=("Segoe UI", 8),
    bg="#f6f7f9",
    fg="#6b7280"
)
disclaimer.pack(anchor="w", pady=(8, 0))

entry_frame = tk.Frame(input_frame, bg="#f6f7f9")
entry_frame.pack(fill="x")

input_box = tk.Entry(
    entry_frame,
    font=("Segoe UI", 11),
    relief="solid",
    borderwidth=1
)
input_box.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=9
)

send_button = tk.Button(
    entry_frame,
    text="Send",
    font=("Segoe UI", 10, "bold"),
    command=send_message,
    padx=18,
    pady=7
)
send_button.pack(side="right", padx=(10, 0))

chat = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="white",
    fg="#1f2937",
    relief="solid",
    borderwidth=1,
    padx=15,
    pady=15
)

chat.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 5)
)

chat.tag_config(
    "user_name",
    font=("Segoe UI", 10, "bold"),
    foreground="#2563eb"
)

chat.tag_config(
    "doctor_name",
    font=("Segoe UI", 10, "bold"),
    foreground="#15803d"
)

chat.tag_config(
    "loading",
    foreground="#6b7280"
)

chat.config(state="disabled")

input_box.bind("<Return>", send_message)

input_box.focus()

root.mainloop()