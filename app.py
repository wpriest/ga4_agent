import streamlit as st
import requests

st.title("📊 GA4 AI Data Agent")

# Initialiseer chat geschiedenis
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon oude berichten
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input van gebruiker
if prompt := st.chat_input("Vraag iets over je Analytics data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stuur naar n8n
    with st.chat_message("assistant"):
        webhook_url = "JOUW_N8N_WEBHOOK_URL_HIER"
        response = requests.post(webhook_url, json={"query": prompt})
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("output", "Ik kon geen antwoord vinden.")
            st.markdown(answer)
            
            # Als n8n een grafiek-URL meestuurt, toon deze:
            if "image_url" in data:
                st.image(data["image_url"])
                
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Fout bij verbinden met n8n.")
            