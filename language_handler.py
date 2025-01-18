# language_handler.py

from translation_config import configure_google_cloud
from config import SUPPORTED_LANGUAGES

class LanguageHandler:
    def __init__(self):
        # Initialize the language handler with the Google Cloud Translation client
        self.supported_languages = SUPPORTED_LANGUAGES
        try:
            self.translate_client = configure_google_cloud()
            print("Translation service initialized successfully")
        except Exception as e:
            print(f"Failed to initialize translation service: {str(e)}")
            self.translate_client = None

    def get_supported_languages(self):
        # Return the dictionary of supported languages
        return self.supported_languages

    def is_translation_available(self):
        # Check if translation service is available
        return self.translate_client is not None

    def detect_language(self, text):
        # Detect the language of the given text
        if not self.is_translation_available():
            print("Translation service unavailable, defaulting to English")
            return 'en'
        
        try:
            result = self.translate_client.detect_language(text)
            return result['language']
        except Exception as e:
            print(f"Language detection failed: {str(e)}")
            return 'en'

    def translate_text(self, text, target_language):
        # Translate text to target language
        if not text:
            return text
            
        if not self.is_translation_available():
            print("Translation service unavailable, returning original text")
            return text
            
        if target_language not in self.supported_languages:
            print(f"Unsupported language: {target_language}")
            return text
        
        try:
            result = self.translate_client.translate(
                text,
                target_language=target_language,
                source_language=None  # Auto-detect source language
            )
            return result['translatedText']
        except Exception as e:
            print(f"Translation failed: {str(e)}")
            return text

    def translate_to_english(self, text, source_language=None):
        # Translate text to English
        if not text:
            return text
            
        if source_language == 'en':
            return text
            
        return self.translate_text(text, 'en')

    def translate_from_english(self, text, target_language):
        # Translate English text to target language
        if not text:
            return text
            
        if target_language == 'en':
            return text
            
        return self.translate_text(text, target_language)