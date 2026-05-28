import tkinter as tk
import random

def play(user):
    choices = ("rock", "scissors", "paper")
    computer = random.choice(choices)
    if user == computer:
        result = "Its a tie!"
        

    elif (user == "rock" and computer == "scissors") or (user == "paper" and computer == "rock") or (user == "scissors" and computer == "paper"):
        result = " You Win! "

    else:
        result = " You Lose!"
    
    result_label.config(text = f"computer: {computer}\n{result}")
    
root = tk.Tk()
root.title(" --ROCK--PAPER--SCISSORS")
root.geometry("400x400")

title_label = tk.Label(root, text = " ---CHOOSE-ROCK-PAPER-OR-SCISSORS---")
title_label.pack(padx = 20)

btn_rock = tk.Button(root, text = "rock")
btn_paper = tk.Button(root, text = "paper")
btn_scissors = tk.Button(root, text = "scissors")

btn_rock.config(command = lambda: play("rock"))
btn_paper.config(command = lambda: play("paper"))
btn_scissors.config(command = lambda: play("scissors"))

btn_rock.pack(padx = 5)
btn_paper.pack(padx = 5)
btn_scissors.pack(padx = 5)

result_label = tk.Label(root, text = "")
result_label.pack(padx = 20)

root.mainloop()   
