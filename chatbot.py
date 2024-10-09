import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from models import ProfileDetails

ProfileDetailsType = {}
isComplete = False

openai_client = OpenAI(api_key=OPENAI_API_KEY)

class Chatbot:

    def extract_info_with_gpt(self, user_input, missing_question):
        global ProfileDetailsType

        if missing_question:
                # Improved prompt for updating profile based on user input and missing information
                prompt = (f"Based on the current profile details: {ProfileDetailsType}, "
                        f"please update the profile with the following user input only: '{user_input}'. "
                        f"This input is specifically for the missing information: '{missing_question}'. "
                        f"Extract the relevant data and provide it in the structured format.")
        else:
                # Improved prompt for extracting information when there's no missing question
                prompt = (f"Please analyze the following user input: '{user_input}' and extract relevant information. "
                        f"Return the extracted data in a structured format that can be used to update the profile.")

        response = openai_client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[{"role": "user", "content": prompt}],
                response_format=ProfileDetails,
            )
        extracted_info = response.choices[0].message.parsed
        
        ProfileDetailsType = extracted_info
        print("Debug: Extracted Info:", ProfileDetailsType)
        
        return ProfileDetailsType
    
    def basic_details_missing(self):
        basicDeatils = getattr(ProfileDetailsType, 'basicDetails', None)
        if basicDeatils and (getattr(basicDeatils, 'name', '') == '' or getattr(basicDeatils, 'age', 0.0) == 0.0):
            return True

    def education_details_missing(self):
        educationDetails = getattr(ProfileDetailsType, 'educationDetails', None)
        if educationDetails and len(getattr(educationDetails, 'educationDetails', [])) < 1:
            return True
        
    def work_details_missing(self):
        workDetails = getattr(ProfileDetailsType, 'workDetails', None)
        if workDetails and len(getattr(workDetails, 'workDetails', [])) < 1:
            return True

    def family_details_missing(self):
        familyDeatils = getattr(ProfileDetailsType, 'familyDetails', None)
        if familyDeatils and (getattr(familyDeatils, 'fathers_name', '') == '' or
                              getattr(familyDeatils, 'mothers_name', '') == '' or
                              getattr(familyDeatils, 'spouse_name', '') == ''):
            return True
    

    def ask_missing_info(self):  
        global isComplete  # Declare global to modify the outer scope variable

        if self.basic_details_missing():
            prompt = (f"Given the following profile details: {ProfileDetailsType}, "
                      f"some data in basic details is missing. "
                      f"Formulate a clear and concise question to ask the user for this missing information. "
                      f"Please output only the question.")
            
        elif self.education_details_missing():
            prompt = (f"Given the following profile details: {ProfileDetailsType}, "
                      f"some data in education details are missing. "
                      f"Formulate a clear and concise question to ask the user for this missing information. "
                      f"Please output only the question.")
        
        elif self.work_details_missing():
            prompt = (f"Given the following profile details: {ProfileDetailsType}, "
                      f"some data in work details are missing. "
                      f"Formulate a clear and concise question to ask the user for this missing information. "
                      f"Please output only the question.")
        
        elif self.family_details_missing():
            prompt = (f"Given the following profile details: {ProfileDetailsType}, "
                      f"some data in family details are missing. "
                      f"Formulate a clear and concise question to ask the user for this missing information. "
                      f"Please output only the question.")
            
        else:
            isComplete = True
            prompt = (f"Given the following profile details: {ProfileDetailsType}, "
                      f"all data is complete. Conclude the profile creation and end the chat.")
            
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
            
            if isComplete:
                print("Bot: Profile gathering is complete.")
                break
            
            # Ask for missing info
            print(f"Bot: {missing_question}")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
