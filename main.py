from tkinter import *
import pandas
import random
from tkinter import messagebox

# Constants
BACKGROUND_COLOR = "#004A65"
FONT_NAME = "Arial"
timer = None
cards_to_learn = {}
current_card = {}


# ---------------------------------- CHANGE CARD ---------------------------------- #
def show_next_card():
    """Show next card with foreign word."""
    global timer, current_card
    if len(cards_to_learn) == 0:
        if timer is not None:
            window.after_cancel(timer)
        all_words_learnt()
    else:
        if timer is not None:
            window.after_cancel(timer)
        current_card = random.choice(cards_to_learn)
        canvas.itemconfig(card_image, image=flashcard_front)
        canvas.itemconfig(card_language, text="Chinese", fill="black")
        canvas.itemconfig(card_transcription, text=current_card["Pinyin"], fill="black")
        canvas.itemconfig(card_word, text=current_card["Chinese"], fill="black")
        timer = window.after(3000, flip_card, current_card)


def remove_learnt_card():
    """Remove learnt card from words_to_learn file"""
    global current_card
    if current_card in cards_to_learn:
        cards_to_learn.remove(current_card)
        words_to_learn = pandas.DataFrame(cards_to_learn)
        words_to_learn.to_csv("data/words_to_learn.csv", index=False)
        show_next_card()


def all_words_learnt():
    """Show message that all words have been learnt"""
    messagebox.showinfo(message="Congratulations!!! You have learnt all the words!")


# ---------------------------------- SHOW TRANSLATION ---------------------------------- #
def flip_card(card):
    """Flip current card and show translation"""
    canvas.itemconfig(card_image, image=flashcard_back)
    canvas.itemconfig(card_language, text="English", fill="white")
    canvas.itemconfig(card_transcription, text="")
    canvas.itemconfig(card_word, text=card["English"], fill="white")


# ---------------------------------- READ FILE ---------------------------------- #
try:
    remaining_cards = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    all_cards = pandas.read_csv("data/chinese_hsk1.csv")
    cards_to_learn = all_cards.to_dict(orient="records")
except pandas.errors.EmptyDataError:
    all_words_learnt()
    exit()
else:
    cards_to_learn = remaining_cards.to_dict(orient="records")


# ---------------------------------- UI SETUP ---------------------------------- #
# Window set up
window = Tk()
window.title("Learn Chinese with Flashcards!")
window.config(bg=BACKGROUND_COLOR, pady=100, padx=200)

# Background
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

# TODO: 1. Add background image and make the window full screen
# TODO: 2. Handle end of words with some animation
# background = Canvas(width=screen_width, height=screen_height, highlightthickness=0)
# # background_image = PhotoImage(file="...")
# background.grid(row=0, column=0, columnspan=2, rowspan=2)

# Flashcard
canvas = Canvas(width=824, height=550, highlightthickness=0, bg=BACKGROUND_COLOR)
flashcard_front = PhotoImage(file="images/white_card.png")
flashcard_back = PhotoImage(file="images/black_card.png")
card_image = canvas.create_image(412, 275)
card_language = canvas.create_text(400, 115, font=(FONT_NAME, 40, "italic"))
card_transcription = canvas.create_text(400, 175, font=(FONT_NAME, 30, "normal"))
card_word = canvas.create_text(400, 263, font=(FONT_NAME, 80, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Correct button
correct_icon = PhotoImage(file="images/correct_button.png")
correct_button = Button(image=correct_icon, width=95, height=95, highlightthickness=0, command=remove_learnt_card)
correct_button.grid(row=1, column=1)

# Wrong button
wrong_icon = PhotoImage(file="images/wrong_button.png")
wrong_button = Button(image=wrong_icon, width=95, height=95, highlightthickness=0, command=show_next_card)
wrong_button.grid(row=1, column=0)

show_next_card()

window.mainloop()
