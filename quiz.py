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
        for q, choices in question_bank.items():
            print(f"Question {number}: {q}")
            number += 1
            print("Choices:", choices)
    else:
        return None

#answering a question    
#answering a question    
def answer_question():
    total_score = 0 # initialize total_score outside the loop
    incorrect_questions = {}
    number_wrong = 0
    for q_text in question_bank:
        score = 0
        attempts = 0 # initialize the number of attempts a player can make
        correct = 1
        wrong = -1
        while attempts < 4:
            answer = str(input(f"Write your answer for '{q_text}': ")) # ask for the answer in the while loop so it asks for every attempt
            if answer == question_answer_bank[q_text]: # if answer = answer in question_answer_bank dict
                print('Correct!')
                score += 1 # add one to score if they get a question correct
                print(f"You received {correct} point for that question!") #give the no. of points received for the question
                break  # Exit the loop if the answer is correct
            else:
                print("Try again")
                print(f"You received {wrong} point for that question!") #print message for points deducted for the question
                number_wrong += 1
                score -= 1
                attempts += 1

                if q_text not in incorrect_questions: #if the question is not already in incorrect_questions 
                    incorrect_questions[q_text] = question_answer_bank[q_text]
                elif number_wrong == 0:
                    print("You got none wrong, well done! Here's a prize!")       
        else:
            # print this if they run out of attempts (exits the while loop)
            print(f"You have run out of attempts. The correct answer was {question_answer_bank[q_text]}")
        
        total_score += score  # add the score for the current question to the total score
        # return incorrect_questions

    print(f"\nYour final score was {total_score}")
    print(f"\nYou got {number_wrong} questions wrong.")
    #test if it is adding incorrect questions:
    print(incorrect_questions)

# def reattempt_questions(incorrect_q):
#     for question in incorrect_q: #incorrect_q = list from answer_question function
        

#main function to run quiz
def start_random_quiz():
    start = input("Do you want to start the random quiz? If so, type yes.")
    show_random_question(start)   
    answer_question()
    # reattempt_questions(answer_question())
start_random_quiz()
