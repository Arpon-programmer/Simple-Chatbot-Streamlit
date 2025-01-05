import streamlit as st
import json
from typing import List, Dict
from main import load_knowledge_base, save_knowledge_base, find_best_match, get_answer_for_question

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = load_knowledge_base('knowledge_base.json')

def display_messages():
    """Display all messages in the chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_user_input(user_input: str) -> str:
    """Process user input and return bot response"""
    # Find best matching question
    best_match = find_best_match(
        user_input, 
        [q["question"] for q in st.session_state.knowledge_base["questions"]]
    )
    
    if best_match:
        return get_answer_for_question(best_match, st.session_state.knowledge_base)
    return None

def add_new_knowledge(question: str, answer: str):
    """Add new question-answer pair to knowledge base"""
    st.session_state.knowledge_base["questions"].append({
        "question": question,
        "answer": answer
    })
    save_knowledge_base('knowledge_base.json', st.session_state.knowledge_base)

def main():
    st.title("AI Assistant Chat")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    display_messages()

    # Chat input
    if prompt := st.chat_input("What can I help you with?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        response = process_user_input(prompt)
        
        # If no response found, ask for new knowledge
        if not response:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I don't know the answer. Would you like to teach me?"
            })
            
            # Create columns for the form
            col1, col2 = st.columns(2)
            
            with col1:
                new_answer = st.text_input("Type the answer:", key="new_answer")
            with col2:
                if st.button("Add Answer"):
                    if new_answer and new_answer.lower() != 'skip':
                        add_new_knowledge(prompt, new_answer)
                        response = new_answer
                        st.success("Thank you! I learned a new response!")
                    st.rerun()
        
        # Display assistant response
        if response:
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response
            })

    # Add a clear chat button in sidebar
    with st.sidebar:
        st.title("Chat Controls")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
