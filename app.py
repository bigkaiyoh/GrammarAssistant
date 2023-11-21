import streamlit as st
from openai import OpenAI
import time

#secret keys

api = st.secrets.api_key
assistant_id = st.secrets.assistant_id


#app begins
st.title("Pro Grammar Coach -Nuginy*:。)")


def main():
    if 'client' not in st.session_state:
        st.session_state.client = OpenAI(api_key=api)

        #retrieve the assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.retrieve(assistant_id)

        #Create a thread 
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_q = st.chat_input("Ask Any Grammar Question!")

    if user_q:
        #Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id = st.session_state.thread.id,
            role = "user",
            content = user_q
        )

        #Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.assistant.id
        )

        while True:
                # Wait for 5 seconds
                time.sleep(5)

                # Retrieve the run status
                run_status = st.session_state.client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=run.id
                )

                # If run is completed, get messages
                if run_status.status == 'completed':
                    messages = st.session_state.client.beta.threads.messages.list(
                        thread_id=st.session_state.thread.id
                    )

                    # Loop through messages and print content based on role
                    for msg in reversed(messages.data):
                        role = msg.role
                        content = msg.content[0].text.value
                        st.write(f"{role.capitalize()}: {content}")
                    break
                else:
                    st.write("Waiting for the Assistant to process...")
                    time.sleep(5)

if __name__ == "__main__":
    main()