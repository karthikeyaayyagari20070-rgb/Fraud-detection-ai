# Fraud-detection-ai
banking fraud detection application
# 🔒 Banking Fraud Detection System

A comprehensive AI-powered banking fraud detection application built with Python and Streamlit. This system helps identify and prevent banking fraud through advanced AI analysis, pattern recognition, and document verification.

## ✨ Features

### 📄 Document Analysis
- **Document Tampering Detection**: AI-powered analysis to detect alterations and forgery in documents
- **Visual Inspection**: Identifies inconsistencies, artifacts, and manipulation signs using GPT-5 Vision API

### ✍️ Signature Verification
- **Signature Fraud Detection**: Compare signatures to detect forgery
- **Hybrid Analysis**: Combines computer vision (SSIM) and AI-based analysis for accurate results
- **Similarity Scoring**: Provides detailed similarity scores and difference analysis

### 🆔 Identity Verification
- **Aadhaar Verification**: Format validation and visual authenticity checks for Indian Aadhaar cards
- **PAN Verification**: Structure validation and document analysis for PAN cards
- **Multi-level Validation**: Both format-based and AI-powered visual verification

### 👤 KYC Processing
- **Automated Data Extraction**: AI-powered information extraction from identity documents
- **Field Validation**: Automatic validation of extracted data (Aadhaar, PAN, mobile, email, DOB)
- **Confidence Scoring**: Provides confidence and completeness scores for extracted data

### 💰 Transaction Monitoring
- **Pattern Analysis**: Detect unusual transaction patterns and anomalies
- **ML-Based Detection**: Uses Isolation Forest for anomaly detection
- **Risk Scoring**: Comprehensive fraud risk assessment (0-100 scale)
- **Multiple Detection Methods**:
  - Large transaction detection
  - Structuring detection (transactions near reporting thresholds)
  - Round number pattern analysis
  - Time-based pattern detection
  - Rapid succession transaction detection

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/banking-fraud-detection.git
cd banking-fraud-detection
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file and add your OpenAI API key:
```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

Or set it as an environment variable:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

4. Run the application:
```bash
streamlit run app.py --server.port 5000
```

5. Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
banking-fraud-detection/
├── app.py                          # Main Streamlit application
├── fraud_detection_ai.py           # AI-powered fraud detection functions
├── validation_utils.py             # Validation utilities for Indian documents
├── transaction_analysis.py         # Transaction pattern analysis module
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .streamlit/
│   └── config.toml                # Streamlit configuration
└── pages/
    ├── __init__.py                # Pages module initialization
    ├── document_tampering.py      # Document tampering detection page
    ├── signature_fraud.py         # Signature fraud detection page
    ├── aadhaar_verification.py    # Aadhaar verification page
    ├── pan_verification.py        # PAN verification page
    ├── kyc_processing.py          # KYC processing page
    └── transaction_analysis_page.py # Transaction analysis page
```

## 📖 Usage Guide

### Document Tampering Detection
1. Navigate to "Document Tampering" from the sidebar
2. Select the document type
3. Upload the document image (PNG, JPG, JPEG, PDF)
4. Click "Analyze Document"
5. Review the tampering detection results and confidence scores

### Signature Fraud Detection
1. Navigate to "Signature Fraud" from the sidebar
2. Upload the reference (authentic) signature
3. Upload the test signature to verify
4. Click "Compare Signatures"
5. Review similarity scores and analysis

### Aadhaar/PAN Verification
1. Navigate to the respective verification page
2. Choose between number validation or visual verification
3. For number validation: Enter the number and click validate
4. For visual verification: Upload the card image and click verify
5. Review the validation results and extracted information

### KYC Processing
1. Navigate to "KYC Processing"
2. Select the document type
3. Upload the identity document
4. Click "Process KYC Document"
5. Review extracted information and field validations

### Transaction Analysis
1. Navigate to "Transaction Analysis"
2. Upload a CSV file with transaction data or use sample data
3. Click "Analyze Transactions"
4. Review anomalies, alerts, and risk assessment

**CSV Format Example:**
```csv
date,amount,transaction_type,description
2024-01-15,450.00,debit,Amazon
2024-01-16,12000.00,withdrawal,ATM
2024-01-17,8500.00,transfer,Bank Transfer
```

## 🔍 Detection Capabilities

### Document Tampering
- Inconsistent fonts or text alignment
- Color variations and quality differences
- Copy-paste artifacts
- Digital manipulation traces
- Photo editing signs
- Inconsistent lighting or shadows

### Signature Analysis
- Stroke patterns and flow
- Pressure points and line thickness
- Proportions and relative sizes
- Slant and writing angle
- Overall structure and layout

### Transaction Anomalies
- Unusually large transactions
- Structuring patterns
- Round number frequency
- Night-time transactions
- Rapid succession transactions
- ML-detected outliers

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-5, scikit-learn, scikit-image
- **Computer Vision**: OpenCV
- **Data Processing**: Pandas, NumPy
- **Image Processing**: Pillow

## 📊 Risk Assessment Levels

- **🔴 HIGH RISK (70-100)**: Multiple severe anomalies detected, immediate investigation recommended
- **🟡 MEDIUM RISK (40-69)**: Some suspicious patterns found, review recommended
- **🟢 LOW RISK (20-39)**: Minor irregularities detected, routine monitoring sufficient
- **✅ MINIMAL RISK (0-19)**: No significant issues, transactions appear normal

## ⚠️ Important Notes

- This is a detection tool, not a replacement for official verification services
- Always use official government portals for final verification
- Ensure compliance with data protection regulations
- All extracted data should be manually verified
- Ensure images are clear and complete for best results

## 🔐 Security & Privacy

- API keys are stored securely using environment variables
- No data is stored permanently by the application
- All analysis is performed in real-time
- Follow data protection regulations when processing customer information

## 📝 License

This project is for educational and demonstration purposes. Ensure compliance with local banking regulations and data protection laws before using in production.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- OpenAI for GPT-5 Vision API
- Streamlit for the amazing web framework
- scikit-learn for machine learning capabilities

---

**Built with ❤️ using Python and AI**
