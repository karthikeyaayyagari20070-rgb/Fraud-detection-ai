# ==========================================
# AI Banking Fraud Detection & Verification
# ==========================================

import streamlit as st
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import pandas as pd
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ------------------- SAFE IMPORT DEEPFACE -------------------
try:
    from deepface import DeepFace
    deepface_available = True
except Exception as e:
    deepface_available = False

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="AI Banking Fraud Detection", layout="wide")

# ------------------- STYLE -------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #E6ECF0;
        color: #003366;
    }
    [data-testid="stSidebar"] {
        background-color: #003366;
        color: silver;
    }
    [data-testid="stSidebar"] * {
        color: silver !important;
    }
    h1, h2, h3 {
        color: #003366;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- TITLE -------------------
st.title("🏦 AI Banking Fraud Detection & Verification")
st.markdown("---")

# ------------------- SIDEBAR -------------------
st.sidebar.header("📂 Upload Section")
uploaded_file1 = st.sidebar.file_uploader("Upload Original Document/Image", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.sidebar.file_uploader("Upload Suspected Document/Image", type=["jpg", "jpeg", "png"])
verify_faces = st.sidebar.checkbox("Enable Face Verification (Optional)", value=False)

# ------------------- FRAUD RULES -------------------
fraud_rules = """
1. Signature/Document similarity is compared using SSIM (Structural Similarity Index).
2. Face verification uses DeepFace for identity matching (if enabled).
3. Fraud likelihood is based on a similarity threshold of 0.75.
4. All images are processed using OpenCV and compared pixel-by-pixel.
"""

# ------------------- IMAGE SIMILARITY -------------------
def compare_images(img1, img2):
    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(grayA, grayB, full=True)
    return score

# ------------------- PDF REPORT GENERATOR -------------------
def generate_pdf(similarity, result_text, face_verified):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 100, "AI Banking Fraud Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 150, f"Document Similarity Score: {similarity:.2f}")
    c.drawString(50, height - 170, f"Final Result: {result_text}")
    c.drawString(50, height - 190, f"Face Verification: {'Enabled' if verify_faces else 'Disabled'}")
    if verify_faces:
        c.drawString(50, height - 210, f"Face Match Result: {face_verified}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 250, "Fraud Detection Rules Followed:")
    text = c.beginText(50, height - 270)
    text.setFont("Helvetica", 12)
    for line in fraud_rules.strip().split("\n"):
        text.textLine(line.strip())
    c.drawText(text)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 150, "Models Used:")
    c.setFont("Helvetica", 12)
    c.drawString(50, 130, "- OpenCV for image comparison")
    c.drawString(50, 115, "- DeepFace (if enabled) for face verification")
    c.drawString(50, 100, "- SSIM for structural similarity index")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ------------------- MAIN LOGIC -------------------
if uploaded_file1 and uploaded_file2:
    st.subheader("🔍 Image Comparison Result")

    img1 = np.array(Image.open(uploaded_file1).convert("RGB"))
    img2 = np.array(Image.open(uploaded_file2).convert("RGB"))

    # Resize to same size
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    similarity = compare_images(img1, img2)
    result_text = "✅ Documents Match (No Fraud)" if similarity >= 0.75 else "⚠️ Fraud Detected (Mismatch Found)"

    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Original Document", use_container_width=True)
    with col2:
        st.image(img2, caption="Suspected Document", use_container_width=True)

    st.success(f"**Similarity Score:** {similarity:.2f}")
    st.info(result_text)

    # ------------------- FACE VERIFICATION -------------------
    face_verified = "Not Performed"
    if verify_faces and deepface_available:
        try:
            analysis = DeepFace.verify(img1, img2)
            if analysis["verified"]:
                face_verified = "✅ Faces Match"
            else:
                face_verified = "❌ Faces Do Not Match"
            st.write("Face Verification:", face_verified)
        except Exception as e:
            st.warning(f"DeepFace Error: {str(e)}")
            face_verified = "Error during verification"

    # ------------------- GENERATE PDF -------------------
    if st.button("📄 Generate Fraud Detection Report"):
        pdf_buffer = generate_pdf(similarity, result_text, face_verified)
        st.download_button(
            label="Download Report as PDF",
            data=pdf_buffer,
            file_name="Fraud_Detection_Report.pdf",
            mime="application/pdf"
        )

else:
    st.warning("Please upload both the Original and Suspected documents to begin analysis.")
