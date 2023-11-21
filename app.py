import streamlit as st
import requests
from ast import literal_eval
import time
import streamlit.components.v1 as components


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {st.secrets['API_KEY']}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


def chat_msg_contanier(content, img=None):
    container = st.container()
    container.markdown(content)
    container.image("image_85.jpg", width=300)
    col1, col2 = st.columns(2)
    col1.button("Add to cart", type="secondary")
    col2.button("Buy this", type="primary")


st.title("Personalized shopping assistance")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state['messages'] = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    # TODO: Add conditions based on `role`
    with st.chat_message(message["role"]):
        # chat_msg_contanier(message["content"])
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What is up?"):
    message_placeholder = st.empty()
    # Display user message in chat message container
    output = query({
        "inputs": f"[INST] <<SYS>> You are personalized shopping assistance, output the respone strictly in json format where fields should include 'intent'(only greet or add to cart or remove from cart or list products or buy), 'entities' (must include product, color, quantity, size, age and many more), 'response'<</SYS>> {prompt}. Remember you are personalized shopping assistance [/INST]",
        "parameters": {
            "max_new_tokens": 1000, 
            "temperature": 1,
        }
    })
    output = output[0]['generated_text']
    response = literal_eval(output[output.find("[/INST]")+7:])
    print(response)

    full_response = response['response']

    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        if response['intent'] == "list products":
            chat_msg_contanier(full_response)
        else:
            st.markdown(full_response)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
