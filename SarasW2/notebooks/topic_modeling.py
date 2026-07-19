# topic_modeling.py — run in SageMaker Studio / Jupyter notebook
import boto3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("FeedbackRecords")

items = table.scan()["Items"]
df = pd.DataFrame(items)
negative = df[df["sentiment"] == "NEGATIVE"]["raw_text"]

vectorizer = CountVectorizer(max_df=0.9, min_df=2, stop_words="english")
doc_term_matrix = vectorizer.fit_transform(negative)

lda = LatentDirichletAllocation(n_components=6, random_state=42)
lda.fit(doc_term_matrix)

feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[-10:]]
    print(f"Topic {topic_idx}: {', '.join(top_words)}")
