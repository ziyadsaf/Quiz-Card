import csv
import random
from pathlib import Path

path = Path('data.csv')
lines = path.read_text().splitlines()
reader = csv.reader(lines)
header_row = next(reader)
#get index of each header
for index,row in enumerate(header_row):
    print(index,row)

#get question and answer data from csv and store in arrays
question_bank = {}
question_answer_bank = {}
for row in reader:
    question_text = str(row[0])
    choice1 = str(row[1])
    choice2 = str(row[2])
    choice3 = str(row[3])
    choice4 = str(row[4])
    answer_text = str(row[5])
    question_bank[question_text] = {choice1,choice2,choice3,choice4}
    question_answer_bank[question_text] = answer_text

def get_question_answer_bank():
    return question_answer_bank

def get_question_bank():
    return question_bank

#show questions in succession
def show_random_question(question_bank, question):
    if question == "yes":
        number = 1
        for question, choices in question_bank.items():
            print(f"Question {number}: {question_text}")
            number += 1
            print("Choices:", choices)
    else:
        return None

#answering a question    
def answer_question():
     for question, choices in question_bank.items():
        answer = str(input("Write your answer here: "))
        if answer == question_answer_bank[question]:
            print('Correct!')
        else:
            print("Try again")


def start_random_quiz():
    question = input("Do you want to start the random quiz? If so, type yes.")
    show_random_question(get_question_bank(), question)   
    answer_question()

start_random_quiz()

#for question,choice,answer in question_answer_bank.items():
    