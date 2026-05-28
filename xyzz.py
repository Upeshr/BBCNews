import tkinter as tk
import random

root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("450x500")
root.config(bg="#261e2f")

title = tk.Label(
    root,
    text="ROCK • PAPER • SCISSORS",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1e1e2f"
)
title.pack(pady=20)

result_label = tk.Label(
    root,
    text="Choose your move!",
    font=("Arial", 14),
    fg="white",
    bg="#1e1e2f"
)
result_label.pack(pady=20)

def play(user):
    choices = ["rock", "paper", "scissors"]
    computer = random.choice(choices)

    if user == computer:
        result_text = f"Tie! Computer chose {computer}"
        color = "yellow"

    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        result_text = f"You Win! Computer chose {computer}"
        color = "green"

    else:
        result_text = f"You Lose! Computer chose {computer}"
        color = "red"

    result_label.config(text=result_text, fg=color)

btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=30)

tk.Button(btn_frame, text=" ROCK", width=12, font=("Arial", 12, "bold"),
          bg="#444", fg="white", command=lambda: play("rock")).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text=" PAPER", width=12, font=("Arial", 12, "bold"),
          bg="#444", fg="white", command=lambda: play("paper")).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text=" SCISSORS", width=12, font=("Arial", 12, "bold"),
          bg="#444", fg="white", command=lambda: play("scissors")).grid(row=0, column=2, padx=10)

root.mainloop()