
import pandas as pd
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load existing ChromaDB
vectorstore = Chroma(
    persist_directory="./chroma_db",
    collection_name="semantic_documents",
    embedding_function=embeddings
)

# 15 queries from different topics
queries = [
    "What is artificial intelligence?",
    "How do computers learn from information?",
    "Explain neural networks",
    "Which programming language is useful for AI?",
    "How can digital systems be protected?",
    "What are online computing services?",
    "How is information stored and organized?",
    "How do computers understand human language?",
    "What are alternative sources of electricity?",
    "How can technology help doctors?",
    "Explain machine learning applications",
    "What is speech recognition?",
    "How does cloud storage work?",
    "What is data security?",
    "How can sunlight generate electricity?"
]

results = []
scores = []

# Search for each query
for query in queries:
    documents = vectorstore.similarity_search_with_score(
        query, k=5
    )

    print("\nQuery:", query)

    for rank, (doc, distance) in enumerate(documents, start=1):
        print(f"\nRank: {rank}")
        print("Document:", doc.page_content)
        print("Source:", doc.metadata.get("source"))
        print("Distance:", distance)

        results.append({
            "Query": query,
            "Rank": rank,
            "Document": doc.page_content,
            "Source": doc.metadata.get("source"),
            "Distance": distance
        })

        scores.append({
            "Query": query,
            "Rank": rank,
            "Source": doc.metadata.get("source"),
            "Distance": distance
        })

# Save CSV files
pd.DataFrame(results).to_csv(
    "dataset/search_results.csv", index=False
)

pd.DataFrame(scores).to_csv(
    "dataset/similarity_scores.csv", index=False
)

print("\nAll searches completed!")
print("Search results saved to CSV files.")

import os
import re

# Keyword-based search
keyword_results = []

for query in queries:
    query_words = set(re.findall(r"\w+", query.lower()))

    matching_documents = []

    for filename in os.listdir("dataset/documents"):
        if filename.endswith(".txt"):
            filepath = os.path.join("dataset/documents", filename)

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            document_words = set(
                re.findall(r"\w+", content.lower())
            )

            # Count matching words
            match_count = len(query_words & document_words)

            if match_count > 0:
                matching_documents.append(
                    (filename, content, match_count)
                )

    # Sort by number of matching words
    matching_documents.sort(
        key=lambda item: item[2],
        reverse=True
    )

    for rank, (filename, content, count) in enumerate(
        matching_documents[:5], start=1
    ):
        keyword_results.append({
            "Query": query,
            "Rank": rank,
            "Source": filename,
            "Document": content,
            "Matching_Words": count
        })

# Save keyword results
keyword_df = pd.DataFrame(keyword_results)

keyword_df.to_csv(
    "dataset/keyword_results.csv",
    index=False
)

print("Keyword search completed!")
print("Keyword results saved successfully.")

# Compare search methods
comparison = []

for query in queries:
    semantic_sources = [
        item["Source"]
        for item in results
        if item["Query"] == query
    ]

    keyword_sources = [
        item["Source"]
        for item in keyword_results
        if item["Query"] == query
    ]

    comparison.append({
        "Query": query,
        "Semantic_Search": ", ".join(semantic_sources),
        "Keyword_Search": ", ".join(keyword_sources)
    })

pd.DataFrame(comparison).to_csv(
    "dataset/search_comparison.csv",
    index=False
)

print("Comparison completed!")
print("Results saved in search_comparison.csv")
