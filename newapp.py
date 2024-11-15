import streamlit as st
from groq import Groq
from src.langchainAPI.newSing import ChatChainSingleton
import uuid
#currently works with OpenAi corretly using the singleton class 
#Need to fix various things:
#1) the case that user enters an invalid api key (create some checker before attempting chain I guess) also figure out scenarios where users switches between the apis, currently if wrong api key is entered into openai causes issue (since chain is initialized already? create method maybe to reinitialize in case or research more how to reset a singleton)
#2) begin considering implementation of "New Conversation", see how we plan to implement uploading the session state to our current database
#3)Research to see how to keep the conversation from dissappearing every time new response is being generated (just looks ugly)
#4)make user input box actually clear itself ( currently doesnt and also the issue where if you clear it and then click on the page the conversation dissapears until next submission)
#5) actually implement same singleton for groq (Are we going to widen the examples we are feeding this thing? Currently is set up with focusing on computer science but we wanted to widen scope, add new examples or reword final promp to just be more encompassing?)
#Note: maybe once user enters correct api key and begins conversation , store that conversation separately, make some button that allows them to switch to other service, store each conversation separately and combine them together in a third so they can later view the entire convo with both)
#Probably doesn't matter but, if you just ran openAI and entered api key, if you ask it what was the first message you asked as your first submission it replies one of the examples from the singleton class, not sure if this matters
def format_message(messages):
    formatted = []
    for msg in messages:
        if not isinstance(msg, dict):
            #case that msg is not a dict
            continue
        #check 'role' and 'content' keys are present
        role = msg.get("role", "unknown")
        content = msg.get("content", "[No content available]")
        formatted.append({"role": role, "content": content})
    return formatted

st.title("StarsGPT")
api_choice = st.sidebar.selectbox("Select API Provider", ["Groq", "OpenAI"])

#to store conversation before later saving to database to create "conversation" log
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
#format messages correctly
st.session_state.messages = format_message(st.session_state.messages)

#API key/chat chain initialization
if api_choice == "Groq":
    groqApi = st.sidebar.text_input("Groq API Key", type="password")
    if groqApi:
        client = Groq(api_key=groqApi)
        ChatChainSingleton.input_api_key = groqApi

elif api_choice == "OpenAI":
    openaiApi = st.sidebar.text_input("OpenAI API Key", type="password")
    if openaiApi:
        ChatChainSingleton.model = "gpt-4o-mini"
        ChatChainSingleton.input_api_key = openaiApi
        chat = ChatChainSingleton().chain

    #displaying the conversation
message_container = st.container()
user_input = st.text_area("Please enter your message below:", "")

if st.button("Submit"):
    if user_input:
        with st.spinner("Generating response..."):
            try:
                #add input to session state messages
                st.session_state.messages.append({"role": "user", "content": user_input})

                history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages[:-1]]
                if api_choice == "OpenAI" and openaiApi:
                    #pass session message as input
                    session_id = str(uuid.uuid4())
                    # pass both `input` and `history`
                    response = chat.invoke({"input": user_input, "history": history}, {"configurable": {"session_id": session_id}})
                    
                    #store output from openAI
                    st.session_state.messages.append({"role": "assistant", "content": response.content})

                elif api_choice == "Groq" and groqApi:
                    #Groq scenario, fix and update to also use our example to guide the bot
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=st.session_state.messages,
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=True,
                        stop=None,
                    )
                    response_text = ""
                    for chunk in completion:
                        response_text += chunk.choices[0].delta.content or ""
                    
                    #add input to session state messages
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                #currently shows all messages, maybe set up separate ones for each scenario to keep separate (maybe set up separate for instance but keep and upload into database to mix both convos??)
                with message_container:
                    for msg in st.session_state.messages:
                        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
                user_input = ""
                st.session_state["user_input"] = ""
                #^^ one clears variable but other isn't clearing the actual visual.
            except Exception as e:
                st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a message.")
else:
    if api_choice == "Groq" and not groqApi:
        st.warning("Please enter your Groq API key.")
    elif api_choice == "OpenAI" and not openaiApi:
        st.warning("Please enter your OpenAI API key.")

