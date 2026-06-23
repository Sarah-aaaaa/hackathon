import streamlit as st
import requests as rp
import time
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# initialise role
if "role" not in st.session_state:
    st.session_state.role = "youth"


#ollama
def get_ai_response(messages):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3:latest",
        "messages":messages,
        "stream":False
    }

    try:
        response = rp.post(url, json=data, timeout=60)
        return response.json()["message"]["content"]

    except Exception as e:
        return f"Error: {e}"
    

def generate_summary(messages):
    url = "http://localhost:11434/api/chat"

    prompt = [
        {
            "role": "user",
            "content": "Summarise this conversation in 2-3 sentences for a social worker. Focus on emotional state , concerns, and issues."
        }
    ]
    data = {
        "model": "llama3:latest",
        "messages": prompt + messages,
        "stream": False
    }

    response = rp.post(url, json=data)
    return response.json()["message"]["content"]

def youth_ai():       
#title      
    st.title("Youth support Chatbot")

    #show old msg
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


    # new msg
    user_input=st.chat_input("Say something")

    #save new msg
    if user_input:
        st.session_state.messages.append({"role":"user", "content":user_input})

            # show loading BEFORE calling AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_reply = get_ai_response(st.session_state.messages)
                st.write(ai_reply)

        st.session_state.messages.append({"role":"assistant", "content":ai_reply})

        st.rerun() 

def worker_mode():
    st.title("Worker Dashboard")

    if st.button("Generate Summary"):
        summary = generate_summary(st.session_state.messages)
        st.write(summary)

    st.subheader("Chat History")

    for msg in st.session_state.messages:
        st.write(f"{msg['role']}: {msg['content']}")


#login
st.sidebar.subheader("Access")
pw_input = st.sidebar.text_input("password")

if st.sidebar.button("login"):
    if pw_input == "worker123":
        st.session_state.role = "worker"
        st.sidebar.success("login as worker")
    else:
        st.sidebar.error("wrong password")
        
if st.session_state.role == "worker":
    worker_mode()
else:
    youth_ai()
