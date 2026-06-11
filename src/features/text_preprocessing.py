import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
    

stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Lowercase
    - Remove punctuation and numbers
    """

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    return text


def preprocess_text(text: str) -> str:
    """
    Complete preprocessing pipeline:
    - Clean text
    - Tokenize
    - Remove stopwords
    - Lemmatize
    """

    text = clean_text(text)

    tokens = word_tokenize(text)

    tokens = [
        word
        for word in tokens
        if word not in stop_words
    ]

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return " ".join(tokens)


