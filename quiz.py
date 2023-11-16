import csv
import sys
import random
from pathlib import Path

def get_file(path):
    """
    The function `get_file` reads a file at the given path, splits the lines, and uses a CSV reader to
    read the contents.
    
    :param path: The `path` parameter is the file path to the CSV file that you want to read. It should
    be a string representing the file path
    """

    lines = path.read_text().splitlines()
    reader = csv.reader(lines)
    header_row = next(reader)
    return reader

#get index of each header
# for index,row in enumerate(header_row):
#     print(index,row)

#get question and answer data from csv and store in arrays
def get_data(reader, question_bank = {},question_answer_bank = {}):
    """
    The function `get_data` takes in a question bank and a question-answer bank as parameters, reads
    data from a CSV file, and populates the question bank and question-answer bank with the data from
    the file.
    
    :param question_bank: The `question_bank` parameter is a dictionary that stores the question text as
    the key and a set of choices as the value. Each set of choices contains four options (choice1,
    choice2, choice3, choice4)
    :param question_answer_bank: The `question_answer_bank` parameter is a dictionary that stores the
    answer for each question. The key of the dictionary is the question text, and the value is the
    answer text
    """
    for row in reader:
        question_text = str(row[0])
        choice1 = str(row[1])
        choice2 = str(row[2])
        choice3 = str(row[3])
        choice4 = str(row[4])
        answer_text = str(row[5])
        question_bank[question_text] = {choice1,choice2,choice3,choice4}
        question_answer_bank[question_text] = answer_text
    return question_bank, question_answer_bank

#receive the data file before starting the quiz
def process_csv():
    """
    The function "process_csv" prompts the user to enter the file name of a .csv file, checks if the
    file type is valid, and then processes the csv file from the get_data() function
    """
    while True:
    #ask the user what the file path is for the data file to be processed for the quiz
        file_name = str(input("Please enter the file name of the .csv file: "))
        if file_name.endswith(".csv"):
            path = Path(file_name)
            reader_file = get_file(path)
            #process the csv file
            data_processed = get_data(reader_file)
            break
        else:
            print("That is an invalid file type. Please try again.")

    return data_processed, file_name

#show questions in succession
def show_random_question(question,q_bank):
    """
    The function `show_random_question` displays a random question and its options if the user inputs
    "Y", otherwise it exits the program if the user inputs "N".
    
    :param question: The parameter "question" is a string that represents the user's response to whether
    they want to see a random question or not. It can be either "Y" (yes) or "N" (no)
    :return: None if the input is neither "Y" nor "N".
    """
    number = q_bank.keys()
    choices = q_bank.values()
    while True:
        if question.upper() == "Y":
            for q, choices in q_bank.items():
                print(f"Question {number}: {q}")
                print("Options:", choices)
            break
        elif question.upper() == "N":
            print("Ok, taking you back to the homepage")
            sys.exit()
        else:
            print("Please enter a valid input...")
  
#answering a question    
def answer_question(q_bank,q_answer):
    """
    The function `answer_question` allows a player to answer a series of questions, keeps track of their
    score, and returns a dictionary of incorrect questions and their correct answers.
    :return: The function `answer_question()` returns a dictionary `incorrect_questions` which contains
    the questions that were answered incorrectly along with their correct answers.
    """
    total_score = 0 # initialize total_score outside the loop
    incorrect_questions = {}
    number_wrong = 0
    for q_text in q_bank:
        score = 0
        attempts = 0 # initialize the number of attempts a player can make
        correct = 1
        wrong = -1
        loop = len(q_bank)
        while attempts < 3 and loop > 0:
            answer = str(input(f"Write your answer for '{q_text}': ")) # ask for the answer in the while loop so it asks for every attempt
            if answer == q_answer[q_text]: # if answer = answer in question_answer_bank dict
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
                    incorrect_questions[q_text] = q_answer[q_text]
        else:
            # print this if they run out of attempts (exits the while loop)
            print(f"You have run out of attempts. The correct answer was {question_answer_bank[q_text]}")
        
        total_score += score  # add the score for the current question to the total score
        

    print(f"\n------------ Your final score was {total_score} ------------")
    print(f"\nYou got {number_wrong} questions wrong.\n")
    
    if number_wrong == 0:
        print("Well done, you got all the questions correct!") #shows a message if you got all the questions correct
        sys.exit() #stop the program as they got everything correct 
        '''change this later to give a prize...'''
    
    return incorrect_questions

