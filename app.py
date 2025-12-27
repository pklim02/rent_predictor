import streamlit as st
import json
import pandas as pd
import joblib
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO

# Page Config for a modern look
st.set_page_config(page_title="Rent Predictor", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for dark theme and modern styling
st.markdown("""
    <style>
    /* Dark theme colors */
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #16213e 100%);
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Title styling */
    h1 {
        color: #ffffff !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #b0b0b0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Label styling */
    label {
        color: #e0e0e0 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Slider styling - no track background or filled portion */
    .stSlider [data-baseweb="slider"] {
        background-color: transparent !important;
    }
    
    .stSlider [data-baseweb="slider"] > div > div {
        background-color: transparent !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: transparent !important;
        border: 2px solid #ef4444 !important;
        border-radius: 50% !important;
    }
    
    .stSlider label {
        color: #e0e0e0 !important;
    }
    
    /* Number input styling */
    .stNumberInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #e0e0e0 !important;
    }
    
    /* Button styling - fancy subtle red gradient */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b6b 0%, #ef4444 30%, #dc2626 70%, #c71f1f 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #ff7878 0%, #f55 35%, #e03333 75%, #d11 100%);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
    }
    
    /* Metric display styling */
    .metric-container {
        text-align: center;
        margin: 0 auto;
    }
    
    /* Center all headings */
    h2, h3 {
        text-align: center !important;
    }
    
    /* Center input fields */
    .element-container {
        text-align: center;
    }
    
    /* Center sliders and number inputs */
    .stSlider, .stNumberInput {
        text-align: center;
    }
    
    /* Center radio buttons */
    .stRadio {
        text-align: center;
        display: flex;
        justify-content: center;
    }
    
    /* Center button */
    .stButton {
        text-align: center;
        display: flex;
        justify-content: center;
    }
    
    /* Center columns content */
    [data-testid="column"] {
        text-align: center;
    }
    
    /* Divider styling */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stRadio label {
        color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    model_path = 'rent_app_final'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        st.error(f"Model file '{model_path}' not found!")
        return None

model = load_model()

st.title("🏙️ Apartment Rent Predictor for 27606")
st.markdown('<p class="subtitle">Enter apartment details below to get a rent prediction</p>', unsafe_allow_html=True)

# Initialize session state for prediction
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'input_data' not in st.session_state:
    st.session_state.input_data = None

# --- Prediction Display (Above Inputs) ---
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
if st.session_state.prediction is not None:
    st.markdown(f'<h2 style="background: linear-gradient(135deg, #ff6b6b 0%, #ef4444 50%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-align: center;">Predicted Monthly Rent</h2>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="color: #ffffff; font-size: 3rem; margin: 0; text-align: center;">${st.session_state.prediction:,.2f}</h1>', unsafe_allow_html=True)
else:
    st.markdown(f'<h2 style="background: linear-gradient(135deg, #ff6b6b 0%, #ef4444 50%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; text-align: center;">Predicted Monthly Rent</h2>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="color: #b0b0b0; font-size: 3rem; margin: 0; text-align: center;">Enter details below</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Input Fields with Toggle Options ---
# Square Footage
st.markdown("### Square Footage")
sqft_mode = st.radio("Input method", ["Slider", "Number Input"], key="sqft_mode", horizontal=True, label_visibility="collapsed")
if sqft_mode == "Slider":
    sqft = st.slider("Square Footage (sq ft)", min_value=300, max_value=3000, value=800, step=50, key="sqft_slider")
else:
    sqft = st.number_input("Square Footage (sq ft)", min_value=300, max_value=3000, value=800, step=50, key="sqft_input")

st.markdown("<br>", unsafe_allow_html=True)

# Bedrooms and Bathrooms in columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Bedrooms")
    beds_mode = st.radio("Input method", ["Slider", "Number Input"], key="beds_mode", horizontal=True, label_visibility="collapsed")
    if beds_mode == "Slider":
        beds = st.slider("Bedrooms", 0, 5, 1, key="beds_slider", label_visibility="collapsed")
    else:
        beds = st.number_input("Bedrooms", min_value=0, max_value=5, value=1, step=1, key="beds_input", label_visibility="collapsed")

with col2:
    st.markdown("### Bathrooms")
    baths_mode = st.radio("Input method", ["Slider", "Number Input"], key="baths_mode", horizontal=True, label_visibility="collapsed")
    if baths_mode == "Slider":
        baths = st.slider("Bathrooms", 1.0, 3.0, 1.0, 0.5, key="baths_slider", label_visibility="collapsed")
    else:
        baths = st.number_input("Bathrooms", min_value=1.0, max_value=3.0, value=1.0, step=0.5, key="baths_input", label_visibility="collapsed")

# Prepare data for model (model expects: bed, 'bath ' (with space), sqft)
input_data = {"sqft": sqft, "bed": beds, "bath": baths}

# --- Calculate Prediction ---
if st.button("Calculate Rent", type="primary"):
    if model is not None:
        # Prepare DataFrame with correct feature names (model expects: bed, 'bath ' with trailing space, sqft)
        df = pd.DataFrame([{
            'bed': input_data['bed'],
            'bath ': input_data['bath'],  # Note: trailing space required
            'sqft': input_data['sqft']
        }])
        
        # Make prediction and store in session state
        prediction = model.predict(df)[0]
        st.session_state.prediction = prediction
        st.session_state.input_data = input_data
        
        # Rerun to update the display
        st.rerun()
    else:
        st.error("Model could not be loaded. Please check that 'rent_app_final' exists.")

# Function to generate PDF
def generate_pdf(prediction, input_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("Apartment Rent Prediction Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Predicted Price
    story.append(Paragraph("Predicted Monthly Rent", heading_style))
    story.append(Paragraph(f"<b>${prediction:,.2f}</b>", styles['Normal']))
    story.append(Spacer(1, 0.4*inch))
    
    # Input Parameters
    story.append(Paragraph("Input Parameters", heading_style))
    
    # Create table for input data
    data = [
        ['Parameter', 'Value'],
        ['Square Footage', f"{input_data['sqft']:,} sq ft"],
        ['Bedrooms', str(int(input_data['bed']))],
        ['Bathrooms', str(input_data['bath'])]
    ]
    
    table = Table(data, colWidths=[3*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CC0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer note
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<i>Generated by Apartment Rent Predictor for 27606</i>", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, 
                                        textColor=colors.grey, alignment=1)))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Show download button if prediction exists
if st.session_state.prediction is not None and st.session_state.input_data is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_buffer = generate_pdf(st.session_state.prediction, st.session_state.input_data)
    st.download_button("📥 Download Prediction PDF", pdf_buffer, "rent_prediction.pdf", 
                      mime="application/pdf", use_container_width=True)