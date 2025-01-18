# chatbot.py

from openai_handler import OpenAIHandler
from database_handler import DatabaseHandler
from language_handler import LanguageHandler
from config import DB_CONFIG, SUPPORTED_LANGUAGES
from rate_limiter import RateLimiter
from validators import InputValidator

class Chatbot:
    def __init__(self):
        # Initialize chatbot with required handlers.
        self.openai_handler = OpenAIHandler()
        self.language_handler = LanguageHandler()
        self.db_handler = DatabaseHandler(**DB_CONFIG)
        self.user_language = 'en'
        self.rate_limiter = RateLimiter()
        self.validator = InputValidator()
        
        # Greeting set as a default response
        self.default_responses = {
            "greeting": "Hello! I am a ChatBot from Nejoum Al Jazeera, and can assist you in with the following things:\n"+
                        "- Car location\n" +
                        "- Car Loading Schedule\n" +
                        "- Payment Status or Details\n" +
                        "- Car Payment Detals\n" +
                        "- Car Arrival Information\n" +
                        "How may I help you today?"
        }

    def set_user_language(self, language_code: str) -> None:
        # Set the user's preferred language.
        if language_code in SUPPORTED_LANGUAGES:
            self.user_language = language_code

    def translate_response(self, response: str) -> str:
        # Translate response to user's preferred language.
        if self.user_language != 'en' and response:
            try:
                return self.language_handler.translate_from_english(response, self.user_language)
            except Exception:
                return response
        return response

    def get_data_for_intent(self, intent: str, extracted_info: dict) -> dict:
        # Retrieve relevant data from database based on intent and extracted information.
        try:
            if intent == "car_location" and "car_id" in extracted_info:
                return {"car_location": self.db_handler.get_car_location(extracted_info["car_id"])}
                
            elif intent == "loading_date" and "car_id" in extracted_info:
                return {"loading_date": self.db_handler.get_loading_date(extracted_info["car_id"])}
                
            elif intent == "payment_status" and "membership_id" in extracted_info:
                return {"payment_status": self.db_handler.get_payment_status(extracted_info["membership_id"])}
                
            elif intent == "car_payment" and "car_id" in extracted_info:
                return {"car_payment": self.db_handler.get_car_payment_info(extracted_info["car_id"])}
                
            elif intent == "arrival_date" and "car_id" in extracted_info:
                return {"arrival_date": self.db_handler.get_arrival_date(extracted_info["car_id"])}
                
            return {}
            
        except Exception:
            return {"error": "database_error"}

    def process_message(self, message: str, user_id: str = "default") -> tuple[str, bool]:
        # Check rate limit
        is_allowed, wait_time = self.rate_limiter.is_allowed(user_id)
        if not is_allowed:
            return f"Please wait {wait_time} seconds before sending another message.", False

        # Sanitize input
        message = self.validator.sanitize_text(message)
        if not message:
            return "Invalid input received.", False

        try:
            # Translate input message to English if needed
            if self.user_language != 'en':
                message = self.language_handler.translate_to_english(message)

            # Get intent and extracted information
            intent, extracted_info = self.openai_handler.identify_intent(message)
            
            # Check if this is a farewell/exit intent
            is_exit = intent == "farewell"
            
            # For greeting, use default greeting response
            if intent == "greeting":
                return self.translate_response(self.default_responses["greeting"]), False

            # Check if we need more information
            if extracted_info.get("needs_more_info", False):
                response = self.openai_handler.generate_response(
                    context={"missing_info": extracted_info.get("missing_info")}
                )
                return self.translate_response(response), False

            # Get relevant data from database
            db_data = self.get_data_for_intent(intent, extracted_info)
            
            # Generate response using OpenAI with context
            response = self.openai_handler.generate_response(
                context={
                    "intent": intent,
                    "data": db_data,
                    "previous_context": self.openai_handler.conversation_history
                }
            )
            
            return self.translate_response(response), is_exit

        except ValueError as ve:
            return f"Validation error: {str(ve)}", False
        except Exception as e:
            error_response = self.openai_handler.generate_response(
                context={"error_type": "general", "error_details": str(e)}
            )
            return self.translate_response(error_response), False

def main():
    try:
        # Initialize chatbot
        chatbot = Chatbot()
        
        # Get supported languages
        supported_languages = SUPPORTED_LANGUAGES
        
        # Display language options
        print("\nPlease select your preferred language:")
        for code, language in supported_languages.items():
            print(f"{code}: {language}")
        
        # Get language preference
        user_language = input("\nEnter the language code: ").lower()
        
        # Set user's language preference
        chatbot.set_user_language(user_language)
        
        # Translate and display initial greeting
        greeting = chatbot.translate_response(chatbot.default_responses["greeting"])
        print(f"\nBot: {greeting}")
        
        while True:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
                
            response, should_exit = chatbot.process_message(user_input)
            print(f"Bot: {response}")
            
            # Exit if OpenAI detected a goodbye/farewell intent
            if should_exit:
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()