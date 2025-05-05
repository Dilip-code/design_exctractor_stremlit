import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro")

st.title("Figma Design to HTML/CSS Generator")

uploaded_file = st.file_uploader("Upload your design image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Design Image", use_column_width=True)

    st.write("Since direct image processing is not supported, please provide a brief description of your design.")
    user_description = st.text_area(
        "Describe your design (e.g., 'A login page with a form on the right and an illustration on the left')",
        placeholder="Add your design description here...",
    )

    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""

    if st.button("Generate HTML/CSS Code"):
        if not user_description.strip():
            st.error("Please provide a description of your design.")
        else:
            with st.spinner("Generating HTML and CSS..."):
                prompt = f"""
                Based on the following design description, generate responsive HTML and CSS code:

                {user_description}

                Requirements:
                - Mobile-friendly
                - Clean, semantic HTML5
                - Properly commented code
                """

                try:
                    response = model.generate_content(prompt)
                    st.session_state.generated_code = response.text

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    if st.session_state.generated_code:
        st.text_area("Generated Code", value=st.session_state.generated_code, height=400)

        st.download_button(
            label="Download HTML/CSS Code",
            data=st.session_state.generated_code,
            file_name="generated_design_code.html",
            mime="text/html",
        )
