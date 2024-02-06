import csv
import sys
import sqlite3
import tkinter as tk
import tkinter.font as font
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class QuizGUI:
    def __init__(self, name):
        self.name = name
        name.title("Quiz App")

        self.data = None
        self.file_name = None
        self.q_bank = None
        self.q_answer = None
        self.incorrect_questions = None

        #initialise the label and load_quiz as need load_quiz button to be changed later
        #label must be above the load_quiz button so also needs to be initialised

        self.label_quiz = tk.Label(self.name, text="Welcome to Quiz-Card!")
        self.label_quiz.pack(pady=10)
        self.btn_load_quiz = tk.Button(self.name, text="Load Quiz", command=self.load_quiz)
        self.btn_load_quiz.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.create_menu()

    def create_menu(self):
        """
        Creates a menu with buttons for starting a quiz, viewing
        flashcards, and exiting the program.
        """
    
        btn_start_quiz = tk.Button(self.name, text="Start Quiz", command=self.start_quiz)
        btn_start_quiz.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        btn_view_flashcards = tk.Button(self.name, text="View Flashcards", command=self.view_flashcards)
        btn_view_flashcards.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        btn_exit_app = tk.Button(self.name, text="Exit", command=self.name.destroy)
        btn_exit_app.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

    def load_quiz(self):
        """
        Allows the user to select a .csv file, reads the file, and stores the
        data in the "q_bank" and "q_answer" variables.
        No longer needed .csv check as filedialog does that for us
        """
        file_name = filedialog.askopenfilename(initialdir="/",
                                               title = "Select a .csv file",
                                               filetypes = (("CSV files", "*.csv*"),)
                                               )

        if file_name:
            path = Path(file_name)
            lines = path.read_text().splitlines()
            reader = csv.reader(lines)
            header_row = next(reader)

            self.data = self.get_data(reader)
            self.q_bank, self.q_answer = self.data

            messagebox.showinfo("Quiz-Card", f"{Path(file_name).stem}.csv loaded successfully!")
            self.btn_load_quiz['text'] = f"File Loaded: {Path(file_name).stem}.csv\n\nClick to change file"

    
    def get_data(self, reader):
        """
        Reads data from a CSV file, 
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

    def store_questions(self):
        """
        Displays questions in numerical order and returns the questions as a dict
        """
        questions = {}
        for number, (q, choices) in enumerate(self.q_bank.items()):
            number = number + 1
            questions[number] = {'question': q, 'choices': choices}
              
        return questions
    
    def start_quiz(self):
        quiz_questions = self.store_questions()
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



    def answer_question(self):
       
        pass

    def reattempt_questions(self):
       
        pass

    def view_flashcards(self):
        
        pass


def main():
    window = tk.Tk()
    window.geometry("500x500")
    app = QuizGUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()
