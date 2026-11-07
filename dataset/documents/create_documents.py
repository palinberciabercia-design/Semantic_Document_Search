import os

folder = "dataset/documents"
os.makedirs(folder, exist_ok=True)

documents = {
    "doc1.txt": "Artificial Intelligence helps computers perform tasks that require human intelligence.",
    "doc2.txt": "Machine Learning enables computers to learn patterns from data.",
    "doc3.txt": "Deep Learning uses neural networks for image and speech recognition.",
    "doc4.txt": "Python is a programming language used in AI and data science.",
    "doc5.txt": "Cybersecurity protects computers and networks from digital attacks.",
    "doc6.txt": "Cloud Computing provides storage and computing services through the internet.",
    "doc7.txt": "Database Management organizes and stores information using databases.",
    "doc8.txt": "Natural Language Processing helps computers understand human language.",
    "doc9.txt": "Renewable energy includes solar power, wind power, and hydropower.",
    "doc10.txt": "Healthcare technology uses AI to support medical diagnosis."
}

for filename, content in documents.items():
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as file:
        file.write(content)

print("10 documents created successfully!")