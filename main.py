import sys
from tkinter import *
import pandas
import random
from pygame import mixer


class FlashcardApp:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Learn Chinese with Flashcards!")
        self.tk.attributes('-fullscreen', True)
        self.tk.bind("<Escape>", self.exit)
        self.tk.bind("<space>", self.mute)
        self.font = "Arial"
        self.timer = None
        self.cards_to_learn = {}
        self.current_card = {}

        self.setup_ui()
        self.tk.after(3000, self.get_data)
        self.tk.after(3000, self.load_card_text)

        mixer.init()
        self.ocean_sound = mixer.Sound("sounds/ocean_waves.mp3")
        self.ocean_sound.play(loops=-1)

        self.tk.mainloop()

    def exit(self, event):
        """Close window when 'escape' is pressed."""
        self.tk.destroy()

    def mute(self, event):
        """Mute sound when 'space' is pressed."""
        self.ocean_sound.stop()

    def setup_ui(self):
        """Set up UI."""
        self.tk.grid_columnconfigure(0, weight=1)
        self.tk.grid_rowconfigure(0, weight=1)

        self.main = Frame(self.tk)
        self.main.grid_rowconfigure(0, weight=1, uniform="True")
        self.main.grid_rowconfigure(1, weight=5, uniform="True")
        self.main.grid_rowconfigure(2, weight=1, uniform="True")
        self.main.grid_rowconfigure(3, weight=1, uniform="True")
        self.main.grid_rowconfigure(4, weight=1, uniform="True")
        for x in range(16):
            self.main.grid_columnconfigure(x, weight=1)
        self.main.grid(row=0, column=0, sticky="nsew")

        self.background = Canvas(self.main, highlightthickness=0, bg="green")
        self.background.grid(row=0, column=0, rowspan=5, columnspan=16, sticky="nsew")

        self.background_image = PhotoImage(file="images/beach1.png")
        self.background.create_image(0, 0, image=self.background_image, anchor=NW)

        self.card = Canvas(self.main, bg="white", highlightthickness=0)
        self.card.grid(row=1, column=5, columnspan=6, sticky="nsew")

        self.correct_icon = PhotoImage(file="images/correct_button.png")
        self.correct_button = Button(self.main, image=self.correct_icon, highlightthickness=0,
                                     command=self.remove_learnt_card)
        self.correct_button.grid(row=3, column=5)

        self.wrong_icon = PhotoImage(file="images/wrong_button.png")
        self.wrong_button = Button(self.main, image=self.wrong_icon, highlightthickness=0, command=self.show_next_card)
        self.wrong_button.grid(row=3, column=10)

        self.loader = Label(self.main,
                            text="Press 'esc' to quit,\n 'space' to mute",
                            font=(self.font, 30),
                            bg="white",
                            fg="black")
        self.loader.grid(row=1, column=5, columnspan=6, sticky="nsew")

    def load_card_text(self):
        """Load correct text position and display text on card."""
        self.loader.grid_forget()  # Hide the loader

        canvas_width = self.card.winfo_width()
        canvas_height = self.card.winfo_height()
        center_x = canvas_width // 2
        self.card_language = self.card.create_text(center_x, canvas_height // 7,
                                                   font=(self.font, 40, "italic"),
                                                   fill="black")
        self.card_transcription = self.card.create_text(center_x, canvas_height // 4,
                                                        font=(self.font, 30, "normal"),
                                                        fill="black")
        self.card_word = self.card.create_text(center_x, canvas_height // 2,
                                               font=(self.font, 140, "bold"),
                                               fill="black")
        self.show_next_card()

    def get_data(self):
        """Load foreign words from file."""
        try:
            remaining_cards = pandas.read_csv("data/words_to_learn.csv")
        except FileNotFoundError:

            all_cards = pandas.read_csv("data/chinese_hsk1.csv")
            self.cards_to_learn = all_cards.to_dict(orient="records")
        except pandas.errors.EmptyDataError:
            self.all_words_learnt()
        else:
            self.cards_to_learn = remaining_cards.to_dict(orient="records")

    def show_next_card(self):
        """Show next card with foreign word."""
        if len(self.cards_to_learn) == 0:
            if self.timer is not None:
                self.tk.after_cancel(self.timer)
            self.all_words_learnt()

        else:
            if self.timer is not None:
                self.tk.after_cancel(self.timer)
            self.current_card = random.choice(self.cards_to_learn)
            self.card.config(bg="white")
            self.card.itemconfig(self.card_language,
                                 text="Chinese",
                                 fill="black")
            self.card.itemconfig(self.card_transcription,
                                 text=self.current_card["Pinyin"],
                                 fill="black")
            self.card.itemconfig(self.card_word,
                                 text=self.current_card["Chinese"],
                                 font=(self.font, 160, "bold"),
                                 fill="black")
            self.timer = self.tk.after(3000, self.flip_card, self.current_card)

    def flip_card(self, card):
        """Flip current card and show translation."""
        self.card.config(bg="black")
        self.card.itemconfig(self.card_language,
                             text="English",
                             fill="white")
        self.card.itemconfig(self.card_transcription,
                             text="")
        self.card.itemconfig(self.card_word,
                             text=card["English"],
                             fill="white",
                             font=(self.font, 80, "bold"))

    def remove_learnt_card(self):
        """Remove learnt card from words_to_learn file."""
        if self.current_card in self.cards_to_learn:
            self.cards_to_learn.remove(self.current_card)
            words_to_learn = pandas.DataFrame(self.cards_to_learn)
            words_to_learn.to_csv("data/words_to_learn.csv", index=False)
            self.show_next_card()

    def all_words_learnt(self):
        """Show text "all words learnt" and disable buttons."""
        self.correct_button.config(state="disabled")
        self.wrong_button.config(state="disabled")
        self.card.config(bg="white")
        self.card.itemconfig(self.card_language,
                             text="",
                             fill="black")
        self.card.itemconfig(self.card_transcription,
                             text="",
                             fill="black")
        self.card.itemconfig(self.card_word,
                             text="Well done!!!\n You have learnt all the words!",
                             fill="black",
                             font=(self.font, 40, "normal"),
                             justify="center")


if __name__ == '__main__':
    FlashcardApp()