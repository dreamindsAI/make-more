import streamlit as st
import random
from utils import encode_text, decode_token_id



# --- Step 4: UI ---
st.title("Malayalam Tokenizer") 

user_text = st.text_area("", "അഖിൽ")

if st.button("Tokenize") and user_text.strip():
    tokens = encode_text(user_text)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div style="font-size:20px; text-align:center;">Tokens</div>'
            f'<div style="font-size:40px; font-weight:bold; text-align:center;">{len(tokens)}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div style="font-size:20px; text-align:center;">Characters</div>'
            f'<div style="font-size:40px; font-weight:bold; text-align:center;">{len(user_text)}</div>',
            unsafe_allow_html=True
        )



    # CSS styles for tokens
    token_html = '<div style="display:flex; flex-wrap:wrap; gap:4px; align-items:center;">'

    tokens = encode_text(user_text)

    for t in tokens:
        label = decode_token_id(t)
        hue = (t * 37) % 360
        color = f"hsl({hue}, 70%, 80%)"

        token_html += f'<span style="background-color:{color}; padding:6px 10px; border-radius:12px; font-size:16px; white-space:nowrap;">{label}</span>'
    token_html += "</div>"


    st.markdown(token_html, unsafe_allow_html=True)
