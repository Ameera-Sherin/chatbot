import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from models import ProfileDetails

ProfileDetailsType = {}

openai_client = OpenAI(api_key=OPENAI_API_KEY)

class Chatbot:

    def extract_info_with_gpt(self, user_input, missing_question):
        global ProfileDetailsType
        if missing_question:
            print('i am printing ---------------')
            prompt = f"Given {ProfileDetailsType}, update the {user_input} as the data obtained for {missing_question}"
        else:
            prompt = f"Please analyze the following user input: '{user_input}' and extract relevant information."

        response = openai_client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            response_format=ProfileDetails,
        )
        extracted_info = response.choices[0].message.parsed
        
        ProfileDetailsType = extracted_info
        print("Debug: Extracted Info:", ProfileDetailsType)
        
        return ProfileDetailsType

    def ask_missing_info(self):  
        print('Debug1--------------------- ', ProfileDetailsType)
        prompt = f"Analyze the following profile details: {ProfileDetailsType} and identify the first missing piece of information. Provide a question to ask the user for this information, output only the question."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )  
        return response.choices[0].message.content.strip()

    def run(self):
        """Run the chatbot interaction."""
        print("Start the conversation with the bot.")
        
        missing_question = None  # Initialize missing_question here
        while True:
            user_input = input("You: ")
            # Only pass missing_question if it exists
            extracted_info = self.extract_info_with_gpt(user_input, missing_question)  
            
            missing_question = self.ask_missing_info()
            
            if missing_question.lower() == "profile is complete.":
                print("Bot: Profile gathering is complete. Here is your profile:")
                print(json.dumps(ProfileDetailsType, indent=4))
                break
            
            # Ask for missing info
            print(f"Bot: {missing_question}")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
