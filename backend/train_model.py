import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, classification_report
from sklearn.preprocessing import StandardScaler,LabelEncoder
import joblib
import warnings
warnings.filterwarnings("ignore")
df = pd.read_csv(r'C:\Users\krish\OneDrive\Desktop\sneaker-hype-model\backend\stockx_sneaker_data.csv')
df.head()
df.info()
df['Retail Price'] = df['Retail Price'].replace('[\$,]', '', regex=True).astype(float)
df['Sale Price'] = df['Sale Price'].replace('[\$,]', '', regex=True).astype(float)
df['profit'] = df['Sale Price'] - df['Retail Price']
threshold = df['profit'].quantile(0.85)  # top 15% most profitable
df['hyped'] = df['profit'].apply(lambda x: 1 if x > threshold else 0)
print(df[['Retail Price', 'Sale Price', 'profit', 'hyped']])
def extract_year_from_last_two(date_str):
    try:
        date_str = str(date_str).strip()
        last_two = date_str[-2:]
        year = int(last_two)
        return 2000 + year if year <= 25 else 1900 + year
    except:
        return None
print(extract_year_from_last_two("9/24/16"))
df['release_year'] = df['Release Date'].apply(extract_year_from_last_two)
# Split sneaker name into components: brand, model, etc.
df[['brand', 'model', 'edition', 'rest']] = df['Sneaker Name'].str.split('-', n=3, expand=True)
# Encode categorical variables
le_brand = LabelEncoder()
le_model = LabelEncoder()
le_edition = LabelEncoder()

df['brand_encoded'] = le_brand.fit_transform(df['brand'].astype(str))
df['model_encoded'] = le_model.fit_transform(df['model'].astype(str))
df['edition_encoded'] = le_edition.fit_transform(df['edition'].astype(str))
# Final features for ML
features = ['Retail Price', 'Sale Price', 'release_year', 'brand_encoded', 'model_encoded', 'edition_encoded']
X = df[features]
y = df['hyped']
# Drop missing rows
X = X.dropna()
y = y[X.index]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
# Model training
model = RandomForestClassifier(n_estimators=1000, max_depth=10, min_samples_split=5, random_state=42)
model.fit(X_train, y_train)
# Save the trained model
joblib.dump(model, 'sneaker_model.pkl')

print("Model trained and saved as sneaker_model.pkl")
joblib.dump(le_brand, "brand_encoder.pkl")
joblib.dump(le_model, "model_encoder.pkl")
joblib.dump(le_edition, "edition_encoder.pkl")

