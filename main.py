from tkinter import *
import pandas
import random
from tkinter import messagebox
from pygame import mixer

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
        window.quit()
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
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()
window.minsize(width=screen_width, height=screen_height)

# Background
# TODO: 2. Handle end of words situation with some animation
background = Canvas(window, width=1728, height=1117, highlightthickness=0)
background_image = PhotoImage(file="images/beach1.png")
background.create_image(0, 0, image=background_image, anchor=NW)
background.place(x=0, y=0)

# Flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0)
flashcard_front = PhotoImage(file="images/white_square.png")
flashcard_back = PhotoImage(file="images/black_square.png")
card_image = canvas.create_image(400, 263)
card_language = canvas.create_text(400, 115, font=(FONT_NAME, 40, "italic"))
card_transcription = canvas.create_text(400, 175, font=(FONT_NAME, 30, "normal"))
card_word = canvas.create_text(400, 263, font=(FONT_NAME, 80, "bold"), width=800)
canvas.place(x=464, y=150)

# Correct button
correct_icon = PhotoImage(file="images/correct_button.png")
correct_button = Button(image=correct_icon, width=95, height=95, highlightthickness=0, command=remove_learnt_card)
correct_button.place(x=564, y=750)

# Wrong button
wrong_icon = PhotoImage(file="images/wrong_button.png")
wrong_button = Button(image=wrong_icon, width=95, height=95, highlightthickness=0, command=show_next_card)
wrong_button.place(x=1064, y=750)

# ---------------------------------- PLAY SOUND ---------------------------------- #

mixer.init()
sound = mixer.Sound("sounds/ocean_waves.mp3")
sound.play(loops=-1)
show_next_card()

window.mainloop()
