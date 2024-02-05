import csv
import sys
from pathlib import Path
import sqlite3

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
    """
    for row in reader:
        question_number = str(row[0])
        question_text = str(row[1])
        choices = {row[i] for i in range(2,  6)} #replaced oriignal choices variables with choices list comp
        answer_text = str(row[6])
        question_bank[question_text] = choices
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
        file_name = input("Please enter the file name of the .csv file: ")
        if file_name.lower().endswith(".csv"):
            path = Path(file_name)
            reader_file = get_file(path)
            #process the csv file
            data_processed = get_data(reader_file)
            break
        else:
            print("That is an invalid file type. Please try again.")

    return data_processed, file_name #return data and file name - to be used for starting quiz func

#show questions in succession
def show_question(question,q_bank):
    """
    The function `show_random_question` displays a random question and its options if the user inputs
    "Y", otherwise it exits the program if the user inputs "N".
    """
    q_list_bank = list(q_bank) #use this for the question numbers
    # number = q_bank.keys() #gets the questions (keys) and assigns it to number variable
    # choices = q_bank.values() ##gets the options for each q(values) and assigns it to choices
    
    while True:
        if question.upper() == "Y": 
            for number, (q, choices) in enumerate(q_bank.items()):
                number = number + 1
                print(f"Question {number}: {q}") 
                print("Options:", choices,"\n")
            break
        elif question.upper() == "N":
            print("Ok, taking you back to the homepage")
            sys.exit()
        else:
            question = input("That is an invalid input.\nType in Y for yes or N for no: ")
  
#answering a question    
def answer_question(q_bank, q_answer):
    """
    The function `answer_question` takes a question bank and a dictionary of question-answer pairs,
    prompts the user to answer each question, keeps track of the score, and returns a dictionary of
    incorrect questions and their correct answers.
    """
    total_score =  0
    incorrect_questions = {}
    number_wrong =  0

    for q_text in q_bank:
        score =  0
        attempts =  0
        max_attempts =  3
        correct_answer = q_answer[q_text]

        while attempts < max_attempts:
            answer = input(f"Write your answer for '{q_text}': ")
            if answer.upper() == correct_answer:
                print('Correct!')
                score +=  1
                print(f"You received  1 point for that question!")
                break
            else:
                print("Incorrect. Try again.")
                print("You received -1 point for that question!")
                number_wrong +=  1
                score -=  1
                attempts +=  1

                if q_text not in incorrect_questions: #if the question is not already in incorrect_questions 
                    incorrect_questions[q_text] = q_answer[q_text]
                    
            if attempts >= max_attempts:
                incorrect_questions[q_text] = correct_answer
                print(f"You have run out of attempts. The correct answer was {correct_answer}")

        total_score += score

    print(f"\n------------ Your final score was {total_score} ------------")
    if number_wrong ==  0:
        print("Well done, you got all the questions correct!")
    elif number_wrong ==  1:
        print(f"\nYou got {number_wrong} question wrong.\n")
    else:
        print(f"\nYou got {number_wrong} questions wrong.\n")

    return incorrect_questions

def reattempt_questions(incorrect_q, q_bank):
    """
    The function `reattempt_questions` takes a dictionary of incorrect questions and their correct
    answers, allows the user to reattempt the questions, and returns a list of questions that still need
    to be reattempted and a dictionary of those questions with their correct answers.
    """

    reattempt_questions = []  # store just the questions they failed to reattempt
    reattempt_questions_answers = {}  # store the questions they failed to reattempt with their answers
    for incorrect_question in incorrect_q.keys():
        correct_answer = incorrect_q[incorrect_question]  # correct answer from the original dict passed into function
        choices = q_bank[incorrect_question] #list of choices for each question
        attempts = 0  # reset attempts to zero for each question
        while attempts < 3:
            # Display the question and choices before asking them to answer it
            print(f"Question: {incorrect_question}")
            print("Options:", choices)
            answer = input("Your answer: ")
            if answer.upper() == correct_answer:
                print("Correct!")
                #print("That is now correct! Well done.\nThat question will be removed from your incorrect questions list.")
                #incorrect_q.pop(incorrect_question)  # don't need this for now as flashcard needs incorrect qs. remove the incorrect question as it is now correct
                break
            else:
                attempts += 1
                print("Try Again")
        else:
            print("You have run out of attempts for that question!\nYour flashcard will be generated now.")
            reattempt_questions.append(incorrect_question)
            # add questions they got wrong with their answer in dict
            reattempt_questions_answers[incorrect_question] = correct_answer

    # if none are wrong
    if not reattempt_questions:
        print("Well done, you have now got all the questions correct!")
       

    return reattempt_questions, reattempt_questions_answers

def create_flashcard(flashcard_questions):
    """
    Create flashcards for incorrect questions.
    """
    print("\nFlashcards for Incorrect Questions:")
    index =  1
    for question, correct_answer in flashcard_questions.items():
        print(f"\n---Flashcard {index}---\n")
        print(f"Question: {question}")
        print(f"Correct Answer: {correct_answer}")
        index +=  1
    return flashcard_questions


def save_flashcards(flashcards):
    """
    The `save_flashcards` function saves flashcards to a SQLite database, checking if the flashcard
    already exists before inserting it.
    """

    db_file = "flashcards.db"
    conn = sqlite3.connect(db_file) #connect to database

    cursor = conn.cursor()
    sql_file_path = Path("flashcards.sql")
    if sql_file_path.exists():
        with open(sql_file_path, "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)


    for question, correct_answer in flashcards.items():
        #checking if the question exists - question variable is passed in as a tuple
        cursor.execute("SELECT question FROM flashcard WHERE question = ?", (question,))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute("INSERT INTO flashcard (question, answer) VALUES (?, ?)",(question, correct_answer))
        else:
            print(f"Flashcard already created for question {question}. Please revise this before attempting the quiz again")
    
    conn.commit()
    conn.close()

# main function to run quiz
def start_quiz(data, file_name):
    """
    The function "start_random_quiz" prompts the user to start a random quiz, displays random questions,
    allows the user to answer the questions, gives the option to reattempt incorrect questions, and
    provides feedback on the quiz performance.
    """
    if file_name:
        start = input("Do you want to start the quiz?\nType in Y for yes or N for no: ")
        q_bank, q_answer = data 
        show_question(start,q_bank)
        incorrect_questions = answer_question(q_bank,q_answer)

    if incorrect_questions: #if there are incorrect questions in the list then run reattempt_questions
        valid = True
        while valid:
            reattempt_choice = input("Would you like to reattempt the questions you got wrong (y) or skip to creating flashcards (n)?\n")
            if reattempt_choice.lower() == "yes" or reattempt_choice.lower() == "y":
                print("Ok, here are your incorrect questions.\nThink carefully before answering!")
                incorrect_reattempt_only, incorrect_reattempt_answers = reattempt_questions(incorrect_questions, q_bank)
                valid = False
            elif reattempt_choice.lower() == "no" or reattempt_choice.lower() == "n":
                print("Ok, your flashcards will be created...")
                valid = False
            else:
                reattempt_choice = input("That is an invalid input, please try again by answering yes or no")
    
        
    return incorrect_questions

"""
Calling main start quiz function
"""
# The code is calling the `process_csv()` function to get the data from a CSV file and the file name.
# Then, it passes the data and file name to the `start_quiz()` function to start the random
# quiz.
data,file_name = process_csv()
incorrect_questions = start_quiz(data, file_name)
# Create flashcards only if there are incorrect questions returned 
if len(incorrect_questions) > 0: 
    print("Your flashcards are now being created...")
    flashcard_questions = create_flashcard(incorrect_questions)
    save_flashcards(flashcard_questions)
    print("Flashcards saved to file.")
else:
    print("No flashcards to create, you got everything correct first time! Congratulations")
    print("Creating feedback file...")

def feedback_csv():
    '''CSV Feedback:
    - Total questions attempted
    - List of attempts with answers given
    - How many tries it took to get the right answer
    - Option to add personal feedback into csv'''

    

