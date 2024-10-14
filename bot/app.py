from flask import Flask, request, jsonify, send_from_directory
from docx import Document
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os

app = Flask(__name__, static_folder='./build', static_url_path='/')

# Load the model
model_name = "facebook/bart-large-cnn"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Load .docx file and extract text
def load_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

# Preprocess the text
def preprocess_text(text):
    return re.sub(r'\s+', ' ', text)

# Split text into chunks
def chunk_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Retrieve relevant chunks
def retrieve_relevant_chunks(query, text_chunks):
    vectorizer = TfidfVectorizer().fit_transform([query] + text_chunks)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
    top_indices = cosine_similarities.argsort()[-3:][::-1]
    return " ".join([text_chunks[i] for i in top_indices])

# Summarize chunks
def summarize_chunks(relevant_chunks):
    return summarizer(relevant_chunks, max_length=200, min_length=50, do_sample=True)[0]['summary_text']

# Extract effective date
def extract_effective_date(text):
    date_pattern = r'(\b(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\b|\b(?:\d{4}-\d{2}-\d{2})\b|\b(?:\d{2}/\d{2}/\d{4})\b)'
    match = re.search(date_pattern, text, re.IGNORECASE)
    return match.group(0) if match else "Effective date not found in the document."

# Route to handle document processing
@app.route('/process-document', methods=['POST'])
def process_document():
    query = request.form.get('query')
    document = request.files.get('document')

    if document and query:
        # Load and process the document
        file_path = os.path.join("/tmp", document.filename)
        document.save(file_path)
        docx_text = load_docx(file_path)
        cleaned_text = preprocess_text(docx_text)
        text_chunks = chunk_text(cleaned_text)

        # Retrieve relevant chunks and summarize
        relevant_chunks = retrieve_relevant_chunks(query, text_chunks)
        summary = summarize_chunks(relevant_chunks)

        # Extract effective date
        effective_date = extract_effective_date(docx_text)

        return jsonify({
            'summary': summary,
            'effective_date': effective_date
        })
    return jsonify({'error': 'Invalid request'})

# Serve React app
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
