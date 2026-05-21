<div align="center">

```
███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ██████╗  █████╗  ██████╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║██████╔╝███████║██║  ███╗
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══██╗██╔══██║██║   ██║
██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║  ██║╚██████╔╝
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝
```

### Advanced Multimodal Retrieval-Augmented Generation System

*Upload documents. Ask anything. Get grounded, cited, real-time answers.*

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00C9A7?style=for-the-badge)

</div>

---

## What Is This?

**NeuroRAG** is a production-grade **Multimodal RAG** system that can read PDFs, scanned images, Word documents, and plain text — then answer questions about them with full citations, using both the uploaded knowledge base and live internet search.

It is not a simple chatbot. It is a complete **AI-powered document intelligence pipeline** built with state-of-the-art components.

---

## Live Architecture

```
╔══════════════════════════════════════════════════════════════════════════╗
║                         USER INTERFACE LAYER                            ║
║                    Streamlit · Chat UI · File Upload                    ║
╚══════════════════════╦═══════════════════════════════════════════════════╝
                       ║
          ┌────────────▼─────────────┐
          │     INGESTION LAYER      │
          │  ┌─────────┐ ┌────────┐  │
          │  │ PDF/DOCX│ │  OCR   │  │
          │  │ PyMuPDF │ │EasyOCR │  │
          │  └─────────┘ └────────┘  │
          │  ┌──────────────────────┐ │
          │  │  Gemini Vision API   │ │
          │  │  (Image Reasoning)   │ │
          │  └──────────────────────┘ │
          └────────────┬─────────────┘
                       ║
          ┌────────────▼─────────────┐
          │    PROCESSING LAYER      │
          │                          │
          │  RecursiveCharacter      │
          │  TextSplitter            │
          │  chunk_size=1000         │
          │  overlap=200             │
          └────────────┬─────────────┘
                       ║
          ┌────────────▼─────────────┐
          │    EMBEDDING LAYER       │
          │                          │
          │  BAAI/bge-small-en-v1.5  │
          │  SentenceTransformers    │
          │  dim=384, cosine sim     │
          └────────────┬─────────────┘
                       ║
          ┌────────────▼─────────────┐
          │    VECTOR DATABASE       │
          │                          │
          │  ┌────────────────────┐  │
          │  │       Qdrant       │  │
          │  │  localhost:6333    │  │
          │  │  cosine distance   │  │
          │  └────────────────────┘  │
          └────────────┬─────────────┘
                       ║
     ╔═════════════════▼══════════════════╗
     ║       ADVANCED RETRIEVAL           ║
     ║                                    ║
     ║  ┌─────────────────────────────┐   ║
     ║  │  1. Query Rewriting         │   ║
     ║  │     Gemini 2.5 Flash        │   ║
     ║  │     vague → precise query   │   ║
     ║  └──────────────┬──────────────┘   ║
     ║                 ║                  ║
     ║  ┌──────────────▼──────────────┐   ║
     ║  │  2. Hybrid Search           │   ║
     ║  │  ┌──────────┐ ┌──────────┐  │   ║
     ║  │  │  Vector  │ │  BM25    │  │   ║
     ║  │  │  Search  │ │ Keyword  │  │   ║
     ║  │  └────┬─────┘ └────┬─────┘  │   ║
     ║  │       └──────┬──────┘        │   ║
     ║  │          Combined             │   ║
     ║  └──────────────┬──────────────┘   ║
     ║                 ║                  ║
     ║  ┌──────────────▼──────────────┐   ║
     ║  │  3. Cross-Encoder Reranking │   ║
     ║  │  ms-marco-MiniLM-L-6-v2     │   ║
     ║  │  Top-3 most relevant chunks │   ║
     ║  └──────────────┬──────────────┘   ║
     ║                 ║                  ║
     ║  ┌──────────────▼──────────────┐   ║
     ║  │  4. Web Search Fusion       │   ║
     ║  │  Tavily API · max_results=3 │   ║
     ║  │  Local Docs + Live Web      │   ║
     ║  └──────────────┬──────────────┘   ║
     ╚═════════════════╬══════════════════╝
                       ║
          ┌────────────▼─────────────┐
          │    GENERATION LAYER      │
          │                          │
          │   Gemini 2.5 Flash       │
          │   Context-grounded       │
          │   Anti-hallucination     │
          └────────────┬─────────────┘
                       ║
          ┌────────────▼─────────────┐
          │    CITATION LAYER        │
          │                          │
          │  Source File + Chunk ID  │
          │  Web URLs                │
          │  Traceable References    │
          └──────────────────────────┘
```

