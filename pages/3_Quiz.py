import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://images.pexels.com/photos/5086477/pexels-photo-5086477.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
            background-size: cover;
            background-position: tile;
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for background and styling
page_bg_img = '''
<style>
h1 {
    color: #ffffff;
    text-align: center;
    padding: 20px;
}
.stRadio > div {
    color: white; 
    background-color: #006eb6;
    border-radius: 10px;
    padding: 10px;
}
.stButton > button {
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    border-radius: 10px;
}
</style>
'''

# Apply the custom CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.title("NASA SDG Quiz")

# Get User Details with unique keys
name = st.text_input("Enter your name:", key="name_input")
# student_id = st.text_input("Enter your ID number:", key="id_input")

# Quiz Questions
questions = [
    "What is the first Sustainable Development Goal (SDG)?",
    "Which SDG focuses on ensuring healthy lives and promoting well-being for all at all ages?",
    "What is the target year for achieving the Sustainable Development Goals",
    "Which SDG addresses climate change and its impacts?",
    "How many Sustainable Development Goals are there in total?",
    "Which SDG focuses on achieving gender equality and empowering all women and girls?",
    "Which SDG promotes access to affordable, reliable, sustainable, and modern energy for all?",
    "The SDG 'Zero Hunger' focuses on what primary goal?",
    "Which SDG is dedicated to promoting sustained, inclusive, and sustainable economic growth?",
    "The SDG 'Life Below Water' is primarily concerned with?"
]

options = [
    ["Zero Hunger", "No Poverty", "Good Health and Well-being", "Quality Education"],
    ["Gender Equality", "Climate Action", "Good Health and Well-being", "Decent Work and Economic Growth"],
    ["2025", "2030", "2040", "2050"],
    ["Life Below Water", "Life on Land", "Responsible Consumption and Production", "Climate Action"],
    ["15", "17", "20", "25"],
    ["Quality Education", "Gender Equality", "Reduced Inequalities", "Peace, Justice, and Strong Institutions"],
    ["Affordable and Clean Energy", "Industry, Innovation, and Infrastructure", "Sustainable Cities and Communities", "Clean Water and Sanitation"],
    ["End hunger and ensure food security", "Promote sustainable agriculture", "Both A and B", "None of the above"],
    ["Decent Work and Economic Growth", "Reduced Inequalities", "Industry, Innovation, and Infrastructure", "Sustainable Cities and Communities"],
    ["Protecting marine ecosystems", "Regulating industrial fishing", "Reducing plastic pollution", "All of the above"]
]

answers = ["No Poverty", "Good Health and Well-being", "2030", "Climate Action", "17", "Gender Equality", "Affordable and Clean Energy", "Both A and B", "Decent Work and Economic Growth", "All of the above"]

# Score Calculation
score = 0

# Quiz only starts if name and ID are provided
if name:
    st.subheader("Answer the following questions:")

    user_answers = []
    for i, question in enumerate(questions):
        user_answer = st.radio(f"{i+1}. {question}", options[i], key=f"question_{i}")
        user_answers.append(user_answer)

    # Submit button
    if st.button("Submit Quiz"):
        # Calculate score
        for i, answer in enumerate(user_answers):
            if answer == answers[i]:
                score += 1
        
        # Display score
        st.markdown(f"<h2 style='color:white;'>Your Score: {score}/10</h2>", unsafe_allow_html=True)
        
        if score >= 7:
            st.balloons()
            st.success(f"Congratulations {name}, you passed! 🎉")
            
            # Generate certificate if score is 7 or above
            def add_text_to_certificate_template(input_pdf, user_name):
                pdf_reader = PdfReader(input_pdf)
                pdf_writer = PdfWriter()

                # Access the first page of the template
                page = pdf_reader.pages[0]

                # Create a BytesIO buffer to store the overlay
                packet = BytesIO()
                canvas_obj = canvas.Canvas(packet)

                custom_font_path = "PinyonScript-Regular.ttf"  # Ensure this path is correct
                pdfmetrics.registerFont(TTFont('PinyonScript-Regular', custom_font_path))

                # Set font and size
                font_name = "PinyonScript-Regular"
                font_size = 45
                canvas_obj.setFont(font_name, font_size)
                canvas_obj.setFillColorRGB(0, 0.157, 0.639)

                # Draw the user's name on the certificate
                canvas_obj.drawString(300, 300, user_name)
                canvas_obj.save()
                packet.seek(0)

                # Merge the overlay with the certificate
                overlay_reader = PdfReader(packet)
                overlay_page = overlay_reader.pages[0]
                page.merge_page(overlay_page)
                pdf_writer.add_page(page)

                # Add remaining pages without modification
                for page in pdf_reader.pages[1:]:
                    pdf_writer.add_page(page)

                # Save the final output to a BytesIO buffer instead of a file
                output_buffer = BytesIO()
                pdf_writer.write(output_buffer)

                # Return the buffer content
                return output_buffer.getvalue()
        
            # Generate certificate as a byte stream
            certificate_pdf = add_text_to_certificate_template("template.pdf", name)
            
            # Provide a download button for the generated certificate
            st.download_button(
                label="📄 Download your Certificate",
                data=certificate_pdf,
                file_name=f"certificate_{name}.pdf",
                mime="application/pdf"
            )
else:
    st.warning("Please enter your name to start the quiz.")
