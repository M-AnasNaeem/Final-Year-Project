# validators.py

import re
from typing import Optional, Union

class InputValidator:
    @staticmethod
    def validate_car_id(car_id: Union[str, int]) -> Optional[int]:
        if isinstance(car_id, str):
            # Check if string is numeric and convert to int
            if car_id.isdigit():
                car_id = int(car_id)
            else:
                return None
                
        if isinstance(car_id, int) and 1 <= car_id <= 999999:
            return car_id
        return None

    @staticmethod
    def validate_membership_id(membership_id: str) -> Optional[str]:
        # Check if membership ID matches pattern (8 chars alphanumeric)
        if isinstance(membership_id, str):
            pattern = r'^[A-Za-z0-9]{8}$'
            if re.match(pattern, membership_id):
                return membership_id.upper()
        return None

    @staticmethod
    def sanitize_text(text: str) -> str:
        # Remove any potentially dangerous characters
        if not isinstance(text, str):
            return ""
        # Remove SQL comment sequences and other dangerous characters
        dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'XP_', 'EXEC', 'exec', 'cmd']
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized