from nlp_recommender import recommend_products

recommendations = recommend_products("Alice", top_n=3)
for product, score in recommendations:
    print(f"Recommended: {product} - Score: {score}")
