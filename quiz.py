import csv
import sys
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class QuizGUI:
    def __init__(self, name):
        self.name = name
        name.title("Quiz App")

        self.data = None
        self.file_name = None
        self.q_bank = None
        self.q_answer = None
        self.incorrect_questions = None

        self.create_menu()

    def create_menu(self):

        tk.Label(self.name, text="Welcome to Quiz-Card!").pack(pady=10)

        tk.Button(self.name, text="Load Quiz", command=self.load_quiz).pack(pady=10)
        tk.Button(self.name, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.name, text="View Flashcards", command=self.view_flashcards).pack(pady=10)
        tk.Button(self.name, text="Exit", command=self.name.destroy).pack(pady=10)

    def load_quiz(self):
        file_name = 0

        if file_name:
            path = Path(file_name)
            reader_file = self.get_file(path)
            self.data = self.get_data(reader_file)
            self.q_bank, self.q_answer = self.data
            messagebox.showinfo("Quiz App", "Quiz loaded successfully!")


    def start_quiz(self):
        pass

    def show_question(self):
       
        pass

    def answer_question(self):
       
        pass

    def reattempt_questions(self):
       
        pass

    def view_flashcards(self):
        
        pass


def main():
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
