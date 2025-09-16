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
st.title("🎨 Malayalam Tokenizer Visualizer")

user_text = st.text_area("Enter text", "അഖിൽ loves AI")

if st.button("Tokenize"):
    tokens = encode_text(user_text)

    st.subheader("Token Visualization")

    # CSS styles for tokens
    token_html = ""
    for t in tokens:
        if t in id_to_char:
            label = id_to_char[t]
        else:
            label = bytes([t]).decode("utf-8", "ignore")

        # Random pastel color
        color = f"hsl({random.randint(0, 360)}, 70%, 80%)"

        token_html += f"""
        <span style="
            background-color:{color};
            padding:6px 10px;
            border-radius:12px;
            margin:4px;
            display:inline-block;
            font-size:16px;
        ">
            {label} <small style="color:#555;">({t})</small>
        </span>
        """

    st.markdown(token_html, unsafe_allow_html=True)

    st.subheader("Decoded Back")
    st.write(decode_tokens(tokens))
