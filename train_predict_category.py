import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib


# Assuming you have a CSV file with 'Description' and 'Category' columns
csv_file_path = 'C:\\Others\\Wiz3\\report_all.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8')

# Replace NaN values in 'Description' column with an empty string
df['Description'] = df['Description'].fillna('')
df['Category'] = df['Category'].fillna('')

# Shuffle the DataFrame
df = shuffle(df, random_state=42)

# Split the shuffled data into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    df['Description'], df['Category'], test_size=0.2, random_state=42
)

# Create a CountVectorizer to convert text into a bag-of-words representation
vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_data)
test_features = vectorizer.transform(test_data)

# Train a Multinomial Naive Bayes classifier with more loops (adjust as needed)
classifier = MultinomialNB()
for _ in range(1000):  # You can adjust the number of loops (epochs)
    classifier.partial_fit(train_features, train_labels, classes=df['Category'].unique())

# Save the trained model
joblib.dump(classifier, 'C:\\Others\\Wiz3\\trained_model.joblib')
joblib.dump(vectorizer, 'C:\\Others\\Wiz3\\vectorizer.pkl')

# Make predictions on the test set
predictions = classifier.predict(test_features)

# Evaluate the model
accuracy = accuracy_score(test_labels, predictions)
print(f"Accuracy: {accuracy:.2f}")

# Display classification report with zero_division parameter set to 1
print("Classification Report:\n", classification_report(test_labels, predictions, zero_division=1))



