"""Analyse de sentiment et génération de wordcloud."""

import json
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def analyze_comments(path: str):
    """Renvoie le score de polarité moyen et un WordCloud."""
    with open(path, "r", encoding="utf-8") as fh:
        comments = [item["comment"] for item in json.load(fh)]
    polarities = [TextBlob(c).sentiment.polarity for c in comments]
    avg = sum(polarities) / len(polarities) if polarities else 0
    wc = WordCloud(width=600, height=400).generate(" ".join(comments))
    return avg, wc


if __name__ == "__main__":
    score, cloud = analyze_comments("data/lyon_comments.json")
    print("Score moyen:", score)
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()
