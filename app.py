import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

AUTOSAGE_PROMPT = """
You are AutoSage, an expert AI assistant specialized in two-wheelers and four-wheelers.

Your task is to provide accurate, clear, and structured vehicle information.

When a user asks a question, respond with:
- Vehicle name
- Brand
- Vehicle type (Bike / Car / EV / Hybrid)
- Key features
- Mileage or range
- Approximate price (India)
- Maintenance tips
- Eco-friendliness insight (if applicable)

Keep the response simple, informative, and user-friendly.
"""
def get_autosage_response(user_query, image_file=None):
    # Always start with text
    contents = [
        AUTOSAGE_PROMPT + "\nUser Query: " + user_query
    ]

    # If image is uploaded, add it correctly
    if image_file is not None:
        image_bytes = image_file.getvalue()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_file.type
        )

        contents.append(image_part)

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=contents
    )

    return response.text

# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="AutoSage App", page_icon="🚗")
st.sidebar.title("🚗 AutoSage")
st.sidebar.info(
    "AutoSage helps you explore vehicle details, comparisons, "
    "maintenance tips, and eco-friendly options using AI."
)


st.title("🚗 AutoSage")
st.subheader("AI Vehicle Expert using Gemini Flash")

st.write(
    "Ask anything about bikes, cars, EVs, mileage, prices, or maintenance."
)

user_query = st.text_input(
    "Enter your vehicle query",
    placeholder="Example: Best bikes under 2 lakhs in India"
)

uploaded_image = st.file_uploader(
    "Upload a vehicle image (optional)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Vehicle Image", use_column_width=True)


if st.button("Get Vehicle Info"):
    if user_query.strip() == "":
        st.warning("Please enter a query")
    else:
        with st.spinner("AutoSage is analyzing..."):
            response = get_autosage_response(user_query, uploaded_image)

        st.success("Here is your result:")
        st.write(response)
