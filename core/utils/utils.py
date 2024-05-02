import spacy

nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> str:
    """
    Takes text as input, removes punctuation symbols, stop words and lemmatizes the text
    Args:
        text (str): raw text string

    Returns:
        str: lemmatized, stop-word removed, lower-cased text
    """
    # Process text using SpaCy
    doc = nlp(text)

    # Initialize list to store tokens after preprocessing
    preprocessed_tokens = []

    # Iterate through tokens in the document
    for token in doc:
        # Check if token is not a stopword and is alphanumeric
        if not token.is_stop and token.is_alpha:
            # Lowercase token and append to list
            preprocessed_tokens.append(token.lemma_.lower())

    return " ".join(preprocessed_tokens)
