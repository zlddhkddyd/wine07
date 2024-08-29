import pandas as pd
#import openai
import streamlit as st
from openai import OpenAI

# Function to load the CSV file
def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to convert CSV content to text
def csv_to_text(df):
    text = ""
    for _, row in df.iterrows():
        text += " | ".join(map(str, row.values)) + "\n"
    return text

# Function to generate answers using GPT-4
#def generate_answer(api_key, question, context):
#    try:
#        openai.api_key = api_key
#        response = openai.ChatCompletion.create(
#            model="gpt-4",
#            messages=[
#                {"role": "system", "content": "You are a wine expert. Please answer the following question based on the provided information."},
#                {"role": "user", "content": f"Here is the relevant information:\n{context}\n\nQuestion: {question}"}
#            ]
#        )
#        return response['choices'][0]['message']['content']
#    except openai.error.AuthenticationError as e:
#        return f"Authentication error: {str(e)}. Please check your API key."
#    except Exception as e:
#        return f"An error occurred: {str(e)}"


def generate_answer(api_key, question, context):
    try:
        client = OpenAI(api_key=api_key)

        messages=[
                {"role": "system", "content": "You are a wine expert. Please answer the following question based on the provided information."},
                {"role": "user", "content": f"Here is the relevant information:\n{context}\n\nQuestion: {question}"}
            ]

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        #print(response.choices[0].message.content)
        return response.choices[0].message.content
    except:
        pass
    #except OpenAI.error.AuthenticationError as e:
    #    return f"Authentication error: {str(e)}. Please check your API key."
    #except Exception as e:
    #    return f"An error occurred: {str(e)}"


# Streamlit app
def main():
    st.title("Wine Expert Chatbot")
    st.write("Ask any question you have about wine!")

    # Input field for the OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:")

    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        return

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Load CSV and convert to text
        df = load_csv(uploaded_file)
        context = csv_to_text(df)
        
        # Input field for the user's question
        question = st.text_input("Enter your question:")

        if question:
            # Generate the answer
            answer = generate_answer(api_key=api_key, question=question, context=context)
            
            # Display the answer
            st.write(f"Answer: {answer}")

    st.write("To exit, simply close the application.")

if __name__ == "__main__":
    main()
