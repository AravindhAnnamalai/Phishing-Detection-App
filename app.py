import streamlit as st
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re

def is_potential_url(string):
    # Regular expression pattern to match URL-like strings
    url_pattern = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
    )
    return bool(re.match(url_pattern, string))


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
        if is_potential_url(url):
            st.write("Checking...")
            seq = tokenize_url(url, tokenizer)
            pred_val = model.predict(seq)
            if pred_val > 0.5:
                st.error('It is a Phishing Website')
            else:
                st.success('It is a Legitimate Website.')
        else:
            st.write("It's not a proper URL")

if __name__ == "__main__":
    main()
