from utils import detect_intent, retrieve_answer
import csv
import os
from datetime import datetime

timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')

def mock_lead_capture(name,email,platform):
    file_exists = os.path.isfile('leads.csv')
    with open('leads.csv','a',newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Name','Email','Platform','Date'])
        writer.writerow([name,email,platform,timestamp])
    print(f'\nLead captured: {name},{email},{platform}\n')


def chat():
    print('AutoStream AI Agent (type "exit" or "bye" to quit)\n')

    state = {
        'intent':None,
        'name':None,
        'email':None,
        'platform':None,
        'collecting':None,
        'awaiting_confirmation': False
    }

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'exit' or user_input.lower() == 'bye':
            print('Bot: Goodbye!')
            break

# 🔥 Handle yes/no after lead capture
        if state.get("awaiting_confirmation"):
            answer = user_input.lower()

            if answer in ["no", "nope", "nah","n"]:
                print("Bot: Thank you! Have a great day :)")
                break

            elif answer in ["yes", "yeah", "yup", "sure","y"]:
                state["awaiting_confirmation"] = False
                print("Bot: Great! You can ask about pricing or policies.")
                continue

            else:
                print("Bot: Please answer with yes or no.")
                continue

        if state['collecting']:
            if state['collecting'] == 'name':
                state['name'] = user_input
                state['collecting'] = 'email'
                print('Bot: Please enter your email:')
                continue
            
            elif state["collecting"] == "email":
                state["email"] = user_input
                state["collecting"] = "platform"
                print("Bot: Which platform do you create content on? (YouTube/Instagram)")
                continue

            elif state["collecting"] == "platform":
                state["platform"] = user_input
                state["collecting"] = None

                mock_lead_capture(state['name'],
                state['email'],state['platform'])

                print("Bot: Thank you! Our team will reach out to you soon.")
                state["intent"] = None
                state["name"] = None
                state["email"] = None
                state["platform"] = None
                state["collecting"] = None
                state["awaiting_confirmation"] = True
                print("\nBot: Is there anything else I can help you with? (Yes/No)\n")
                continue

        intent = detect_intent(user_input)

        if intent == 'greeting':
            print("Bot: Welcome to AutoStream, an AI-powered video editing platform for content creators. I can assist you with pricing, policies or getting started :)")
        
        elif intent == 'pricing':
            print("Bot: Let me pull up the details for you…")
            data = retrieve_answer(user_input)
            print('Bot:',data)

        elif intent == 'policies':
            print("Bot: Let me pull up the details for you…")
            data = retrieve_answer(user_input)
            print('Bot:',data)

        elif intent == 'high_intent':
            print("Bot: Awesome! Let me get you started.")
            state['collecting'] = 'name'
            print('Bot: Please enter your name:')

        else:
            print('Bot: Can you please clarify your question?')


if __name__ == "__main__":
    chat()