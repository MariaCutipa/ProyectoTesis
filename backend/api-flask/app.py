import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from flask import Flask, jsonify, request

app = Flask(__name__)


data = pd.read_csv('cats.csv', delimiter=';')


lemma = WordNetLemmatizer()
en_stopwords = stopwords.words("english")

def clean(text):
    text = re.sub("[^A-Za-z1-9 ]+", "", text)
    text = text.lower()
    tokens = word_tokenize(text)
    clean_list = [lemma.lemmatize(token) for token in tokens if token not in en_stopwords]
    return " ".join(clean_list)


data['Description'] = data['Description'].apply(clean)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['Description'])



@app.route('/api/cats', methods=['GET'])
def get_cats():
    json_data = data[['Cat_Name', 'Breed', 'Personality_Trait', 'Image_Link', 'Backstory', 'Description']].to_dict(orient='records')
    return jsonify(json_data)


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    query = request.args.get('query', '')

    if not query:
        return jsonify({"error": "El parámetro 'query' es obligatorio"}), 400

    
    query_clean = clean(query)
    query_tfidf = vectorizer.transform([query_clean])

    
    similarity = cosine_similarity(query_tfidf, tfidf_matrix)
    similar_cats = list(enumerate(similarity[0]))
    sorted_similar_cats = sorted(similar_cats, key=lambda x: x[1], reverse=True)[:5]

    
    recommendations = []
    for i, score in sorted_similar_cats:
        recommendations.append(data.iloc[i].to_dict())

    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)