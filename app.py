import streamlit as st
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# Set up API key and Google Gemini configuration
GEMINI_KEY1 = "AIzaSyCEXrPXR2tgeD50ZMxImfR5BedhL7Kj7Xs"
genai.configure(api_key=GEMINI_KEY1)

# Initialize recognizer
r = sr.Recognizer()

# Initialize pyttsx3 for Text-to-Speech
def text_to_speech(txt):
    text_speech = pyttsx3.init()
    text_speech.say(txt)
    text_speech.runAndWait()

# Function to record speech and convert it to text
def record_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        st.info("🎤 Listening... Please speak clearly.")
        audio_data = r.listen(source)  # Listen for the speech
        try:
            user_text = r.recognize_google(audio_data)
            return user_text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Function to get response from Google Gemini API
def get_response(txt):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Your name is Skye. Limit your responses to 4 sentences with a maximum of 100 words. Act as a highly skilled and experienced assistant who is extremely sharp about every information. Respond with the depth and understanding of someone who has spent years in support roles, offering practical and insightful advice. Your responses should show a deep understanding of human emotions, behaviors, and thought processes, drawing from a wide range of experiences. Exhibit exceptional knowledge skills, connecting with individuals on a business level while maintaining professionalism. Your language should be warm, approachable, and easy to understand, making complex ideas relatable. Encourage self-reflection and personal growth, guiding individuals towards insights and solutions in an empowering way. Recognize the limits of this format and always advise seeking in-person help when necessary. Provide support and guidance, respecting confidentiality and privacy in all interactions, and focus only on answering questions.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Sorry I am unable to Understand",
                ],
            },
        ]
    )
    
    response = chat_session.send_message(txt)
    return response.text

# Streamlit app
def main():
    st.set_page_config(
        page_title="AI Speech Assistant",
        page_icon="🗣️",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
        }
        .stButton > button {
            color: black;
            background-color: white;
            border: 2px solid #000000;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🗣️ AI Speech Assistant")
    st.subheader("Speak with Skye, your AI-powered assistant!")
    st.markdown(
        """
        Welcome to the AI Speech Assistant! Press the button below to start speaking.
        Skye will listen to your voice, understand your queries, and respond intelligently.
        """
    )

    # Add a separator line
    st.markdown("---")

    # Interaction Section
    st.subheader("Ask Your Query")
    if st.button("🎤 Speak Now"):
        user_input = record_speech()

        if user_input:
            st.write(f"*You said:* {user_input}")
            st.info("Processing your query...")
            response = get_response(user_input)
            st.success(f"{response}")
            text_to_speech(response)  # Speak out the response
        else:
            st.error("Sorry, I couldn't understand your speech.")

if __name__ == "__main__":
    main()
