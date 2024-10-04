import streamlit as st
import os

# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://images.pexels.com/photos/4644812/pexels-photo-4644812.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
            background-size: cover;
            opacity: 0.9;
            background-position: tile;
            background-attachment: fixed;
        }
        .stImage {
            border-style: solid;
            border-right-style: solid;
            border-width: 5px;
            border-color: red;
        }
    </style>
""", unsafe_allow_html=True)

images_folder = os.path.join(os.getcwd(), "images")

images = [
    os.path.join(images_folder, 'goal-01.jpg'),
    os.path.join(images_folder, 'goal-02.jpg'),
    os.path.join(images_folder, 'goal-03.jpg'),
    os.path.join(images_folder, 'goal-04.jpg'),
    os.path.join(images_folder, 'goal-05.jpg'),
    os.path.join(images_folder, 'goal-06.jpg'),
    os.path.join(images_folder, 'goal-07.jpg'),
    os.path.join(images_folder, 'goal-08.jpg'),
    os.path.join(images_folder, 'goal-09.jpg'),
    os.path.join(images_folder, 'goal-10.jpg'),
    os.path.join(images_folder, 'goal-11.jpg'),
    os.path.join(images_folder, 'goal-12.jpg'),
    os.path.join(images_folder, 'goal-13.jpg'),
    os.path.join(images_folder, 'goal-14.jpg'),
    os.path.join(images_folder, 'goal-15.jpg'),
    os.path.join(images_folder, 'goal-16.jpg'),
    os.path.join(images_folder, 'goal-17.jpg'),
]

for image_path in images:
    if not os.path.exists(image_path):
        st.error(f"Image not found: {image_path}")


# Function to display the slideshow
def image_slideshow():
    # Initialize a session state variable to track the current image index
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    # Display the current image with custom width
    st.image(images[st.session_state.current_index], width=695)  # Set your desired width

    # Create two buttons for Previous and Next
    col1, col3 = st.columns([9, 1])
    with col1:
        if st.button("Previous"):
            st.session_state.current_index = (st.session_state.current_index - 0 - 1) % len(images)
    with col3:
        if st.button("Next"):
            st.session_state.current_index = (st.session_state.current_index + 0 + 1) % len(images)

# Run the slideshow
image_slideshow()

