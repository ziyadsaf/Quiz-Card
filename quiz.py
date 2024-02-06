import csv
import sys
from pathlib import Path
import sqlite3

class Quiz:
    def __init__(self):
        self.data = None
        self.file_name = None
        self.q_bank = None
        self.q_answer = None
        self.incorrect_questions = None

    def get_file(self, path):
        """
        Reads a file at the given path, splits the lines, and uses a CSV reader to read the contents.
        """
        lines = path.read_text().splitlines()
        reader = csv.reader(lines)
        header_row = next(reader)
        return reader

    def get_data(self, reader):
        """
        Takes in a question bank and a question-answer bank as parameters, read data from a CSV file, 
        and populates the question bank and question-answer bank with the data from the file.
        """
        question_bank = {}
        question_answer_bank = {}
        for row in reader:
            question_number = str(row[0])
            question_text = str(row[1])
            choices = {row[i] for i in range(2,  6)}
            answer_text = str(row[6])
            question_bank[question_text] = choices
            question_answer_bank[question_text] = answer_text
        return question_bank, question_answer_bank

    def process_csv(self):
        """
         Prompts the user to enter the file name of a .csv file, checks if the 
         file type is valid, and then processes the csv file from the get_data() function
        """
        while True:
            file_name = input("Please enter the file name of the .csv file: ")
            if file_name.lower().endswith(".csv"):
                path = Path(file_name)
                reader_file = self.get_file(path)
                data_processed = self.get_data(reader_file)
                break
            else:
                print("That is an invalid file type. Please try again.")

        self.data, self.file_name = data_processed, file_name

    def show_question(self, question):
        """
        Displays a list of questions and their options if the user inputs
        "Y", otherwise it exits the program if the user inputs "N".
        """
        q_list_bank = list(self.q_bank)
        while True:
            if question.upper() == "Y":
                for number, (q, choices) in enumerate(self.q_bank.items()):
                    number = number + 1
                    print(f"Question {number}: {q}")
                    print("Options:", choices, "\n")
                break
            elif question.upper() == "N":
                print("Ok, taking you back to the homepage")
                sys.exit()
            else:
                question = input("That is an invalid input.\nType in Y for yes or N for no: ")

    def answer_question(self):
        """
        Allows the user to answer a set of questions, keeps track of their score, and
        provides feedback on incorrect answers.
        """
        total_score = 0
        incorrect_questions = {}
        number_wrong = 0

        for q_text in self.q_bank:
            score = 0
            attempts = 0
            max_attempts = 3
            correct_answer = self.q_answer[q_text]

            while attempts < max_attempts:
                answer = input(f"Write your answer for '{q_text}': ")
                if answer.upper() == correct_answer:
                    print('Correct!')
                    score += 1
                    print(f"You received 1 point for that question!")
                    break
                else:
                    print("Incorrect. Try again.")
                    print("You received -1 point for that question!")
                    number_wrong += 1
                    score -= 1
                    attempts += 1

                    if q_text not in incorrect_questions:
                        incorrect_questions[q_text] = correct_answer

                if attempts >= max_attempts:
                    incorrect_questions[q_text] = correct_answer
                    print(f"You have run out of attempts. The correct answer was {correct_answer}")

            total_score += score

        print(f"\n------------ Your final score was {total_score} ------------")
        if number_wrong == 0:
            print("Well done, you got all the questions correct!")
        elif number_wrong == 1:
            print(f"\nYou got {number_wrong} question wrong.\n")
        else:
            print(f"\nYou got {number_wrong} questions wrong.\n")

        self.incorrect_questions = incorrect_questions
        return incorrect_questions #returns all the incorrect questions with their correct answer

    def reattempt_questions(self, incorrect_questions):
        """
        Allows the user to retry answering incorrect questions from a
        question bank, with a maximum of (3) attempts per question.
        """
        reattempt_questions = [] #store questions to be reattempted
        reattempt_questions_answers = {} 

        for incorrect_question in incorrect_questions.keys():
            correct_answer = self.incorrect_questions[incorrect_question]
            choices = self.q_bank[incorrect_question]
            attempts = 0
            max_attempts = 3

            while attempts < max_attempts:
                print(f"Question: {incorrect_question}")
                print("Options:", choices)
                answer = input("Your answer: ")
                if answer.upper() == correct_answer:
                    print("Correct!")
                    break
                else:
                    attempts += 1
                    print("Try Again")
            else:
                print("You have run out of attempts for that question!\nYour flashcard will be generated now.")
                reattempt_questions.append(incorrect_question)
                reattempt_questions_answers[incorrect_question] = correct_answer

        if not reattempt_questions:
            print("Well done, you have now got all the questions correct!")

        return reattempt_questions_answers


class Flashcard:
    def __init__(self, flashcards):
        self.flashcards = flashcards

    def create_flashcard(self):
        """
        Prints out flashcards for incorrect questions.
        """

        print("\nFlashcards for Incorrect Questions:")
        index = 1
        for question, correct_answer in self.flashcards.items():
            print(f"\n---Flashcard {index}---\n")
            print(f"Question: {question}")
            print(f"Correct Answer: {correct_answer}")
            index += 1

    def save_flashcards(self):
        """
        Saves flashcards to a SQLite database, checking if a flashcard
        already exists before inserting a new one.
        """

        db_file = "flashcards.db"
        conn = sqlite3.connect(db_file)

        cursor = conn.cursor()
        sql_file_path = Path("flashcards.sql")
        if sql_file_path.exists():
            with open(sql_file_path, "r") as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)

        for question, correct_answer in self.flashcards.items():
            cursor.execute("SELECT question FROM flashcard WHERE question = ?", (question,))
            result = cursor.fetchone()

            if result is None:
                cursor.execute("INSERT INTO flashcard (question, answer) VALUES (?, ?)", (question, correct_answer))
            else:
                print(f"Flashcard already created for question {question}. Please revise this before attempting the quiz again")

        conn.commit()
        conn.close()


def main():
    quiz = Quiz()
    quiz.process_csv()
    quiz.q_bank, quiz.q_answer = quiz.data

    start = input("Do you want to start the quiz?\nType in Y for yes or N for no: ")
    quiz.show_question(start)
    incorrect_questions = quiz.answer_question()

    if incorrect_questions:
        print("You will now be given a chance to reattempt the incorrect questions...")
        quiz.reattempt_questions(incorrect_questions)

        print("Creating your flashcards for the incorrect questions...")

        flashcards = Flashcard(quiz.incorrect_questions)
        flashcards.create_flashcard()
        flashcards.save_flashcards()
        print("Flashcards saved to file.")
    else:
        print("No flashcards to create, you got everything correct first time! Congratulations")

if __name__ == "__main__":
    main()

