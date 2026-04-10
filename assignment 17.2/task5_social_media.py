"""
Task 5 – Social Media Text Data Cleaning and Feature Extraction
================================================================
Use AI-assisted Python scripting to clean and preprocess social media
text data for sentiment analysis.

Steps:
  1. Remove duplicate posts and null text entries.
  2. Clean text by removing URLs, special characters, and extra spaces.
  3. Convert text to lowercase and perform basic tokenization.
  4. Remove stopwords and perform stemming or lemmatization.
  5. Generate basic text features such as word count and sentiment score.
"""

import pandas as pd
import numpy as np
import re
import nltk

# Download required NLTK data (only runs once)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# ── 1. Create sample social media dataset ────────────────────────────────────
raw_data = {
    "post_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 3, 11],
    "user":    ["@alice", "@bob", "@charlie", "@diana", "@eve",
                "@frank", "@grace", "@hank", "@charlie", "@ivy",
                "@charlie", "@jack"],
    "text": [
        "I LOVE this new phone!! 📱🔥🔥 Check it out https://example.com/phone",
        "Terrible    service... never going back!!! #angry #disappointed",
        "Just had the BEST pizza ever 🍕🍕🍕 @PizzaPlace is amazing!!!",
        None,
        "Can't believe how BAD the traffic is today 😡😡 https://t.co/xyz123",
        "  Beautiful day for a walk in the park!!!   Nature is healing 🌳🌸  ",
        "This movie was absolutely WONDERFUL!!! A must-watch @Netflix",
        "Worst experience ever... 0/10 would NOT recommend #fail #terrible",
        "Just had the BEST pizza ever 🍕🍕🍕 @PizzaPlace is amazing!!!",
        "Feeling great today! Life is good. 😊😊",
        "Just had the BEST pizza ever 🍕🍕🍕 @PizzaPlace is amazing!!!",
        None,
    ],
    "likes":     [150, 23, 89, 0, 45, 67, 210, 12, 89, 134, 89, 0],
    "retweets":  [30, 5, 15, 0, 10, 8, 45, 2, 15, 22, 15, 0],
}

posts = pd.DataFrame(raw_data)

# Save raw CSV
posts.to_csv("social_media_posts.csv", index=False)

print("=" * 65)
print("ORIGINAL DATASET")
print("=" * 65)
print(posts)
print(f"\nShape : {posts.shape}")
print(f"Nulls :\n{posts.isnull().sum()}")
print(f"Duplicates (post_id): {posts.duplicated(subset='post_id').sum()}")

# ── 2. Remove null text entries and duplicates ──────────────────────────────
posts = posts.dropna(subset=["text"])
posts = posts.drop_duplicates(subset=["post_id"], keep="first").reset_index(drop=True)
print(f"\n>> Removed nulls & duplicates. New shape: {posts.shape}")

# ── 3. Clean text ───────────────────────────────────────────────────────────
def clean_text(text):
    """Remove URLs, mentions, hashtags symbols, special chars, extra spaces."""
    text = re.sub(r"http\S+|www\.\S+", "", text)        # Remove URLs
    text = re.sub(r"@\w+", "", text)                     # Remove @mentions
    text = re.sub(r"#", "", text)                        # Remove hashtag symbol
    text = re.sub(r"[^\w\s]", "", text)                  # Remove special chars
    text = re.sub(r"\s+", " ", text).strip()             # Collapse whitespace
    return text

posts["cleaned_text"] = posts["text"].apply(clean_text)
print(">> Cleaned text (removed URLs, mentions, special characters).")

# ── 4. Lowercase and tokenize ──────────────────────────────────────────────
posts["cleaned_text"] = posts["cleaned_text"].str.lower()

posts["tokens"] = posts["cleaned_text"].apply(word_tokenize)
print(">> Converted to lowercase and tokenized.")

# ── 5. Remove stopwords and lemmatize ───────────────────────────────────────
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def process_tokens(tokens):
    """Remove stopwords and lemmatize each token."""
    return [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]

posts["processed_tokens"] = posts["tokens"].apply(process_tokens)
print(">> Removed stopwords and applied lemmatization.")

# ── 6. Generate text features ──────────────────────────────────────────────
# Word count (from processed tokens)
posts["word_count"] = posts["processed_tokens"].apply(len)

# Character count of original text
posts["char_count"] = posts["text"].str.len()

# Sentiment score using TextBlob (-1 = negative, 0 = neutral, +1 = positive)
posts["sentiment_score"] = posts["cleaned_text"].apply(
    lambda x: round(TextBlob(x).sentiment.polarity, 3)
)

# Sentiment label
posts["sentiment_label"] = posts["sentiment_score"].apply(
    lambda s: "Positive" if s > 0.1 else ("Negative" if s < -0.1 else "Neutral")
)

print(">> Generated features: word_count, char_count, sentiment_score, sentiment_label.")

# ── 7. Display cleaned dataset ──────────────────────────────────────────────
display_cols = [
    "post_id", "user", "cleaned_text", "processed_tokens",
    "word_count", "sentiment_score", "sentiment_label",
]

print("\n" + "=" * 65)
print("CLEANED & FEATURE-ENRICHED DATASET")
print("=" * 65)
print(posts[display_cols].to_string())

# Save cleaned CSV (drop token lists for CSV compatibility)
save_cols = [
    "post_id", "user", "text", "cleaned_text",
    "word_count", "char_count", "sentiment_score", "sentiment_label",
    "likes", "retweets",
]
posts[save_cols].to_csv("social_media_cleaned.csv", index=False)
print("\n>> Saved cleaned dataset to 'social_media_cleaned.csv'.")
