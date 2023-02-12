import pandas as pd

def count_sentiment_score(path_data: str, path_stop: str, path_positive: str, path_negative: str) -> int:
    df = pd.read_csv(path_data, sep=";", header=None, names=["tweet", "date"])
    df_positive = pd.read_csv(path_positive, header=None, names=["word"])
    df_negative = pd.read_csv(path_negative, header=None, names=["word"])
    df_stop = pd.read_csv(path_stop, header=None, names=["word"])

    # Lowercase the words, split to get array
    arr_words = df["tweet"].str.lower().str.split()
    words = []

    # Concatenate arrays
    for arr in arr_words:
        words.extend([word for word in arr])

    # Convert to dictionary
    positive_words = { word: 0 for word in df_positive["word"] }
    negative_words = { word: 0 for word in df_negative["word"] }
    stop_words = { word: 0 for word in df_stop["word"] }

    # Remove stop word
    words = [word for word in words if stop_words.get(word) == None]

    # Keep only positive and negative words
    words = [word for word in words if positive_words.get(word) == 0 or negative_words.get(word) == 0]
    score = 0

    for w in words:
        if positive_words.get(w) == 0:
            score += 1
        elif negative_words.get(w) == 0:
            score -= 1

    return score

def main():
    score = count_sentiment_score("./data/trump_tweets.txt", "./data/stop-words.txt", "./data/positive-words.txt", "./data/negative-words.txt")
    print(f"Sentiment score : {score}")

main()
    

    