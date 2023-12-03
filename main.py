import tkinter as tk
import random

words_list = []
points = 0
mistakes = 0

def show_add_words():
    frame_add_words.pack()
    frame_fight.pack_forget()

def show_fight():
    frame_fight.pack()
    frame_add_words.pack_forget()
    result_label.config(text="")
    entry_translation.delete(0, tk.END)
    get_random_word()

def add_words():
    english_word = entry_english.get()
    polish_word = entry_polish.get()

    with open('words.txt', 'r') as file:
        words = file.readlines()
        for word in words:
            if english_word in word or polish_word in word:
                result_label.config(text="To słowo już istnieje w bazie!")
                return

    with open('words.txt', 'a') as file:
        file.write(f"{english_word},{polish_word}\n")

    entry_english.delete(0, tk.END)
    entry_polish.delete(0, tk.END)
    load_words()

def load_words():
    global words_list
    with open('words.txt', 'r') as file:
        words = file.readlines()
        if words:
            words_list = [word.strip().split(',') for word in words]

def get_random_word():
    global words_list
    global points
    global mistakes
    if words_list:
        random_word_pair = random.choice(words_list)
        polish_word = random_word_pair[1]
        label_translation.config(text=f"Tłumaczenie słowa '{polish_word}':")
    else:
        label_translation.config(text="Brak słów w pliku")
        return

    points_label.config(text=f"Punkty: {points}")
    mistakes_label.config(text=f"Błędy: {mistakes}")

def check_translation():
    global words_list
    global points
    global mistakes
    if words_list:
        user_translation = entry_translation.get().strip().lower()
        correct_translation = None
        for word_pair in words_list:
            english_word = word_pair[0].lower()
            if user_translation == english_word:
                points += 1
                result_label.config(text="Poprawna odpowiedź!")
                correct_translation = word_pair[1]
                break

        if correct_translation is None:
            mistakes += 1
            if words_list:
                correct_translation = words_list[0][1]
            result_label.config(text=f"Błędna odpowiedź. Poprawne tłumaczenie to: {correct_translation}")

        get_random_word()
        entry_translation.delete(0, tk.END)

random.seed("JAZDA")
root = tk.Tk()
root.title("Nauka słówek")
root.geometry("800x600")

frame_buttons = tk.Frame(root)
frame_buttons.pack()

button_add_words = tk.Button(frame_buttons, text="ADD WORDS", command=show_add_words, font=("Arial", 16))
button_add_words.pack(side=tk.LEFT, padx=10, pady=10)

button_fight = tk.Button(frame_buttons, text="FIGHT", command=show_fight, font=("Arial", 16))
button_fight.pack(side=tk.LEFT, padx=10, pady=10)

frame_add_words = tk.Frame(root)

label_english = tk.Label(frame_add_words, text="Słówko angielskie:", font=("Arial", 16))
label_english.grid(row=0, column=0, padx=10, pady=10)

entry_english = tk.Entry(frame_add_words, font=("Arial", 16))
entry_english.grid(row=0, column=1, padx=10, pady=10)

label_polish = tk.Label(frame_add_words, text="Słówko polskie:", font=("Arial", 16))
label_polish.grid(row=1, column=0, padx=10, pady=10)

entry_polish = tk.Entry(frame_add_words, font=("Arial", 16))
entry_polish.grid(row=1, column=1, padx=10, pady=10)

button_add = tk.Button(frame_add_words, text="Add", command=add_words, font=("Arial", 16))
button_add.grid(row=2, columnspan=2, padx=10, pady=10)

frame_fight = tk.Frame(root)

label_translation = tk.Label(frame_fight, text="", font=("Arial", 18))
label_translation.pack(pady=20)

entry_translation = tk.Entry(frame_fight, font=("Arial", 16))
entry_translation.pack(pady=10)

button_fight_check = tk.Button(frame_fight, text="Check", command=check_translation, font=("Arial", 16))
button_fight_check.pack(pady=10)

result_label = tk.Label(frame_fight, text="", font=("Arial", 16))
result_label.pack(pady=10)

points_label = tk.Label(frame_fight, text=f"Punkty: {points}", font=("Arial", 16))
points_label.pack(pady=10)

mistakes_label = tk.Label(frame_fight, text=f"Błędy: {mistakes}", font=("Arial", 16))
mistakes_label.pack(pady=10)

load_words()

root.mainloop()
