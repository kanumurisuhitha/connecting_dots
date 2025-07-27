
# Connecting the Dots - PDF Insight Engine 🧠📄

Solution for Adobe's **Connecting the Dots Challenge**. This project reimagines the PDF as an intelligent, interactive experience—helping machines and users understand documents better by extracting structure and meaning.

---

## 🚀 Challenge Overview

### 🔹 Round 1A: Structured Outline Extraction

**Goal:** Automatically extract a structured outline (Title, H1, H2, H3 headings with page numbers) from any PDF file (up to 50 pages).

**Input:** PDF file  
**Output:** A JSON file with structure like:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

### 🔹 Round 1B: Persona-Based Insight Summarizer

**Goal:** Given a user-defined persona and job (like "PhD Researcher in Biology"), extract the top relevant segments from multiple PDFs by semantic similarity.

**Input:**
- A JSON file `persona.json` describing the user intent:
  ```json
  {
    "persona": "PhD Researcher in Biology",
    "job": "Summarize recent techniques in gene editing",
    "documents": ["doc1.pdf", "doc2.pdf"]
  }
  ```

- Multiple PDF files under `/app/input`

**Output:**
- A summary JSON `persona_output.json` with:
  - Top 5 relevant sections
  - Pages and content with scores
  - Document metadata

---

## 🛠️ How It Works

- 🧠 Uses **Sentence-BERT (`all-MiniLM-L6-v2`)** to compute semantic similarity
- 🔍 Extracts blocks from PDFs using `PyMuPDF` (fitz)
- 📈 Scores relevance by comparing user query vector with block vectors
- 📦 Dockerized and works offline with cached model
- ✅ Supports multiple documents and outputs combined ranked insights

---

## 🧪 Example Commands

### 🔧 Build Docker Image

```bash
docker build --platform linux/amd64 -t pdf_insight_engine:dev .
```

### ▶️ Run the container

```bash
docker run --rm   -v "${PWD}/input:/app/input"   -v "${PWD}/output:/app/output"   --network none   pdf_insight_engine:dev
```


## 🧠 Models Used

- **Model:** `all-MiniLM-L6-v2` (pre-downloaded and stored in `cached_model`)
- **Size:** ~90MB (meets Adobe constraint)
- **Inference:** CPU-only, fast and lightweight

---

## ✅ Constraints Met

| Constraint                | Status       |
|---------------------------|--------------|
| ≤ 10s for 50-page PDF     | ✅ Met        |
| ≤ 200MB model size        | ✅ Met (90MB) |
| Works without internet    | ✅ Offline    |
| Docker AMD64 compatible   | ✅ Supported  |
| CPU-based execution       | ✅ Enforced   |

---

## 📜 License

MIT License. For academic and evaluation use.

---

## 🙌 Acknowledgements

Thanks to Adobe for the challenge and inspiration to rethink PDF interaction!
 
