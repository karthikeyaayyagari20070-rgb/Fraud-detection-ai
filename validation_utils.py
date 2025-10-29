import re
from datetime import datetime


def validate_aadhaar_format(aadhaar_number):
    """
    Validate Aadhaar number format
    Aadhaar: 12-digit number
    Returns: dict with is_valid, message, formatted_number
    """
    if not aadhaar_number:
        return {
            "is_valid": False,
            "message": "Aadhaar number is required",
            "formatted_number": None
        }
    
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', str(aadhaar_number))
    
    # Check if it's exactly 12 digits
    if not re.match(r'^\d{12}$', cleaned):
        return {
            "is_valid": False,
            "message": "Aadhaar number must be exactly 12 digits",
            "formatted_number": None
        }
    
    # Check if all digits are same (invalid pattern)
    if len(set(cleaned)) == 1:
        return {
            "is_valid": False,
            "message": "Invalid Aadhaar number pattern",
            "formatted_number": None
        }
    
    # Format: XXXX XXXX XXXX
    formatted = f"{cleaned[0:4]} {cleaned[4:8]} {cleaned[8:12]}"
    
    return {
        "is_valid": True,
        "message": "Valid Aadhaar format",
        "formatted_number": formatted
    }


def validate_pan_format(pan_number):
    """
    Validate PAN card number format
    PAN: 10 alphanumeric characters (ABCDE1234F)
    Format: 5 letters + 4 digits + 1 letter
    Returns: dict with is_valid, message, formatted_number
    """
    if not pan_number:
        return {
            "is_valid": False,
            "message": "PAN number is required",
            "formatted_number": None
        }
    
    # Remove spaces and convert to uppercase
    cleaned = re.sub(r'\s', '', str(pan_number)).upper()
    
    # PAN format: [A-Z]{5}[0-9]{4}[A-Z]{1}
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    
    if not re.match(pan_pattern, cleaned):
        return {
            "is_valid": False,
            "message": "PAN must be 10 characters: 5 letters + 4 digits + 1 letter (e.g., ABCDE1234F)",
            "formatted_number": None
        }
    
    # Additional validation: 4th character indicates person type
    # P - Individual, C - Company, H - HUF, F - Firm, etc.
    person_type_codes = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']
    if cleaned[3] not in person_type_codes:
        return {
            "is_valid": False,
            "message": "Invalid PAN structure (4th character must be P/C/H/F/A/T/B/L/J/G)",
            "formatted_number": None
        }
    
    return {
        "is_valid": True,
        "message": "Valid PAN format",
        "formatted_number": cleaned,
        "person_type": get_pan_person_type(cleaned[3])
    }


def get_pan_person_type(code):
    """Get person type from PAN 4th character"""
    types = {
        'P': 'Individual',
        'C': 'Company',
        'H': 'Hindu Undivided Family (HUF)',
        'F': 'Firm',
        'A': 'Association of Persons (AOP)',
        'T': 'Trust',
        'B': 'Body of Individuals (BOI)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'G': 'Government'
    }
    return types.get(code, 'Unknown')


def validate_indian_mobile(mobile_number):
    """
    Validate Indian mobile number
    Format: 10 digits starting with 6-9
    Returns: dict with is_valid, message, formatted_number
    """
    if not mobile_number:
        return {
            "is_valid": False,
            "message": "Mobile number is required",
            "formatted_number": None
        }
    
    # Remove spaces, dashes, and +91
    cleaned = re.sub(r'[\s\-\+]', '', str(mobile_number))
    if cleaned.startswith('91'):
        cleaned = cleaned[2:]
    
    # Check if it's exactly 10 digits and starts with 6-9
    if not re.match(r'^[6-9]\d{9}$', cleaned):
        return {
            "is_valid": False,
            "message": "Mobile number must be 10 digits starting with 6-9",
            "formatted_number": None
        }
    
    formatted = f"+91 {cleaned[0:5]} {cleaned[5:10]}"
    
    return {
        "is_valid": True,
        "message": "Valid mobile number",
        "formatted_number": formatted
    }


def validate_email(email):
    """
    Validate email address
    Returns: dict with is_valid, message
    """
    if not email:
        return {
            "is_valid": False,
            "message": "Email is required"
        }
    
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return {
            "is_valid": False,
            "message": "Invalid email format"
        }
    
    return {
        "is_valid": True,
        "message": "Valid email format"
    }


def validate_date_of_birth(dob_string, min_age=18, max_age=100):
    """
    Validate date of birth
    Accepts formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    Returns: dict with is_valid, message, age, formatted_date
    """
    if not dob_string:
        return {
            "is_valid": False,
            "message": "Date of birth is required",
            "age": None,
            "formatted_date": None
        }
    
    # Try different date formats
    formats = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y']
    parsed_date = None
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(str(dob_string), fmt)
            break
        except ValueError:
            continue
    
    if not parsed_date:
        return {
            "is_valid": False,
            "message": "Invalid date format. Use DD/MM/YYYY or DD-MM-YYYY",
            "age": None,
            "formatted_date": None
        }
    
    # Calculate age
    today = datetime.now()
    age = today.year - parsed_date.year - ((today.month, today.day) < (parsed_date.month, parsed_date.day))
    
    # Check if date is in future
    if parsed_date > today:
        return {
            "is_valid": False,
            "message": "Date of birth cannot be in the future",
            "age": None,
            "formatted_date": None
        }
    
    # Check age constraints
    if age < min_age:
        return {
            "is_valid": False,
            "message": f"Age must be at least {min_age} years",
            "age": age,
            "formatted_date": parsed_date.strftime('%d/%m/%Y')
        }
    
    if age > max_age:
        return {
            "is_valid": False,
            "message": f"Age cannot exceed {max_age} years",
            "age": age,
            "formatted_date": parsed_date.strftime('%d/%m/%Y')
        }
    
    return {
        "is_valid": True,
        "message": "Valid date of birth",
        "age": age,
        "formatted_date": parsed_date.strftime('%d/%m/%Y')
    }
