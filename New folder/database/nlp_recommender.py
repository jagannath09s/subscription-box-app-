import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_user_preferences(user_name):
    conn = sqlite3.connect('subscription_box.db')
    cursor = conn.cursor()
    cursor.execute("SELECT preferences FROM users WHERE name = ?", (user_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_products():
    conn = sqlite3.connect('subscription_box.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, tags FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def recommend_products(user_name, top_n=3):
    user_prefs = get_user_preferences(user_name)
    if not user_prefs:
        return f"No preferences found for user: {user_name}"

    product_data = get_all_products()
    texts = [user_prefs] + [tags for _, tags in product_data]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    recommendations = sorted(zip(product_data, similarities), key=lambda x: x[1], reverse=True)

    result = []
    for (name, _), score in recommendations[:top_n]:
        result.append((name, round(score, 2)))

    return result

# Run this only for testing directly
if __name__ == "__main__":
    top_recs = recommend_products("Alice", top_n=3)
    print("Top Recommendations:")
    for name, score in top_recs:
        print(f"{name} (Score: {score})")

