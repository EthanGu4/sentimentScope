# Sentiment Scope: Film Edition

End-to-end NLP project that scrapes movie reviews directly from Reddit and applies machine learning to uncover audience sentiment, popular keywords, and recurring themes.

I built this tool to explore how social media reviews align with professional critic ratings, and to practice applying deep learning–based NLP techniques to real-world, noisy data.

## ⚙️ Setup

- Requires Python 3.7+
- Install dependencies: `pip install -r requirements.txt`
- Add your Reddit API credentials to `config.py`


## 🔧 Tech Highlights

Reddit Scraper – Custom-built using Reddit’s API to fetch posts and comments for a given film.

NLP & Sentiment Analysis – Leveraged transformer-based models (HuggingFace/Transformers), PyTorch, and TensorFlow for fine-tuned classification of positive/negative sentiment.

Keyword Extraction – Implemented phrase frequency analysis and filtering to highlight the most common praises and criticisms for each film.

Statistical Comparison – Generated sentiment-derived “audience scores” and compared them against critic ratings to visualize alignment or divergence.

Data Pipeline – Cleaned and preprocessed raw Reddit text with tokenization, stopword removal, and lemmatization using NLTK and spaCy.

Visualization – Displayed sentiment distributions and top keywords with Matplotlib and Seaborn, making results clear and interpretable.

## 🚀 Why I Built It

I wanted to combine my interest in film with hands-on practice in natural language processing, sentiment classification, and data visualization. This project gave me the opportunity to integrate data scraping, ML model training, and real-world evaluation into a single pipeline—while experimenting with both traditional models (scikit-learn classifiers) and state-of-the-art deep learning (transformer architectures).

## Usage

Run `python main.py` and enter a movie name to scrape reviews.
