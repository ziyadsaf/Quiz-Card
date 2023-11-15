import csv
import sys
import random
from pathlib import Path

path = Path('data.csv')
lines = path.read_text().splitlines()
reader = csv.reader(lines)
header_row = next(reader)
#get index of each header
# for index,row in enumerate(header_row):
#     print(index,row)

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
    if question.upper() == "Y":
        number = 1
        for q, choices in question_bank.items():
            print(f"Question {number}: {q}")
            number += 1
            print("Choices:", choices)
    elif question.upper() == "N":
        print("Ok, taking you back to the homepage")
        sys.exit()
    else:
        return None
  
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
        loop = len(question_bank)
        while attempts < 4 and loop > 0:
            answer = str(input(f"Write your answer for '{q_text}': ")) # ask for the answer in the while loop so it asks for every attempt
            if answer == question_answer_bank[q_text]: # if answer = answer in question_answer_bank dict
                print('Correct!')
                score += 1 # add one to score if they get a question correct
                print(f"You received {correct} point for that question!") #give the no. of points received for the question
                loop -= 1 
                break  # Exit the loop if the answer is correct
            else:
                print("Try again")
                print(f"You received {wrong} point for that question!") #print message for points deducted for the question
                number_wrong += 1
                score -= 1
                attempts += 1

                if q_text not in incorrect_questions: #if the question is not already in incorrect_questions 
                    incorrect_questions[q_text] = question_answer_bank[q_text]
            if number_wrong == 0:
                print("You got none wrong, well done! Here's a prize!")       
        else:
            # print this if they run out of attempts (exits the while loop)
            print(f"You have run out of attempts. The correct answer was {question_answer_bank[q_text]}")
        
        total_score += score  # add the score for the current question to the total score
        

    print(f"\nYour final score was {total_score}")
    print(f"\nYou got {number_wrong} questions wrong.")
    
    return incorrect_questions

def reattempt_questions(incorrect_q):
    question_reattempt = list(incorrect_q.keys())
    reattempt_questions = []  # store just the questions they failed to reattempt
    reattempt_questions_answers = {}  # store the questions they failed to reattempt with their answers
    for incorrect_question in question_reattempt:
        correct_answer = incorrect_q[incorrect_question]  # correct answer from the original dict passed into function
        choices = question_bank[incorrect_question] #list of choices for each question
        attempts = 0  # reset attempts to zero for each question
        while attempts < 4:
            # Display the question and choices before asking them to answer it
            print(f"Question: {incorrect_question}")
            print("Choices:", choices)
            
            answer = input("Your answer: ")
            if answer == correct_answer:
                print("That is now correct! Well done.\nThat question will be removed from your incorrect questions list.")
                incorrect_q.pop(incorrect_question)  # remove the incorrect question as it is now correct
                break
            else:
                attempts += 1
                print("Try Again")
        else:
            print("You have run out of attempts for that question!\n You will get a chance to try again later")
            reattempt_questions.append(incorrect_question)
            # add questions they got wrong with their answer in dict
            reattempt_questions_answers[incorrect_question] = correct_answer

    # if none are wrong
    if not reattempt_questions:
        print("Well done, you have now got all the questions correct!")

    return reattempt_questions, reattempt_questions_answers

# main function to run quiz
def start_random_quiz():
    start = input("Do you want to start the random quiz?\nType in Y for yes or N for no: ")
    show_random_question(start)
    incorrect_questions = answer_question()
    if incorrect_questions: #if there are incorrect questions in the list then run reattempt_questions
        reattempt_choice = input("Would you like to reattempt the questions you got wrong?")
        if reattempt_choice == "yes":
            print("Ok, here are your incorrect questions.\n Think carefully before answering!")
            reattempt_questions(incorrect_questions)
        else:
            print("Ok, thanks for playing the quiz. You missed out on correcting the ones you got wrong though...")
            sys.exit()
    #separate tuple from reattempt_questions
    incorrect_reattempt_only, incorrect_reattempt_answers = reattempt_questions(incorrect_questions)
    if incorrect_reattempt_only or incorrect_reattempt_answers:
        wrong_questions = str(input("Would you like to see the questions you couldn't do after re-attempting them?"))
        if wrong_questions.lower() == "yes":
            print("Here are the questions you couldn't answer...\n")
            for incorrect_reattempt in incorrect_reattempt_only:
                print(incorrect_reattempt)
            show_answer = input("Would you like to look at the answers for these questions?")
            if show_answer.lower() == "yes":
                for question, answer in incorrect_reattempt_answers.items():
                    print(f"Question: {question}, Answer: {answer}")
            else:
                print("Ok, thanks for playing the quiz!")
        else:
            print("Ok, thanks for playing the quiz!")
    print("Thanks for playing!")
start_random_quiz()
