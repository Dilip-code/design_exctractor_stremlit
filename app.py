import streamlit as st
from openai import OpenAI
from PIL import Image

gpt4o = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

    if st.button("Generate HTML/CSS Code"):
        if not user_description.strip():
            st.error("Please provide a description of your design.")
        else:
            with st.spinner("Generating HTML and CSS..."):
                prompt = f"""
                Based on the following design description, generate responsive HTML and CSS code:
                {user_description}
                
                Ensure the code is:
                - Mobile-friendly
                - Cleanly formatted
                - Uses semantic HTML5 elements
                - Includes comments explaining the code
                
                The design description: {user_description}
                """
                try:
                    response = gpt4o.chat.completions.create(
                    model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a front-end development assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.7,
                        max_tokens=1500,
                    )

                    response_content: int = response.choices[0].message.content

                    st.text_area("Generated Code", value=response_content, height=400)

                    st.download_button(
                        label="Download HTML/CSS Code",
                        data=response_content,
                        file_name="generated_design_code.html",
                        mime="text/html",
                    )

                except Exception as e:
                    st.error(f"An error occurred: {e}")
