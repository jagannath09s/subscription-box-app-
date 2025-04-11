import pandas as pd
from sklearn.neighbors import NearestNeighbors

class BoxRecommender:
    def __init__(self, user_data_path, product_data_path):
        self.user_data = pd.read_csv("data/user_preferences.csv")
        self.product_data = pd.read_csv("data/products.csv")

        self.product_data.columns = self.product_data.columns.str.strip().str.lower()
        self.product_data.rename(columns={'product_category_name': 'category', 'product_link': 'link'}, inplace=True)

        # Map detailed categories to general ones
        self.category_mapping = {
            'beauty': ['makeup', 'skincare', 'fragrance', 'hair', 'nails'],
            'fitness': ['fitness', 'workout', 'exercise'],
            'food': ['snacks', 'nutrition', 'superfoods'],
            'tech': ['gadgets', 'electronics', 'devices'],
            'lifestyle': ['home', 'wellness', 'accessories', 'travel']
        }

        self.model = NearestNeighbors(n_neighbors=3, metric='euclidean')
        self.model.fit(self.user_data.drop('user_id', axis=1))

    def map_to_general_category(self, cat_name):
        cat_name = str(cat_name).lower()
        for general, keywords in self.category_mapping.items():
            for keyword in keywords:
                if keyword in cat_name:
                    return general
        return None  # unmatched

    def recommend(self, user_preferences):
        distances, indices = self.model.kneighbors([user_preferences])
        similar_users = self.user_data.iloc[indices[0]]
        avg_preferences = similar_users.drop('user_id', axis=1).mean()
        top_categories = avg_preferences.sort_values(ascending=False).index.tolist()[:3]

        # Add mapped category to product_data
        self.product_data['general_category'] = self.product_data['category'].apply(self.map_to_general_category)

        recommendations = []
        for cat in top_categories:
            matched = self.product_data[self.product_data['general_category'] == cat]
            selected = matched.head(2)
            for _, row in selected.iterrows():
                recommendations.append({
                    'product_name': row.get('product_name', 'Unnamed Product'),
                    'category': cat.capitalize(),
                    'link': row.get('link', '#')
                })

        return recommendations