---

## Key Features

| Feature | Description |
|---|---|
| **Multimodal Input** | PDFs, DOCX, TXT, PNG, JPG — all supported |
| **OCR Engine** | EasyOCR extracts text from scanned documents and images |
| **Vision Understanding** | Gemini Vision reasons over charts, diagrams, screenshots |
| **Semantic Chunking** | LangChain RecursiveCharacterTextSplitter with 200-token overlap |
| **Vector Search** | BAAI/bge-small-en-v1.5 embeddings stored in Qdrant |
| **Hybrid Retrieval** | Dense vector search + BM25 sparse keyword search combined |
| **Query Rewriting** | Gemini rewrites vague queries for better retrieval accuracy |
| **Cross-Encoder Reranking** | ms-marco-MiniLM-L-6-v2 re-scores top chunks by relevance |
| **Live Web Search** | Tavily API fuses real-time web results with local knowledge |
| **Citation System** | Every answer references exact source files and chunk IDs |
| **Session Memory** | Full conversation history maintained across turns |
| **Custom UI** | Particle-animated dark-mode Streamlit interface |

<p>Temporary LLM API key is disabled due to API limit</p>
---

## Folder Structure

```
advanced-multimodal-rag/
│
├── app/                          # Core backend logic
│   │
│   ├── ingestion/                # Document parsing & extraction
│   │   ├── __init__.py
│   │   ├── parser.py             # PDF + DOCX text extraction (PyMuPDF, python-docx)
│   │   ├── ocr.py                # EasyOCR for images and scanned docs
│   │   └── image_extractor.py    # Extract embedded images from PDFs
│   │
│   ├── llm/                      # Language model integrations
│   │   ├── __init__.py
│   │   ├── generator.py          # Gemini 2.5 Flash answer generation
│   │   └── vision.py             # Gemini Vision for image understanding
│   │
│   └── rag/                      # Full RAG pipeline
│       ├── __init__.py
│       ├── chunker.py            # RecursiveCharacterTextSplitter
│       ├── embedder.py           # BAAI/bge-small-en-v1.5 embeddings
│       ├── pipeline.py           # Chunk + embed + prepare data
│       ├── qdrant_db.py          # Qdrant vector DB operations
│       ├── query_rewriter.py     # Gemini-powered query improvement
│       ├── hybrid_search.py      # BM25 keyword search
│       ├── advanced_rag.py       # Query rewrite + vector search + rerank
│       ├── reranker.py           # CrossEncoder reranking
│       ├── web_search.py         # Tavily real-time web search
│       ├── rag_chain.py          # Full end-to-end RAG chain
│       └── citations.py          # Citation generation from contexts
│
├── frontend/
│   └── streamlit_app.py          # Streamlit chat UI
│
├── data/
│   ├── uploads/                  # User uploaded files
│   ├── processed/                # Extracted images and processed content
│   └── vectordb/                 # Local vector storage (optional)
│
├── .env                          # API keys (not committed)
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Chat UI, file upload, session memory |
| **LLM** | Gemini 2.5 Flash | Query rewriting, answer generation |
| **Vision** | Gemini Vision API | Image and chart understanding |
| **Embeddings** | BAAI/bge-small-en-v1.5 | Semantic vector generation |
| **Vector DB** | Qdrant | Fast cosine similarity search |
| **Reranker** | ms-marco-MiniLM-L-6-v2 | Cross-encoder result reranking |
| **OCR** | EasyOCR | Scanned document text extraction |
| **Chunking** | LangChain | Recursive text splitting |
| **Web Search** | Tavily API | Real-time internet search |
| **PDF Parsing** | PyMuPDF (fitz) | Fast PDF text + image extraction |
| **DOCX Parsing** | python-docx | Word document text extraction |
| **Containerization** | Docker | Qdrant vector database server |

---

## Setup & Installation

### 1 · Clone the Repository

```bash
git clone https://github.com/your-username/advanced-multimodal-rag.git
cd advanced-multimodal-rag
```

### 2 · Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3 · Install Dependencies

```bash
pip install -r requirements.txt
```

### 4 · Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys:
- Gemini API → [Google AI Studio](https://aistudio.google.com/)
- Tavily API → [Tavily](https://tavily.com/)

### 5 · Start Qdrant with Docker

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Verify it's running:

```
http://localhost:6333/dashboard
```

### 6 · Run the Application

```bash
streamlit run frontend/streamlit_app.py
```

Open your browser at `http://localhost:8501`

