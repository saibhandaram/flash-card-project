from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
word_display = {}

# ---------------- importing data from Pandas----------------

try:
    base_words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    base_words = pandas.read_csv("data/french_words.csv")
    words_dict = base_words.to_dict(orient="records")
else:
    words_dict = base_words.to_dict(orient="records")


def change_card():
    global word_display, time_count
    window.after_cancel(time_count)
    word_display = random.choice(words_dict)
    canvas.itemconfig(title_word, text="French", fill="black")
    canvas.itemconfig(card_word, text=word_display['French'], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    time_count = window.after(3000, func=change_card)


# ------------ Button Click ---------------
def right_button_click():
    # remove item from csv
    global word_display
    words_dict.remove(word_display)
    df = pandas.DataFrame(words_dict)
    df.to_csv("data/words_to_learn.csv", index=False)
    change_card()


def wrong_button_click():
    # show answer
    global word_display, time_count
    window.after_cancel(time_count)
    canvas.itemconfig(title_word, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_display['English'], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
    time_count = window.after(3000, func=change_card)


# ---------------- Creating UI ----------------------------------

window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

time_count = window.after(3000, func=wrong_button_click)

canvas = Canvas(width=800, height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
title_word = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 250, text="", font=("Ariel", 80, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
right_button = Button(text="right", image=right_image, highlightthickness=0, command=right_button_click)
right_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(text="wrong", image=wrong_image, highlightthickness=0, command=wrong_button_click)
wrong_button.grid(column=1, row=1)

change_card()

window.mainloop()
