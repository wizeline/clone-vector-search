import spacy

nlp = spacy.load("en_core_web_sm")


def preprocess_text(text) -> str:
    """
    preprocess_text takes text as input, removes punctuation symbols, stop words and lemmatizes the text
    :param text: raw text string
    :return: lemmatized, stop-word removed, lower-cased text
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
