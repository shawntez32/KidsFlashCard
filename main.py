from email.mime import image
from email.policy import default
from tkinter import *
import pandas
import random
from PIL import Image,ImageTk
from gtts import gTTS
import os, playsound
import pygame



BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Ariel", 45, "bold")
FONT2 = ("Ariel", 30, "italic")

wordsLeft = {}
currentCard = {}

# read CSV
try:
    data = pandas.read_csv("data/kids_vocab.csv")
except FileNotFoundError:
    originalData = pandas.read_csv("data/kids_vocab.csv")
    wordsLeft = originalData.to_dict(orient="records")
else:
    wordsLeft = data.to_dict(orient="records")

def sayWord(word):
    language = "en"
    sound = gTTS(text=word, lang=language, slow=False)
    sound.save(f"data/sounds/{word}.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(f"data/sounds/{word}.mp3")
    pygame.mixer.music.play()


def nextCard():
    global currentCard, flipTimer
    window.after_cancel(flipTimer)
    currentCard = random.choice(wordsLeft)
    canvas.itemconfig(cardWord, text="Word", fill="black")
    canvas.itemconfig(cardTitle, text=currentCard["Word"], fill="black")
    canvas.itemconfig(cardBackground, image=flashcardFrontIMG)
    sayWord(currentCard["Word"])
    flipTimer = window.after(4000, func=flipCard)


def flipCard():
    index = currentCard["FilePath"]
    canvas.itemconfig(cardWord, text="Definition", fill="white")
    canvas.itemconfig(cardTitle, text=currentCard["Definition"], fill="white")
    wordImage = photoList[index]
    canvas.itemconfig(cardBackground, image=wordImage)
         
def isKnown():
    wordsLeft.remove(currentCard)
    nextCard()

# UI
window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flipTimer = window.after(6000, func=flipCard)

cat = ImageTk.PhotoImage(file="cat.jfif")
dog = ImageTk.PhotoImage(file="data/images/dog.jfif")
cow = ImageTk.PhotoImage(file="data/images/cow.jfif")
car = ImageTk.PhotoImage(file="data/images/car.jfif")
run = ImageTk.PhotoImage(file="data/images/run.jfif")
school = ImageTk.PhotoImage(file="data/images/school.jfif")
bus = ImageTk.PhotoImage(file="data/images/bus.jfif")

photoList = [cat,dog,cow,car,run,bus,school]

canvas = Canvas(height=526, width=900)
flashcardFrontIMG = ImageTk.PhotoImage(file="card_front.gif")
flashcardBackImage = ImageTk.PhotoImage(file="card_back.gif")
cardBackground = canvas.create_image(400, 263, image=flashcardFrontIMG)
cardTitle = canvas.create_text(400, 263, text="", font=FONT1)
cardWord = canvas.create_text(400, 150, text="", font=FONT2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

checkIMG = PhotoImage(file="right.gif")
correctButton = Button(image=checkIMG, highlightthickness=0, command=isKnown)
correctButton.grid(column=0, row=1)

audioImage = PhotoImage(file="audio2.png")
audioBtn = Button(image=audioImage,highlightthickness=0)
audioBtn.grid(column=1,row=1)

wrongIMG = PhotoImage(file="wrong.gif")
wrongButton = Button(image=wrongIMG, highlightthickness=0, command=nextCard)
wrongButton.grid(column=2, row=1)

nextCard()

window.mainloop()
