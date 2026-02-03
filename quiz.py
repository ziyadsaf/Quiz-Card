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
    DB_FILE = "flashcards.db"

    def __init__(self, flashcards=None):
        self.flashcards = flashcards if flashcards else {}

    @classmethod
    def load_flashcards(cls):
        """
        Loads all flashcards from the database and returns a Flashcard instance.
        """
        conn = sqlite3.connect(cls.DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flashcard'")
        if cursor.fetchone() is None:
            conn.close()
            return cls({})

        cursor.execute("SELECT id, question, answer FROM flashcard")
        rows = cursor.fetchall()
        conn.close()

        flashcards = {row[1]: {"id": row[0], "answer": row[2]} for row in rows}
        instance = cls({q: data["answer"] for q, data in flashcards.items()})
        instance._flashcard_ids = {q: data["id"] for q, data in flashcards.items()}
        return instance

    def review_flashcards(self):
        """
        Interactive flashcard review session. Shows question, waits for user,
        then reveals the answer. Offers option to delete mastered cards.
        """
        if not self.flashcards:
            print("\nNo flashcards to review. Take a quiz first to generate some!")
            return

        print(f"\n========== Flashcard Review ==========")
        print(f"You have {len(self.flashcards)} flashcard(s) to review.\n")

        cards_to_delete = []

        for i, (question, answer) in enumerate(self.flashcards.items(), 1):
            print(f"\n--- Card {i} of {len(self.flashcards)} ---")
            print(f"\nQuestion: {question}")
            input("\nPress Enter to reveal the answer...")
            print(f"Answer: {answer}")

            while True:
                response = input("\nDid you get it right? (Y/N) or 'D' to delete this card: ").upper()
                if response == "Y":
                    print("Great job!")
                    break
                elif response == "N":
                    print("Keep practicing!")
                    break
                elif response == "D":
                    cards_to_delete.append(question)
                    print("Card marked for deletion.")
                    break
                else:
                    print("Invalid input. Please enter Y, N, or D.")

        if cards_to_delete:
            print(f"\nDeleting {len(cards_to_delete)} mastered card(s)...")
            for question in cards_to_delete:
                self.delete_flashcard(question)
            print("Cards deleted successfully!")

        print("\n========== Review Complete ==========")

    def delete_flashcard(self, question):
        """
        Deletes a flashcard from the database by question text.
        """
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM flashcard WHERE question = ?", (question,))
        conn.commit()
        conn.close()

        if question in self.flashcards:
            del self.flashcards[question]

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


def show_menu():
    """
    Displays the main menu and returns the user's choice.
    """
    print("\n========== Quiz-Card ==========")
    print("1. Take a Quiz")
    print("2. Review Flashcards")
    print("3. Exit")
    print("================================")
    return input("Choose an option (1-3): ")


def run_quiz():
    """
    Runs the quiz flow: load CSV, answer questions, reattempt, and save flashcards.
    """
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


def review_flashcards():
    """
    Loads and reviews saved flashcards from the database.
    """
    flashcards = Flashcard.load_flashcards()
    flashcards.review_flashcards()


def main():
    while True:
        choice = show_menu()

        if choice == "1":
            run_quiz()
        elif choice == "2":
            review_flashcards()
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()

