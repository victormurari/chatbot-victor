import os
import streamlit as st
import google.generativeai as genai # Import for Gemini API
from google.api_core import exceptions # Import for handling Google API exceptions

# Initialize the Gemini client with the key saved in st.secrets
# Ensure your Gemini API key is configured in st.secrets in Streamlit Cloud
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please ensure 'GEMINI_API_KEY' is set in st.secrets.")
    st.stop() # Stop the app if API key is not configured

def load_txt_files(folder):
    """
    Loads all .txt files from a folder and concatenates them into a single string.

    Args:
        folder (str): The path to the folder containing the .txt files.

    Returns:
        str: A single string containing the content of all .txt files,
             separated by two newlines.
    """
    texts = []
    # Check if the folder exists before attempting to list its contents
    if not os.path.exists(folder):
        st.error(f"Error: The folder '{folder}' was not found. Please create it and add your .txt documents.")
        return "" # Return an empty string if the folder does not exist

    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    texts.append(f.read())
            except Exception as e:
                st.warning(f"Could not read file {file_name}: {e}")
    return "\n\n".join(texts)

# Load base text from the "documentos" folder
# Make sure you have a folder named 'documentos' at the same level as your script
# and that it contains .txt files with Victor Murari's information.
base_text = load_txt_files("documentos") # Changed from "documents" to "documentos"

# Streamlit page configurations
st.set_page_config(page_title="Chat with Victor Murari")
st.title("Chat with Victor Murari")
st.write("Chat with my projects and academic biography.")

# Input field for the user's question
question = st.text_input("Enter your question:")

if question:
    # Display a spinner while the response is being generated
    with st.spinner("Generating response..."):
        try:
            # Create the GenerativeModel instance for the Gemini free tier model
            model = genai.GenerativeModel('gemini-2.0-flash')

            # Make the API call to Gemini to get the response
            response = model.generate_content(
                contents=[
                    {
                        "role": "user",
                        "parts": [
                            {"text": "You are an assistant that answers based on Victor Murari's biography and projects. Use the information below as a basis:\n\n" + base_text},
                            {"text": question}
                        ]
                    }
                ],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7 # Controls the randomness of the response (0.0 to 1.0)
                )
            )
            # Display the model's response
            st.write(response.text)
        except exceptions.ResourceExhausted:
            # Catches the API rate limit error for Gemini
            st.error("API rate limit exceeded. Please try again later.")
        except Exception as e:
            # Catches other errors that may occur during the API call
            st.error(f"An error occurred: {e}. Please check your API key and try again later.")

# Add a footer or additional information, if desired
st.markdown("---")
st.markdown("This chatbot was created to interact with Victor Murari's biography and projects.")
