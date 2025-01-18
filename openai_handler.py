# openai_handler.py

from openai import OpenAI
import json
from typing import Dict, Any, Tuple
from config import OPENAI_CONFIG

class OpenAIHandler:
    def __init__(self):
        # Initialize OpenAI handler with configuration parameters.
        self.client = OpenAI(api_key=OPENAI_CONFIG['api_key'])
        self.model = OPENAI_CONFIG['model']
        self.temperature = OPENAI_CONFIG['temperature']
        self.max_tokens = OPENAI_CONFIG['max_tokens']
        self.conversation_history = []
        
        # System prompt for better conversation flow and intent detection
        self.system_prompt = """
        You are a helpful customer service agent for an autoshipping company, Nejoum al Jazeera. 
        Engage in natural, flowing conversation while helping customers with their queries.

        You can help with:
        1. Car location (requires car_id)
        2. Loading dates/schedule (requires car_id)
        3. Payment status (requires membership_id)
        4. Car payment details (requires car_id)
        5. Arrival information/dates (requires car_id)

        When identifying intents, use these specific categories:
        - car_location
        - loading_date
        - payment_status
        - car_payment
        - arrival_date
        - greeting
        - farewell
        - unknown

        When asking for IDs:
        - Always use "Car ID" instead of "car_id"
        - Always use "Membership ID" instead of "membership_id"

        Guidelines:
        - Match "Car Payment Details" to 'car_payment' intent
        - Match "Arrival Information" to 'arrival_date' intent
        - Maintain a natural conversation flow
        - Remember context from previous messages
        - When specific information is needed, ask for it politely
        - If a question is asked and the required ID (membership_id or car_id) is not provided in the same prompt, ask for it in terms that you need it, not that you have searched the database and havent gotten any information.
        - If after searching trying to retrieve the data, no data is found ask the user to confirm whether the entered ID is correct.
        - Show empathy and understanding in responses
        - Provide relevant follow-up information when appropriate
        - Handle greetings and farewells in a friendly manner
        - For farewell intents, recognize them regardless of phrasing
        - If you encounter errors, explain them clearly and offer solutions

        Important: When identifying intents, carefully analyze if the user is trying to end the conversation.
        This could be through various expressions in any language that convey:
        - Saying goodbye
        - Wanting to end the conversation
        - Expressing thanks and indication of finishing
        - Any cultural variations of farewell

        ID Formats:
        - car_id: numeric only
        - membership_id: 8 characters alphanumeric
        """

    def add_message_to_history(self, role: str, content: str) -> None:
        # Add a message to conversation history with context management.
        self.conversation_history.append({"role": role, "content": content})
        # Keep last 10 messages for context
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def identify_intent(self, message: str) -> Tuple[str, Dict[str, Any]]:
        # Use OpenAI to identify intent and extract relevant information
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history,
                {"role": "user", "content": message}
            ]

            tools = [{
                "type": "function",
                "function": {
                    "name": "process_customer_request",
                    "description": "Process customer service request and identify required information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "intent": {
                                "type": "string",
                                "enum": ["car_location", "loading_date", "payment_status", 
                                       "car_payment", "arrival_date", "greeting", "farewell", "unknown"]
                            },
                            "car_id": {"type": "string"},
                            "membership_id": {"type": "string"},
                            "needs_more_info": {"type": "boolean"},
                            "missing_info": {"type": "string"},
                            "conversation_context": {"type": "object"}
                        },
                        "required": ["intent"]
                    }
                }
            }]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                tools=tools,
                tool_choice={"type": "function", "function": {"name": "process_customer_request"}}
            )

            function_response = json.loads(
                response.choices[0].message.tool_calls[0].function.arguments
            )

            self.add_message_to_history("user", message)
            content = response.choices[0].message.content if response.choices[0].message.content else ""
            self.add_message_to_history("assistant", content)

            return function_response["intent"], function_response

        except Exception as e:
            print(f"Error in intent identification: {str(e)}")
            return "unknown", {}

    def generate_response(self, context: Dict[str, Any] = None) -> str:
        # Generate a natural language response with improved context and flow.
        try:
            # Create a context-aware prompt
            if context:
                context_str = self._format_context(context)
            else:
                context_str = "No additional context provided."
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history,
                {"role": "user", "content": f"Please generate a natural conversational response based on this context: {context_str}"}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            response_text = response.choices[0].message.content
            self.add_message_to_history("assistant", response_text)
            
            return response_text

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return self._generate_error_response(str(e))

    def _format_context(self, context: Dict[str, Any]) -> str:
        # Format context data for better response generation.
        if "error_type" in context:
            return self._format_error_context(context)
        elif "intent" in context and context["intent"] == "farewell":
            return "Generate a friendly farewell response that maintains conversation history context."
        else:
            return json.dumps(context, indent=2)

    def _format_error_context(self, context: Dict[str, Any]) -> str:
        # Format error context for better error responses.
        error_type = context.get("error_type", "general")
        error_details = context.get("error_details", "Unknown error")
        return f"Error type: {error_type}, Details: {error_details}"

    def _generate_error_response(self, error_details: str) -> str:
        # Generate an error response.
        return f"I apologize, but I encountered an issue while processing your request. Please try again, and if the problem persists, let me know so I can help you in a different way. Technical details: {error_details}"