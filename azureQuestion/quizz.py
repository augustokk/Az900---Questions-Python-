import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.questions = questions
        self.current_question_index = 0
        self.correct_answers = 0

        self.setup_gui()

    def setup_gui(self):
        self.master.title("Quiz App")
        self.master.geometry("600x600")
        self.master.configure(bg='#F0F0F0')

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg='#F0F0F0', wraplength=500)
        self.question_label.pack(pady=20)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg='#F0F0F0')
        self.result_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            button = ttk.Button(self.master, text="", style='Option.TButton', command=lambda i=i: self.check_answer(i))
            button.pack(pady=10)
            self.option_buttons.append(button)

        self.style = ttk.Style()
        self.style.configure('Option.TButton', font=("Helvetica", 12), padding=10, background='#FFF')

        self.show_next_question()

    def show_next_question(self):
        # Check if there are more questions
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.config(text=question_data['question'])
            self.result_label.config(text="")  # Clear result label

            for i, option_button in enumerate(self.option_buttons):
                option_button.config(text=question_data['options'][i], command=lambda i=i: self.check_answer(i))
                option_button.configure(style='Option.TButton')  # Reset button style

        else:
            # All questions answered, show final score
            self.show_results()

    def check_answer(self, selected_option):
        # Check if there are more questions
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            correct_answer_index = question_data['options'].index(question_data['correct_answer'])

            for i, option_button in enumerate(self.option_buttons):
                option_button.configure(state=tk.DISABLED)  # Disable buttons during result display

            # Display result for 2 seconds
            if selected_option == correct_answer_index:
                self.result_label.config(text="Correct!", fg='green')
                self.correct_answers += 1
            else:
                self.result_label.config(text=f"Incorrect. Correct answer: {question_data['correct_answer']}", fg='red')

            self.master.after(2000, self.next_question)
        else:
            # If no more questions, do nothing
            pass

    def next_question(self):
        # Move on to the next question
        self.current_question_index += 1
        self.reset_button_states()
        self.show_next_question()

    def reset_button_states(self):
        # Reset button states after displaying result
        for option_button in self.option_buttons:
            option_button.configure(state=tk.NORMAL)
        self.result_label.config(text="")

    def show_results(self):
        # Display the final score
        total_questions = len(self.questions)
        if total_questions > 0:
            percentage_correct = (self.correct_answers / total_questions) * 100
            message = f"You got {self.correct_answers} out of {total_questions} questions correct.\n"
            message += f"Percentage correct: {percentage_correct:.2f}%"
        else:
            message = "No valid questions found."

        # Show final score in messagebox
        messagebox.showinfo("Quiz Results", message)
        self.master.destroy()

def read_questions(filename):
    """Read questions from a file and return a list of dictionaries."""
    questions = []

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            i = 0
            while i < len(lines):
                if lines[i].lower().startswith("question"):
                    question_text = lines[i][len("Question"):].strip()

                    options = [lines[i + j].strip() for j in range(1, 5)]
                    correct_answer = options[0]

                    # Shuffle the options
                    random.shuffle(options)

                    question_data = {
                        'question': question_text,
                        'options': options,
                        'correct_answer': correct_answer
                    }

                    questions.append(question_data)
                    i += 5  # Move to the next question
                else:
                    i += 1  # Move to the next line
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return questions

if __name__ == "__main__":
    questions = read_questions("questions.txt")

    if not questions:
        print("No valid questions found in the file.")
    else:
        root = tk.Tk()
        app = QuizApp(root, questions)
        root.mainloop()
