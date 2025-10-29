# ==========================================
# AI Banking Fraud Detection & Verification
# ==========================================

import os
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# ---------- SAFE OPENCV IMPORT ----------
try:
    import cv2
    os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
except ImportError:
    st.warning("⚠️ OpenCV not available. Some image features may be limited.")

# ---------- DEEPFACE IMPORT HANDLING ----------
try:
    from deepface import DeepFace
    deepface_available = True
except Exception:
    deepface_available = False
    st.warning("⚠️ DeepFace not available in this environment.")

# ---------- TENSORFLOW SETUP (optional use only) ----------
try:
    import tensorflow as tf
    tf.get_logger().setLevel('ERROR')
except Exception:
    st.warning("⚠️ TensorFlow not available. Using fallback logic.")

# ---------- APP TITLE ----------
st.markdown(
    "<h1 style='color:#1E90FF;text-align:center;'>AI Banking Fraud Detection & Verification</h1>",
    unsafe_allow_html=True
)
st.write("### Intelligent system for document and image-based fraud analysis.")
