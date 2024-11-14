import openai
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

openai.api_key = ""

st.set_page_config(page_title="Charlsgpt - Your Personal Chatbot", layout="wide")

# CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #4A90E2;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #333;
        margin-bottom: 20px;
    }
    .message {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        font-size: 18px;
    }
    .user-message {
        background-color: #bbdefb;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: right;
        font-size: 18px;
    }
    .send-button {
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
    }
    .send-button:hover {
        background-color: #357ABD;
    }
    .input-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    .input-box {
        flex-grow: 1;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
        border: 1px solid #ccc;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.markdown('<div class="title">Welcome to Charlsgpt 🤖</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<h2>User Feedback</h2>', unsafe_allow_html=True)
    feedback = st.text_area("Your feedback:")
    submit_feedback = st.button("Submit Feedback")

    # Handle feedback submission
    if submit_feedback and feedback:
        try:
            # Email configuration
            sender_email = "charlsgptfeedback@gmail.com"
            receiver_email = "charlztf19@gmail.com"
            password = "kmrs oego hpqm eclp"  # Replace with your email password

            # Email server setup
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)

            # Create email content
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "User Feedback for Charlsgpt"
            message.attach(MIMEText(feedback, "plain"))

            # Send email
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            st.success("Thank you for your feedback! It has been sent successfully.")
        except Exception as e:
            st.error(f"An error occurred while sending feedback: {str(e)}")

st.markdown('<div class="subtitle">I\'m your personal assistant. How can I assist you today?</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        if chat['sender'] == 'You':
            st.markdown(f'<div class="user-message"><strong>{chat["sender"]}:</strong> {chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message"><strong>{chat["sender"]}:</strong> {chat["message"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_message = st.text_input("", key="user_input", label_visibility="collapsed", placeholder="Type your message here...", value=st.session_state.input_text)
send_button = st.button("Send")

if send_button and user_message.strip():
    st.session_state.chat_history.append({"sender": "You", "message": user_message})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response['choices'][0]['message']['content'].strip()
        st.session_state.chat_history.append({"sender": "Charlsgpt", "message": bot_reply})
    except Exception as e:
        st.session_state.chat_history.append({"sender": "Charlsgpt", "message": f"Error: {str(e)}"})

    st.session_state.input_text = ""
