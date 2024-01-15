import random


def read_questions(filename):
    """Read questions from a file and return a list of dictionaries."""
    questions = []

    try:
        with open (filename, 'r') as file:
            lines = file.readlines ()

            i = 0
            while i < len (lines):
                if lines[i].lower ().startswith ("question"):
                    question_text = lines[i][len ("Question"):].strip ()

                    options = [lines[i + j].strip () for j in range (1, 5)]
                    correct_answer = options[0]

                    # Shuffle the options
                    random.shuffle (options)

                    question_data = {
                        'question': question_text,
                        'options': options,
                        'correct_answer': correct_answer
                    }

                    questions.append (question_data)
                    i += 5  # Move to the next question
                else:
                    i += 1  # Move to the next line
    except FileNotFoundError:
        print (f"Error: File '{filename}' not found.")
    except Exception as e:
        print (f"An error occurred while reading the file: {e}")

    return questions

def display_question(question_data):
    """Display a question and its options."""
    print (f"\n{question_data['question']}")

    for i, option in enumerate (question_data['options'], start=1):
        print (f"{i}. {option}")


def get_user_answer():
    """Get user's answer and validate it."""
    while True:
        try:
            user_input = int (input ("Enter the number of your answer: "))
            if 1 <= user_input <= 4:
                return user_input
            else:
                print ("Invalid input. Please enter a number between 1 and 4.")
        except ValueError:
            print ("Invalid input. Please enter a number.")


def main():
    # Read questions from the file
    questions = read_questions ("questions.txt")

    if not questions:
        print ("No valid questions found in the file.")
        return

    # Shuffle the questions
    random.shuffle (questions)

    correct_answers = 0

    # Iterate through each question
    for question_data in questions:
        display_question (question_data)

        # Get user's answer
        user_answer = get_user_answer ()

        # Check if the answer is correct
        if question_data['options'][user_answer - 1] == question_data['correct_answer']:
            print ("Correct!\n")
            correct_answers += 1
        else:
            print (f"Wrong! The correct answer is: {question_data['correct_answer']}\n")

    # Display the results
    total_questions = len (questions)

    if total_questions > 0:
        percentage_correct = (correct_answers / total_questions) * 100
        print (f"You got {correct_answers} out of {total_questions} questions correct.")
        print (f"Percentage correct: {percentage_correct:.2f}%")
    else:
        print ("No valid questions found in the file.")


if __name__ == "__main__":
    main ()
