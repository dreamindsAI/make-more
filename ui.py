# tokenizer_app.py
import streamlit as st
import random

# --- Step 1: Build Malayalam vocab ---
malayalam_chars = [chr(code) for code in range(0x0D00, 0x0D7F + 1)]
malayalam_chars_vocab = {
    tuple(ch.encode("utf-8")): 256 + i for i, ch in enumerate(malayalam_chars)
}

# Reverse mapping (ID -> char)
id_to_char = {v: bytes(k).decode("utf-8") for k, v in malayalam_chars_vocab.items()}

# --- Step 2: Encoding function ---
def encode_text(text: str):
    tokens = []
    raw_bytes = list(text.encode("utf-8"))
    i = 0
    while i < len(raw_bytes):
        if i + 2 < len(raw_bytes):
            key = (raw_bytes[i], raw_bytes[i+1], raw_bytes[i+2])
            if key in malayalam_chars_vocab:
                tokens.append(malayalam_chars_vocab[key])
                i += 3
                continue
        tokens.append(raw_bytes[i])  # keep ASCII/other bytes
        i += 1
    return tokens

# --- Step 3: Decoding function ---
def decode_tokens(tokens: list[int]):
    chars = []
    for t in tokens:
        if t in id_to_char:
            chars.append(id_to_char[t])
        else:
            try:
                chars.append(bytes([t]).decode("utf-8"))
            except:
                chars.append("�")
    return "".join(chars)

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
    for t in tokens:
        if t in id_to_char:
            label = id_to_char[t]
        else:
            label = bytes([t]).decode("utf-8", "ignore")

        hue = (t * 37) % 360
        color = f"hsl({hue}, 70%, 80%)"

        token_html += f'<span style="background-color:{color}; padding:6px 10px; border-radius:12px; font-size:16px; white-space:nowrap;">{label}</span>'
    token_html += "</div>"


    st.markdown(token_html, unsafe_allow_html=True)