---

## How It Works — Step by Step

```
Step 1   Upload a PDF, DOCX, image, or TXT file via the UI
         └─► File is saved to data/uploads/

Step 2   Parser detects the file type
         ├─► PDF    → PyMuPDF extracts text page by page
         ├─► DOCX   → python-docx extracts paragraphs
         ├─► Image  → EasyOCR reads all visible text
         └─► TXT    → Direct read

Step 3   Text is chunked into 1000-character pieces (200 overlap)
         └─► Each chunk tagged with source filename + chunk ID

Step 4   Chunks are embedded with BAAI/bge-small-en-v1.5 (384-dim vectors)
         └─► Stored in Qdrant with metadata payload

Step 5   User asks a question in the chat

Step 6   Query is rewritten by Gemini 2.5 Flash for better retrieval

Step 7   Hybrid retrieval runs:
         ├─► Vector search in Qdrant (top-k cosine similarity)
         └─► BM25 keyword search over stored chunks

Step 8   CrossEncoder reranks all retrieved chunks by relevance score

Step 9   Tavily fetches 3 live web results and appends them to context

Step 10  Gemini 2.5 Flash generates a grounded answer using only the context

Step 11  Citations are extracted from metadata and displayed with the answer
```

---

## Example Queries

```
"Summarize the key findings in this research paper"
"What does the financial report say about Q3 revenue?"
"Extract all table data from the uploaded PDF"
"What is the latest news about this topic?"
"Compare what the document says vs current web information"
"Find all mentions of risk factors across uploaded documents"
```

---

## Use Cases

- **Research Assistant** — Chat with academic papers and technical reports
- **Enterprise Knowledge Base** — Internal document QA with citations
- **Legal Document Review** — Extract clauses and references from contracts
- **Financial Analysis** — Query annual reports and earnings documents
- **Medical Literature** — Retrieve information from clinical documents
- **Customer Support** — Product manual and policy document retrieval

---

## Requirements

```txt
streamlit
google-generativeai
qdrant-client
sentence-transformers
langchain-text-splitters
rank-bm25
pymupdf
python-docx
easyocr
Pillow
tavily-python
python-dotenv
```

---

## Roadmap

- [ ] Graph RAG for entity-relationship retrieval
- [ ] Multi-agent agentic workflows
- [ ] Table-aware structured data extraction
- [ ] Audio and video input support
- [ ] Redis caching for faster responses
- [ ] Cloud deployment (AWS / GCP)
- [ ] User authentication and multi-tenant support
- [ ] REST API layer for external integrations

---

## Why This Architecture?

**Hybrid Search** combines the strength of semantic similarity (vector) with exact keyword matching (BM25). Neither alone is sufficient — together they dramatically improve recall.

**Query Rewriting** compensates for the fact that users rarely phrase queries the way documents are written. Rewriting bridges that vocabulary gap before retrieval happens.

**Cross-Encoder Reranking** is more accurate than bi-encoder retrieval alone because it can attend to both query and document simultaneously. Using it as a second stage keeps latency low while maximizing precision.

**Web Fusion** ensures answers are never limited to uploaded documents. Live web results are appended to context so Gemini can synthesize both sources.

**Citations** make every answer explainable and auditable — essential for enterprise and academic use cases.

---

<div align="center">

---

Made with love ❤️ by **Dhruv Devaliya** · *Bit-Bard*

[![Email](https://img.shields.io/badge/Email-dhruvdevaliya%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:dhruvdevaliya@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dhruv_Devaliya-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dhruv-devaliya/)

*If this project helped you, consider giving it a ⭐ on GitHub*

---

</div>
