# config.py

# OpenAI configuration
OPENAI_CONFIG = {
    'api_key': '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',
    'model': 'gpt-4',
    'temperature': 0,
    'max_tokens': 150
}

# Google Cloud configuration for translations
GOOGLE_CLOUD_CONFIG = {
    'credentials_path': './ict302-chatbot-botbuilders-6e398aa5f91c.json',
    'project_id': 'ict302-chatbot-botbuilders'
}

# Supported languages configuration
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ar': 'Arabic',
    'ur': 'Urdu'
}

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '302@BotBuilders',
    'database': 'BotBuilders'
}