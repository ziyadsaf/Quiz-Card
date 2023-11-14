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
def show_random_question(question):
    if question == "yes":
        number = 1
        for question, choices in question_bank.items():
            print(f"Question {number}: {question_text}")
            number += 1
            print("Choices:", choices)
    else:
        return None

#answering a question    
#answering a question    
def answer_question():
    total_score = 0 # initialize total_score outside the loop
    for q_text in question_bank:
        score = 0
        attempts = 0 # initialize the number of attempts a player can make
        while attempts < 4:
            answer = str(input(f"Write your answer for '{q_text}': ")) # ask for the answer in the while loop so it asks for every attempt
            if answer == question_answer_bank[q_text]: # if answer = answer in question_answer_bank dict
                print('Correct!')
                score += 1 # add one to score if they get a question correct
                break  # Exit the loop if the answer is correct
            else:
                print("Try again")
                score -= 1
                attempts += 1
        else:
            # print this if they run out of attempts (exits the while loop)
            print(f"You have run out of attempts. The correct answer was {question_answer_bank[q_text]}")
        
        total_score += score  # add the score for the current question to the total score
        print(f"Your current score is: {total_score}")

    print(f"\nYour final score was {total_score}")


def start_random_quiz():
    start = input("Do you want to start the random quiz? If so, type yes.")
    show_random_question(start)   
    answer_question()

start_random_quiz()

#for question,choice,answer in question_answer_bank.items():
    