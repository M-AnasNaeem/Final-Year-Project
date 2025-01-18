from flask import Flask, request, jsonify, send_from_directory
from openai_handler import OpenAIHandler
from database_handler import DatabaseHandler
from config import DB_CONFIG
from language_handler import LanguageHandler
from rate_limiter import RateLimiter

app = Flask(__name__)

# Initialize handlers
openai_handler = OpenAIHandler()
db_handler = DatabaseHandler(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)
language_handler = LanguageHandler()
rate_limiter = RateLimiter()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        user_language = data.get('language', 'en')
        
        # If it's the initial greeting
        if message == "GREETING":
            greeting = "Hello! I am a ChatBot from Nejoum Al Jazeera. How may I help you today?"
            if user_language != 'en':
                greeting = language_handler.translate_from_english(greeting, user_language)
            return jsonify({'response': greeting})

        # For regular messages
        if user_language != 'en':
            # Translate user message to English for processing
            english_message = language_handler.translate_to_english(message)
            # Process message and get response in English
            intent, context = openai_handler.identify_intent(english_message)
            # Add language to context
            context['language'] = user_language
            english_response = handle_intent(intent, context, db_handler)
            return jsonify({'response': english_response})  # Response is already translated in handle_intent
        else:
            # Process English messages normally
            intent, context = openai_handler.identify_intent(message)
            context['language'] = user_language
            response = handle_intent(intent, context, db_handler)
            return jsonify({'response': response})

    except Exception as e:
        print(f"Error processing chat request: {str(e)}")
        error_message = "I apologize, but I encountered an error. Please try again."
        if user_language != 'en':
            error_message = language_handler.translate_from_english(error_message, user_language)
        return jsonify({
            'error': 'Internal server error',
            'response': error_message
        }), 500

def handle_intent(intent, context, db):
    try:
        # First get the database information
        data = {}
        
        if intent == 'car_location':
            if 'car_id' in context:
                data = db.get_car_location(context['car_id'])
            
        elif intent == 'loading_date' or intent == 'loading_schedule':
            if 'car_id' in context:
                date = db.get_loading_date(context['car_id'])
                data = {"loading_date": date} if date else {}
                
        elif intent == 'payment_status':
            if 'membership_id' in context:
                data = db.get_payment_status(context['membership_id'])
                
        elif intent == 'car_payment' or intent == 'car_payment_details':
            if 'car_id' in context:
                data = db.get_car_payment_info(context['car_id'])
                
        elif intent == 'arrival_date' or intent == 'arrival_information':
            if 'car_id' in context:
                date = db.get_arrival_date(context['car_id'])
                data = {"arrival_date": date} if date else {}

        # Map database field names to user-friendly terms
        user_friendly_context = {
            "intent": intent,
            "data": data,
            "Car ID": context.get('car_id'),
            "Membership ID": context.get('membership_id')
        }
        
        # Get response from OpenAI
        response = openai_handler.generate_response(user_friendly_context)

        # Translate if needed
        user_language = context.get('language', 'en')
        if user_language != 'en':
            response = language_handler.translate_from_english(response, user_language)
            
        return response

    except Exception as e:
        print(f"Error handling intent {intent}: {str(e)}")
        error_msg = "I apologize, but I encountered an error processing your request. Please try again."
        if context.get('language', 'en') != 'en':
            error_msg = language_handler.translate_from_english(error_msg, context['language'])
        return error_msg

@app.route('/')
def serve_app():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/set-language', methods=['POST'])
def set_language():
    try:
        data = request.json
        language = data.get('language', 'en')
        
        # Store language preference (you might want to store this in a session or database)
        session['language'] = language
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/translate-options', methods=['POST'])
def translate_options():
    try:
        data = request.json
        options = data.get('options', [])
        target_language = data.get('language', 'en')
        
        if target_language == 'en':
            return jsonify({'translated_options': options})
            
        translated_options = [
            language_handler.translate_from_english(option, target_language)
            for option in options
        ]
        
        return jsonify({'translated_options': translated_options})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
