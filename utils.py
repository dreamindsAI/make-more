import pickle

with open("malayalam_chars_mapping.pkl", "rb") as f:
    MALAYALAM_CHARS_MAPPING = pickle.load(f)

with open("malayalam_syllabeles_mapping.pkl", "rb") as f:
    MALAYALAM_SYLLABELES_MAPPING = pickle.load(f)

with open("merged_chars_mapping.pkl", "rb") as f:
    MERGED_CHARS_MAPPING = pickle.load(f)

with open("vocabulary.pkl", "rb") as f:
    VOCABULARY = pickle.load(f)


def merge_malayalam_char_tokens(tokens: list[int]) -> list[int]:
    """Merge UTF-8 byte sequences into new vocab ids for Malayalam characters"""
    merged_tokens = []
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens):  # check if 3 bytes available
            key = (tokens[i], tokens[i+1], tokens[i+2])
            value = MALAYALAM_CHARS_MAPPING.get(key)
            if value is not None:
                merged_tokens.append(value)
                i += 3
                continue
        # fallback: keep single byte
        merged_tokens.append(tokens[i])
        i += 1
    return merged_tokens

def merge_malayalam_syllabele_tokens(tokens: list[int]) -> list[int]:
    """Merge UTF-8 byte sequences into new vocab ids for Malayalam characters"""
    merged_tokens = []
    i = 0
    while i < len(tokens):
        if i + 5 < len(tokens):  # check if 3 bytes available
            key = (tokens[i], tokens[i+1], tokens[i+2], tokens[i+3], tokens[i+4], tokens[i+5])
            value = MALAYALAM_SYLLABELES_MAPPING.get(key)
            if value is not None:
                merged_tokens.append(value)
                i += 6
                continue
        # fallback: keep single byte
        merged_tokens.append(tokens[i])
        i += 1
    return merged_tokens

def merge_pair(tokens, pair_to_merge, new_idx):
    """Merge common pairs to create new pairs"""
    merged_tokens = []
    i = 0
    while i < len(tokens):
        if i < len(tokens)-1 and (tokens[i], tokens[i+1]) == pair_to_merge:
            merged_tokens.append(new_idx)
            i += 2
        else:
            merged_tokens.append(tokens[i])
            i += 1
    return merged_tokens


def encode_text(text: str) -> list[int]:

    tokens = list(text.encode("utf-8")) # text of list of ids 0-225
    tokens = merge_malayalam_syllabele_tokens(tokens) # Merge malayalam syllabele tokens
    tokens = merge_malayalam_char_tokens(tokens) # Merge malayalam char tokens

    for pair_to_merge, new_idx in MERGED_CHARS_MAPPING.items():
        tokens = merge_pair(tokens, pair_to_merge, new_idx)
    
    return tokens

def decode_token_id(id):
    if id < 256:
        return chr(id)
    else:
        return VOCABULARY.get(id)

        