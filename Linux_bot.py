import json
from difflib import get_close_matches
import pyttsx3
from typing import List


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()



# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    """
    Read the knowledge base from a JSON file.

    :param file_path: The path to the JSON file containing the knowledge base.
    :return: A dictionary with the knowledge base data.
    """
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    """
    Write the updated knowledge base to a JSON file.

    :param file_path: The path to the JSON file to save the knowledge base.
    :param data: A dictionary with the knowledge base data.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Find the closest matching question
def find_best_match(user_question: str, questions: List[str]) -> str or None:
    """
    Find the closest matching question in the knowledge base.

    :param user_question: The user's input question.
    :param questions: A list of questions from the knowledge base.
    :return: The closest matching question or None if no match is found.
    """
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str or None:
    """
    Retrieve the answer for a given question from the knowledge base.

    :param question: The matched question from the knowledge base.
    :param knowledge_base: A dictionary containing the knowledge base data.
    :return: The answer to the question or None if the question is not found.
    """
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


# Main function to handle user input and respond
def chatbot():
    """
    Run the chatbot to interact with the user, answer questions, and learn new information.

    The chatbot does the following:
    1. Load the knowledge base from a JSON file.
    2. Continuously prompt the user for questions.
    3. Find the closest matching question in the knowledge base.
    4. If a match is found, return the answer. Otherwise, ask the user to teach the chatbot.
    5. If the user provides a new answer, add it to the knowledge base and save the updated knowledge base to the JSON file.
    6. Exit the chatbot when the user types 'quit'.
    """
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            break

        # Finds the best match, otherwise returns None
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            # If there is a best match, return the answer from the knowledge base
            answer: str = get_answer_for_question(best_match, knowledge_base)
            speak(answer)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            speak("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! I've learned something new.")


if __name__ == "__main__":
    chatbot()