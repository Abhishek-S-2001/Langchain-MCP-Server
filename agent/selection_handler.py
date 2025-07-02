from agent.tool import book_appointment_by_input
import re

def detect_selection_and_book(user_input):
    user_input = user_input.lower()

    number_map = {
        "first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5",
        "sixth": "6", "seventh": "7", "eighth": "8", "ninth": "9", "tenth": "10"
    }

    # Try to match patterns like 'option 1', 'choose 2', '3rd'
    match = re.search(r'(option\s*(\d+))|(choose\s*(\d+))|(\b(\d+)(st|nd|rd|th)?\b)', user_input)
    if match:
        selected_option = match.group(2) or match.group(4) or match.group(7)
        return book_appointment_by_input(selected_option=selected_option, user_note="No additional note provided.")

    # Try to match phrases like 'first one', 'second option', etc.
    for word, num in number_map.items():
        if word in user_input:
            return book_appointment_by_input(selected_option=num, user_note="No additional note provided.")

    return None