def reattempt_questions(incorrect_q, q_bank):
    """
    The function `reattempt_questions` takes a dictionary of incorrect questions and their correct
    answers, allows the user to reattempt the questions, and returns a list of questions that still need
    to be reattempted and a dictionary of those questions with their correct answers.
    
    :param incorrect_q: A dictionary containing the questions that the user answered incorrectly, with
    the corresponding correct answers
    :return: The function `reattempt_questions` returns two values: `reattempt_questions` and
    `reattempt_questions_answers`.
    """
    question_reattempt = list(incorrect_q.keys())
    reattempt_questions = []  # store just the questions they failed to reattempt
    reattempt_questions_answers = {}  # store the questions they failed to reattempt with their answers
    for incorrect_question in question_reattempt:
        correct_answer = incorrect_q[incorrect_question]  # correct answer from the original dict passed into function
        choices = q_bank[incorrect_question] #list of choices for each question
        attempts = 0  # reset attempts to zero for each question
        while attempts < 3:
            # Display the question and choices before asking them to answer it
            print(f"Question: {incorrect_question}")
            print("Options:", choices)
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
def start_random_quiz(data, file_name):
    """
    The function "start_random_quiz" prompts the user to start a random quiz, displays random questions,
    allows the user to answer the questions, gives the option to reattempt incorrect questions, and
    provides feedback on the quiz performance.
    """
    start = input("Do you want to start the random quiz?\nType in Y for yes or N for no: ")
    q_bank, q_answer = data
    show_random_question(start,q_bank)
    incorrect_questions = answer_question(q_bank,q_answer)
    if incorrect_questions: #if there are incorrect questions in the list then run reattempt_questions
        reattempt_choice = input("Would you like to reattempt the questions you got wrong? ")
        if reattempt_choice == "yes":
            print("Ok, here are your incorrect questions.\n Think carefully before answering!")
            incorrect_reattempt_only, incorrect_reattempt_answers = reattempt_questions(incorrect_questions, q_bank)
        else:
            print("Ok, thanks for playing the quiz. You missed out on correcting the ones you got wrong though...")
            sys.exit()
   
   # attempting to re-attempt incorrect questions from a question bank. It prompts
   # the user if they would like to see the questions they couldn't answer after re-attempting them.
   # If the user chooses to see the questions, it prints them out. Then, it prompts the user if they
   # would like to see the answers for these questions. If the user chooses to see the answers, it
   # prints them out. Finally, it prints a thank you message.
    
     #separate tuple from reattempt_questions
    if incorrect_reattempt_only or incorrect_reattempt_answers:
        wrong_questions = str(input("Would you like to see the questions you couldn't do after re-attempting them?"))
        if wrong_questions.lower() == "yes":
            print("Here are the questions you couldn't answer...\n")
            for incorrect_reattempt in incorrect_reattempt_only:
                print(incorrect_reattempt)
            show_answer = input("Would you like to look at the answers for these questions? ")
            if show_answer.lower() == "yes":
                for question, answer in incorrect_reattempt_answers.items():
                    print(f"Question: {question}, Answer: {answer}")
            else:
                print("Ok, thanks for playing the quiz!")
        else:
            print("Ok, thanks for playing the quiz!")
    print("Thanks for playing!")

# The code is calling the `process_csv()` function to get the data from a CSV file and the file name.
# Then, it passes the data and file name to the `start_random_quiz()` function to start the random
# quiz.
data,file_name = process_csv()
start_random_quiz(data,file_name)
