import streamlit as st
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

# Load the tokenizer from the pickle file
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Load the saved model
model = load_model('model.h5')

def tokenize_url(url, tokenizer, sequence_length=200):
    # Tokenize the URL
    url_sequence = tokenizer.texts_to_sequences([url])
    # Pad the sequence
    padded_sequence = pad_sequences(url_sequence, maxlen=sequence_length)
    return padded_sequence

def main():
    st.title("Phishing URL Checker")
    st.write("Enter the URL below to check if it's phishing or legitimate.")

    url = st.text_input("Enter URL:")

    

    if st.button('Check'):
        if url:
            st.write("Checking...")
            seq = tokenize_url(url, tokenizer)
            pred_val = model.predict(seq)
            if pred_val > 0.5:
                st.error('It is a Phishing Website')
            else:
                st.success('It is a Legitimate Website.')
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()
