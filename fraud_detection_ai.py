import json
import os
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

# Using python_openai blueprint
# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)


def image_to_base64(image):
    """Convert PIL Image or numpy array to base64 string"""
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def analyze_document_tampering(image, document_type="document"):
    """
    Analyze document for signs of tampering using OpenAI Vision API
    Returns: dict with tampering_detected (bool), confidence (float), issues (list), analysis (str)
    """
    try:
        base64_image = image_to_base64(image)
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a forensic document analysis expert specializing in detecting document fraud and tampering. "
                    + "Analyze documents for signs of manipulation, alterations, inconsistencies, and forgery. "
                    + "Respond with JSON in this format: "
                    + "{'tampering_detected': boolean, 'confidence': number (0-1), 'issues': [list of specific issues found], 'analysis': 'detailed explanation'}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this {document_type} for signs of tampering, forgery, or manipulation. "
                            + "Look for: inconsistent fonts, misaligned text, color variations, copy-paste artifacts, "
                            + "digital manipulation traces, photo editing signs, inconsistent lighting, quality differences, "
                            + "text overlay artifacts, and any other suspicious elements.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048,
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "tampering_detected": False,
            "confidence": 0.0,
            "issues": [],
            "analysis": f"Error analyzing document: {str(e)}"
        }


def analyze_signature_fraud(reference_signature, test_signature):
    """
    Compare two signatures to detect potential fraud
    Uses both computer vision and AI analysis
    Returns: dict with fraud_detected (bool), similarity_score (float), analysis (str)
    """
    try:
        # Convert to grayscale for CV analysis
        if isinstance(reference_signature, Image.Image):
            ref_cv = cv2.cvtColor(np.array(reference_signature), cv2.COLOR_RGB2GRAY)
        else:
            ref_cv = cv2.cvtColor(reference_signature, cv2.COLOR_BGR2GRAY)
            
        if isinstance(test_signature, Image.Image):
            test_cv = cv2.cvtColor(np.array(test_signature), cv2.COLOR_RGB2GRAY)
        else:
            test_cv = cv2.cvtColor(test_signature, cv2.COLOR_BGR2GRAY)
        
        # Resize to same dimensions
        height = max(ref_cv.shape[0], test_cv.shape[0])
        width = max(ref_cv.shape[1], test_cv.shape[1])
        ref_cv = cv2.resize(ref_cv, (width, height))
        test_cv = cv2.resize(test_cv, (width, height))
        
        # Calculate structural similarity
        from skimage.metrics import structural_similarity as ssim
        similarity_score = ssim(ref_cv, test_cv)
        
        # Use AI for detailed analysis
        ref_base64 = image_to_base64(reference_signature)
        test_base64 = image_to_base64(test_signature)
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a forensic handwriting and signature analysis expert. "
                    + "Compare signatures for authenticity and detect potential forgery. "
                    + "Respond with JSON in this format: "
                    + "{'fraud_detected': boolean, 'ai_similarity': number (0-1), 'differences': [list of differences], 'analysis': 'detailed explanation'}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Compare these two signatures. The first is the reference signature, the second is the test signature. "
                            + "Analyze stroke patterns, pressure points, flow, proportions, slant, and overall characteristics. "
                            + "Determine if they appear to be from the same person or if the test signature shows signs of forgery.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{ref_base64}"},
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{test_base64}"},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048,
        )
        
        ai_result = json.loads(response.choices[0].message.content)
        
        # Combine CV and AI results
        combined_similarity = (similarity_score + ai_result.get('ai_similarity', 0.5)) / 2
        fraud_detected = ai_result.get('fraud_detected', False) or similarity_score < 0.6
        
        return {
            "fraud_detected": fraud_detected,
            "cv_similarity_score": float(similarity_score),
            "ai_similarity_score": ai_result.get('ai_similarity', 0.0),
            "combined_similarity": float(combined_similarity),
            "differences": ai_result.get('differences', []),
            "analysis": ai_result.get('analysis', ''),
        }
    except Exception as e:
        return {
            "fraud_detected": False,
            "cv_similarity_score": 0.0,
            "ai_similarity_score": 0.0,
            "combined_similarity": 0.0,
            "differences": [],
            "analysis": f"Error analyzing signatures: {str(e)}"
        }


def extract_kyc_information(document_image, document_type="identity document"):
    """
    Extract KYC information from uploaded documents using AI
    Returns: dict with extracted data and confidence scores
    """
    try:
        base64_image = image_to_base64(document_image)
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a KYC document processing expert. Extract all relevant information from identity documents. "
                    + "Respond with JSON in this format: "
                    + "{'document_type': string, 'extracted_data': {key: value pairs}, 'confidence': number (0-1), 'completeness': number (0-1), 'notes': string}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Extract all KYC information from this {document_type}. "
                            + "Include: full name, date of birth, document number, address, photo details, issue/expiry dates, "
                            + "and any other relevant identification information. Also assess document quality and authenticity.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048,
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "document_type": "unknown",
            "extracted_data": {},
            "confidence": 0.0,
            "completeness": 0.0,
            "notes": f"Error extracting KYC information: {str(e)}"
        }


def verify_aadhaar_visual(aadhaar_image):
    """
    Verify Aadhaar card visually using AI
    Returns: dict with verification result
    """
    try:
        base64_image = image_to_base64(aadhaar_image)
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Indian Aadhaar card verification. "
                    + "Verify Aadhaar cards for authenticity and extract information. "
                    + "Respond with JSON in this format: "
                    + "{'is_valid_aadhaar': boolean, 'aadhaar_number': string or null, 'name': string or null, 'confidence': number (0-1), 'issues': [list], 'analysis': string}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Verify if this is a genuine Aadhaar card. Check for: proper format, UIDAI logo, "
                            + "QR code presence, correct layout, security features, and extract the Aadhaar number and name if visible. "
                            + "The Aadhaar number should be 12 digits, possibly masked.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048,
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "is_valid_aadhaar": False,
            "aadhaar_number": None,
            "name": None,
            "confidence": 0.0,
            "issues": [f"Error: {str(e)}"],
            "analysis": f"Error verifying Aadhaar: {str(e)}"
        }


def verify_pan_visual(pan_image):
    """
    Verify PAN card visually using AI
    Returns: dict with verification result
    """
    try:
        base64_image = image_to_base64(pan_image)
        
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Indian PAN card verification. "
                    + "Verify PAN cards for authenticity and extract information. "
                    + "Respond with JSON in this format: "
                    + "{'is_valid_pan': boolean, 'pan_number': string or null, 'name': string or null, 'father_name': string or null, 'dob': string or null, 'confidence': number (0-1), 'issues': [list], 'analysis': string}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Verify if this is a genuine PAN card. Check for: proper format, Income Tax Department logo, "
                            + "lamination, hologram, correct layout, and extract the PAN number (10 alphanumeric characters), "
                            + "name, father's name, and date of birth if visible.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2048,
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "is_valid_pan": False,
            "pan_number": None,
            "name": None,
            "father_name": None,
            "dob": None,
            "confidence": 0.0,
            "issues": [f"Error: {str(e)}"],
            "analysis": f"Error verifying PAN: {str(e)}"
        }
