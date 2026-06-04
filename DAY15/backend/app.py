from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)
CORS(app)

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector database
db = FAISS.load_local(
    "backend/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

@app.route("/")
def home():
    return "RAG Bot Backend Running Successfully!"

@app.route("/test")
def test():

    results = db.similarity_search(
        "What are symptoms of diabetes?",
        k=2
    )

    answer = ""

    for doc in results:
        answer += doc.page_content + "<br><br>"

    return answer

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    query = data["query"]

    results = db.similarity_search(query, k=2)

    answer = ""

    for doc in results:
        answer += doc.page_content + "\n"

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)