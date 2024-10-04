import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
from dotenv import load_dotenv
import os


# Set Streamlit page configuration
st.set_page_config(
    page_title="Ask Question About SDG",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key is properly loaded
if GOOGLE_API_KEY is None:
    st.error("API Key is not set in the environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona: You are a Sustainable Development Goals (SDG) specialist, focused on the 17 SDG Goals. Your role is to provide information and guidance strictly related to these goals in a way that is easy for school-going kids to understand."
        "if user query reach 3 politely encourage the user to attempt a quiz. If a user asks something unrelated to SDG and its 17 Goals, politely inform them that you can only provide information related to the SDGs."
        "Tone: Always keep your answers brief, clear, and simple for school-going kids."
    )
)

# Function to get response from the chatbot
def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text.strip()


# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://images.pexels.com/photos/2538107/pexels-photo-2538107.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
            background-size: cover;
            opacity: 1;
            background-position: tile;
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)

# Load and display a custom header image (optional)
def load_header():
    header_html = """
    <div style="padding:10px;border-radius:10px;text-align:center;">
        <h2 style="color:white;margin:0;">Sustainable Development Goals Bot</h2>
        <p style="color:yellow;margin:0;">Ask me anything about SDG Goals!</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Initialize session state for chat history and form visibility
if "history" not in st.session_state:
    st.session_state.history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False

user_avatar_url = "https://img.freepik.com/premium-photo/cartoon-character-with-glasses-book-called-character_14117-15190.jpg?w=1380"
bot_avatar_url = "https://img.freepik.com/premium-photo/cartoon-man-with-glasses-brown-briefcase_14117-9631.jpg?w=1380"

# Function to display chat messages
def display_chat_history():
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center;">
                        <div style="background-color: #075e54; color: white; padding: 10px; border-radius: 10px; max-width: 70%; ">
                            <p style="margin: 0;"><b>You:</b> {chat['content']}</p>
                        </div>
                        <img src="{user_avatar_url}" style="width: 60px; height: 50px; border-radius: 60%; margin-left: 10px;"/>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="{bot_avatar_url}" style="width: 60px; height: 50px; border-radius: 60%; margin-right: 10px;">
                    <div style="background-color: #128c7E; color: white; padding: 10px; border-radius: 10px; max-width: 70%;">
                        <p style="margin: 0;"><b>Bot:</b> {chat['content']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)


# Main application layout
def main():
    load_header()
    st.write("")  # Add spacing

    with st.container():
        display_chat_history()

        # User input area
        with st.form(key="user_input_form", clear_on_submit=True):
            user_input = st.text_input(
                label="",
                placeholder="Type your message here...",
                max_chars=500
            )
            submit_button = st.form_submit_button(label="Send")

            if submit_button and user_input.strip():
                with st.spinner("Thinking..."):
                    bot_response = get_chatbot_response(user_input)
                
                # Update chat history
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "bot", "content": bot_response})
                
                # Display the user question and bot response
                st.write(f"""
                <div style="color: yellow">
                        <p>Q: {user_input}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"""
                <div style="color: white">
                        <p>{bot_response}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                
# Footer with provided link
# st.markdown("""
#     <p style="text-align:center; color:white; margin-top:50px;">
#         Check out the <a href="https://live-appointment-chatbot20.zapier.app/" target="_blank" style="color:#34c759;">Live Appointment</a>.
#     </p>
# """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()