import streamlit as st
import random

st.title("Coin Toss App 🪙")
st.write("Flip a virtual coin and see the result!")

if st.button("Flip Coin"):
    result = random.choice(["Heads", "Tails"])
    st.write(f"The coin landed on **{result}**!")

