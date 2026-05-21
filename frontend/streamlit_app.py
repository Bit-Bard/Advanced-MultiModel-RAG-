import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app")
    )
)

import streamlit as st
from ingestion.parser import extract_pdf_text, extract_docx_text
from ingestion.ocr import extract_text_from_image
from rag.pipeline import process_document
from rag.qdrant_db import create_collection, upload_data
from rag.rag_chain import ask_question

# ══════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════

st.set_page_config(
    page_title="NeuroRAG",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════
#  SESSION STATE  (init once)
# ══════════════════════════════════════════

if "messages"      not in st.session_state: st.session_state.messages      = []
if "query_count"   not in st.session_state: st.session_state.query_count   = 0
if "indexed_files" not in st.session_state: st.session_state.indexed_files = set()

os.makedirs("data/uploads", exist_ok=True)

# ══════════════════════════════════════════
#  STYLES
# ══════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap');

:root {
    --bg:   #03050c;
    --s1:   #070b18;
    --s2:   #0b1025;
    --c1:   #e8f4ff;
    --c2:   #94b8ff;
    --c3:   #4a7fff;
    --g1:   #00e5c8;
    --r1:   #ff4f6a;
    --w1:   #f5c842;
    --mono: 'IBM Plex Mono', monospace;
    --serif:'Instrument Serif', serif;
    --cond: 'Barlow Condensed', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--c1) !important;
    font-family: var(--mono) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 900px 600px at 15% 50%, rgba(74,127,255,0.045) 0%, transparent 70%),
        radial-gradient(ellipse 700px 500px at 85% 20%, rgba(0,229,200,0.03) 0%, transparent 70%),
        radial-gradient(ellipse 500px 400px at 60% 80%, rgba(255,79,106,0.02) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"]    { display: none; }
[data-testid="stDecoration"] { display: none; }

::-webkit-scrollbar            { width: 3px; height: 3px; }
::-webkit-scrollbar-track      { background: var(--bg); }
::-webkit-scrollbar-thumb      { background: rgba(74,127,255,0.3); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(7,11,24,0.99) !important;
    border-right: 1px solid rgba(74,127,255,0.15) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label { color: var(--c1) !important; font-family: var(--mono) !important; }

/* ── Main block ── */
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stMain"] { background: transparent !important; }

/* ── Particle canvas ── */
#particle-canvas {
    position: fixed; inset: 0;
    pointer-events: none;
    z-index: 0; opacity: 0.4;
}

/* ── Live dot ── */
.live-dot {
    display: inline-block;
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--g1); margin-right: 7px;
    vertical-align: middle;
    animation: liveblink 1.2s ease-in-out infinite;
}
@keyframes liveblink {
    0%,100% { opacity:1; box-shadow: 0 0 8px var(--g1); }
    50%      { opacity:0.2; box-shadow: none; }
}

/* ── Hero ── */
.hero-wrap {
    padding: 30px 40px 22px;
    border-bottom: 1px solid rgba(74,127,255,0.1);
    background: rgba(7,11,24,0.85);
    position: relative; overflow: hidden;
}
.hero-wrap::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,200,0.02));
    pointer-events: none;
}
.hero-eyebrow {
    font-family: var(--mono); font-size: 9px;
    letter-spacing: 4px; text-transform: uppercase;
    color: var(--g1); margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
    content: ''; display: inline-block;
    width: 20px; height: 1px; background: var(--g1);
}
.hero-title {
    font-family: var(--cond); font-size: 42px;
    font-weight: 900; letter-spacing: -0.5px;
    color: var(--c1); line-height: 1.05; margin-bottom: 2px;
}
.hero-title em {
    font-family: var(--serif); font-style: italic;
    color: rgba(148,184,255,0.7); font-size: 36px;
}
.hero-pills { display: flex; gap: 7px; flex-wrap: wrap; margin-top: 14px; }
.pill {
    font-family: var(--mono); font-size: 8.5px;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 3px 10px; border: 1px solid; border-radius: 1px; font-weight: 600;
}
.pill-teal  { color:var(--g1); border-color:rgba(0,229,200,0.3);   background:rgba(0,229,200,0.05); }
.pill-blue  { color:var(--c2); border-color:rgba(74,127,255,0.3);  background:rgba(74,127,255,0.05); }
.pill-red   { color:var(--r1); border-color:rgba(255,79,106,0.3);  background:rgba(255,79,106,0.05); }

/* ── Stat bar ── */
.stat-bar {
    display: flex; gap: 0;
    border-bottom: 1px solid rgba(74,127,255,0.1);
    background: rgba(7,11,24,0.9);
}
.stat-cell {
    flex: 1; padding: 13px 24px;
    border-right: 1px solid rgba(74,127,255,0.07);
    position: relative;
}
.stat-cell::before {
    content:''; position:absolute;
    top:0; left:0; right:0; height:2px;
}
.stat-cell.g::before { background: var(--g1); }
.stat-cell.b::before { background: var(--c3); }
.stat-cell.r::before { background: var(--r1); }
.stat-cell.w::before { background: var(--w1); }
.stat-val {
    font-family: var(--cond); font-size: 24px;
    font-weight: 900; color: var(--c1);
    line-height: 1; margin-bottom: 2px;
}
.stat-cell.g .stat-val { color: var(--g1); }
.stat-cell.r .stat-val { color: var(--r1); }
.stat-cell.w .stat-val { color: var(--w1); }
.stat-lbl {
    font-family: var(--mono); font-size: 7.5px;
    letter-spacing: 2px; text-transform: uppercase;
    color: rgba(74,127,255,0.45);
}

/* ── Section header ── */
.sec-hdr {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 40px 10px;
}
.sec-hdr-text {
    font-family: var(--mono); font-size: 8.5px;
    letter-spacing: 3px; text-transform: uppercase;
    color: rgba(74,127,255,0.45); white-space: nowrap;
}
.sec-hdr-line { flex:1; height:1px; background:rgba(74,127,255,0.1); }

/* ── Padded content area ── */
.content-pad { padding: 0 40px; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(11,16,37,0.8) !important;
    border: 1px dashed rgba(74,127,255,0.2) !important;
    border-radius: 3px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(74,127,255,0.45) !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    color: rgba(74,127,255,0.4) !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
}
[data-testid="stFileUploaderDropzoneInput"] + div {
    color: rgba(74,127,255,0.4) !important;
}

/* ── Alerts ── */
.stSuccess {
    background: rgba(0,229,200,0.06) !important;
    border: 1px solid rgba(0,229,200,0.25) !important;
    border-left: 3px solid var(--g1) !important;
    border-radius: 2px !important;
    color: var(--g1) !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
}
.stError {
    background: rgba(255,79,106,0.06) !important;
    border: 1px solid rgba(255,79,106,0.25) !important;
    border-left: 3px solid var(--r1) !important;
    border-radius: 2px !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
}
.stWarning {
    background: rgba(245,200,66,0.06) !important;
    border: 1px solid rgba(245,200,66,0.25) !important;
    border-left: 3px solid var(--w1) !important;
    border-radius: 2px !important;
    font-family: var(--mono) !important;
    font-size: 11.5px !important;
}
[data-testid="stSpinner"] > div {
    border-top-color: var(--g1) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(11,16,37,0.88) !important;
    border: 1px solid rgba(74,127,255,0.12) !important;
    border-radius: 3px !important;
    margin-bottom: 10px !important;
    font-family: var(--mono) !important;
    font-size: 12.5px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(74,127,255,0.28) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-top: 2px solid rgba(74,127,255,0.55) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-top: 2px solid var(--g1) !important;
}
[data-testid="stChatMessageContent"] p {
    color: rgba(232,244,255,0.9) !important;
    line-height: 1.7 !important;
    font-family: var(--mono) !important;
    font-size: 12.5px !important;
}
[data-testid="stChatMessageAvatar"] {
    background: rgba(74,127,255,0.1) !important;
    border: 1px solid rgba(74,127,255,0.2) !important;
    border-radius: 2px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: rgba(11,16,37,0.97) !important;
    border: 1px solid rgba(74,127,255,0.22) !important;
    border-radius: 3px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(74,127,255,0.5) !important;
    box-shadow: 0 0 0 1px rgba(74,127,255,0.08) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--c1) !important;
    font-family: var(--mono) !important;
    font-size: 12px !important;
    caret-color: var(--g1) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(74,127,255,0.3) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(74,127,255,0.08) !important;
    border: 1px solid rgba(74,127,255,0.25) !important;
    border-radius: 2px !important;
    color: var(--c2) !important;
    font-family: var(--mono) !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 8px 18px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: rgba(74,127,255,0.16) !important;
    border-color: rgba(74,127,255,0.5) !important;
    color: var(--c1) !important;
    transform: translateY(-1px) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(11,16,37,0.8) !important;
    border: 1px solid rgba(74,127,255,0.12) !important;
    border-radius: 3px !important;
    font-family: var(--mono) !important;
}
[data-testid="stExpander"] summary {
    color: rgba(148,184,255,0.6) !important;
    font-family: var(--mono) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}

/* ── HR ── */
hr { border-color: rgba(74,127,255,0.1) !important; margin: 16px 0 !important; }

/* ── Citation card ── */
.cite-card {
    display: flex; align-items: center; gap: 10px;
    background: rgba(11,16,37,0.8);
    border: 1px solid rgba(74,127,255,0.1);
    border-left: 2px solid rgba(74,127,255,0.45);
    border-radius: 2px; padding: 9px 14px; margin-bottom: 6px;
    font-family: var(--mono); font-size: 10px;
    color: rgba(148,184,255,0.6); transition: all 0.15s;
}
.cite-card:hover {
    border-left-color: var(--g1); color: var(--c1);
    background: rgba(74,127,255,0.04);
}

/* ── Chunk card ── */
.chunk-card {
    background: rgba(11,16,37,0.8);
    border: 1px solid rgba(74,127,255,0.1);
    border-radius: 2px; padding: 14px 16px; margin-bottom: 10px;
    font-family: var(--mono); transition: border-color 0.15s;
}
.chunk-card:hover { border-color: rgba(74,127,255,0.3); }
.chunk-src {
    font-size: 8.5px; letter-spacing: 2px; text-transform: uppercase;
    color: var(--g1); margin-bottom: 6px; font-weight: 600;
}
.chunk-score-row { display:flex; align-items:center; gap:8px; margin-bottom:7px; }
.chunk-track { flex:1; height:2px; background:rgba(74,127,255,0.1); }
.chunk-fill  { height:100%; }
.chunk-score-val { font-size:9px; min-width:38px; text-align:right; font-weight:500; }
.chunk-text  { font-size:10.5px; color:rgba(148,184,255,0.55); line-height:1.65; }

/* ── Web result card ── */
.web-card {
    background: rgba(11,16,37,0.8);
    border: 1px solid rgba(255,79,106,0.12);
    border-left: 2px solid rgba(255,79,106,0.4);
    border-radius: 2px; padding: 10px 14px; margin-bottom: 8px;
    font-family: var(--mono); transition: all 0.15s;
}
.web-card:hover { border-left-color:var(--r1); background:rgba(255,79,106,0.04); }
.web-url     { font-size:8.5px; color:var(--r1); margin-bottom:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; opacity:.8; }
.web-snippet { font-size:10px; color:rgba(148,184,255,0.5); line-height:1.5; }

/* ── Sidebar custom ── */
.sb-logo-wrap {
    padding: 20px 18px 14px;
    border-bottom: 1px solid rgba(74,127,255,0.12); margin-bottom: 6px;
}
.sb-logo-text { font-family:var(--cond); font-size:20px; font-weight:900; letter-spacing:2px; color:var(--c1); }
.sb-logo-sub  { font-family:var(--mono); font-size:7.5px; letter-spacing:3px; text-transform:uppercase; color:rgba(74,127,255,0.4); margin-top:3px; }
.sb-sec       { font-family:var(--mono); font-size:7.5px; letter-spacing:3px; text-transform:uppercase; color:rgba(74,127,255,0.35); padding:10px 0 7px; }
.sb-file {
    display:flex; align-items:center; gap:8px; padding:7px 8px;
    font-family:var(--mono); font-size:10px; color:rgba(148,184,255,0.55);
    border:1px solid rgba(74,127,255,0.08); border-radius:2px; margin-bottom:5px; transition:all .15s;
}
.sb-file:hover { border-color:rgba(74,127,255,0.3); color:var(--c1); background:rgba(74,127,255,0.04); }
.sb-file-name { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:145px; }
.sb-file-type { margin-left:auto; font-size:7px; padding:1px 5px; border-radius:1px; background:rgba(74,127,255,0.1); color:rgba(74,127,255,0.6); letter-spacing:1px; text-transform:uppercase; }
.sb-stack-row { display:flex; justify-content:space-between; align-items:center; padding:4px 0; font-family:var(--mono); font-size:9.5px; border-bottom:1px solid rgba(74,127,255,0.06); }
.sb-stack-row:last-child { border-bottom:none; }
.sb-stack-name { color:rgba(74,127,255,0.4); }
.sb-stack-val  { color:var(--g1); font-weight:500; }
</style>

<canvas id="particle-canvas"></canvas>
<script>
(function(){
    var c=document.getElementById('particle-canvas');
    if(!c)return;
    var x=c.getContext('2d'),W,H,P=[];
    function rs(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
    rs(); window.addEventListener('resize',rs);
    for(var i=0;i<65;i++) P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.22,vy:(Math.random()-.5)*.22,r:Math.random()*1.3+.4,o:Math.random()*.38+.12});
    function draw(){
        x.clearRect(0,0,W,H);
        for(var i=0;i<P.length;i++){
            var p=P[i];p.x+=p.vx;p.y+=p.vy;
            if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
            x.beginPath();x.arc(p.x,p.y,p.r,0,6.28);
            x.fillStyle='rgba(74,127,255,'+p.o+')';x.fill();
            for(var j=i+1;j<P.length;j++){
                var q=P[j],d=Math.hypot(p.x-q.x,p.y-q.y);
                if(d<125){x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);
                x.strokeStyle='rgba(74,127,255,'+(0.1*(1-d/125))+')';x.lineWidth=.5;x.stroke();}
            }
        }
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sb-logo-wrap">
        <div class="sb-logo-text"><span class="live-dot"></span>NEURORAG</div>
        <div class="sb-logo-sub">Multimodal Intelligence Engine</div>
    </div>
    """, unsafe_allow_html=True)

    # Files list
    st.markdown('<div class="sb-sec">Indexed Files</div>', unsafe_allow_html=True)
    files = os.listdir("data/uploads")
    if files:
        for f in files:
            ext  = f.split(".")[-1].lower()
            icon = {"pdf":"▤","docx":"▤","txt":"▤","png":"▣","jpg":"▣","jpeg":"▣"}.get(ext,"▤")
            st.markdown(
                f'<div class="sb-file"><span>{icon}</span>'
                f'<span class="sb-file-name">{f}</span>'
                f'<span class="sb-file-type">{ext}</span></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;color:rgba(74,127,255,.3);padding:4px 0">No files indexed yet</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Tech stack
    st.markdown('<div class="sb-sec">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-stack-row"><span class="sb-stack-name">LLM</span><span class="sb-stack-val">Gemini 1.5 Flash</span></div>
    <div class="sb-stack-row"><span class="sb-stack-name">Embedder</span><span class="sb-stack-val">BGE-small-en</span></div>
    <div class="sb-stack-row"><span class="sb-stack-name">Vector DB</span><span class="sb-stack-val">Qdrant</span></div>
    <div class="sb-stack-row"><span class="sb-stack-name">Reranker</span><span class="sb-stack-val">CrossEncoder</span></div>
    <div class="sb-stack-row"><span class="sb-stack-name">Web Search</span><span class="sb-stack-val">Tavily</span></div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("⟳  Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


# ══════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════

st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">Retrieval-Augmented Generation</div>
    <div class="hero-title">Ask anything. <em>Find everything.</em></div>
    <div class="hero-pills">
        <span class="pill pill-teal">Semantic Search</span>
        <span class="pill pill-blue">Cross-Encoder Rerank</span>
        <span class="pill pill-red">Live Web Search</span>
        <span class="pill pill-teal">OCR Vision</span>
        <span class="pill pill-blue">Query Rewriting</span>
        <span class="pill pill-red">Traceable Citations</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  STAT BAR
# ══════════════════════════════════════════

doc_count = len(os.listdir("data/uploads"))
msg_count = len(st.session_state.messages)
q_count   = st.session_state.query_count

st.markdown(f"""
<div class="stat-bar">
    <div class="stat-cell g">
        <div class="stat-val">{doc_count}</div>
        <div class="stat-lbl">Docs Indexed</div>
    </div>
    <div class="stat-cell b">
        <div class="stat-val">{msg_count}</div>
        <div class="stat-lbl">Messages</div>
    </div>
    <div class="stat-cell r">
        <div class="stat-val">{q_count}</div>
        <div class="stat-lbl">Queries Run</div>
    </div>
    <div class="stat-cell w">
        <div class="stat-val">3</div>
        <div class="stat-lbl">Sources / Query</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  UPLOAD SECTION
# ══════════════════════════════════════════

st.markdown("""
<div class="sec-hdr">
    <span class="sec-hdr-text">Upload &amp; Index</span>
    <div class="sec-hdr-line"></div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop a file to index it into the knowledge base",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    # ── KEY FIX: only process if not already indexed ──
    if uploaded_file and uploaded_file.name not in st.session_state.indexed_files:

        save_path = os.path.join("data/uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        ext = uploaded_file.name.split(".")[-1].lower()

        with st.spinner(f"Parsing · {uploaded_file.name}"):
            if ext == "pdf":
                text = extract_pdf_text(save_path)
            elif ext == "docx":
                text = extract_docx_text(save_path)
            elif ext in ["png", "jpg", "jpeg"]:
                text = extract_text_from_image(save_path)
            elif ext == "txt":
                with open(save_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                text = ""

        if text.strip():
            with st.spinner("Chunking · Embedding · Indexing into Qdrant"):
                processed = process_document(text, uploaded_file.name)
                create_collection()
                upload_data(processed)

            # Mark as indexed — prevents re-running on every Streamlit rerun
            st.session_state.indexed_files.add(uploaded_file.name)

            st.success(f"✓  {uploaded_file.name}  indexed  ·  {len(text):,} characters processed")
            st.rerun()
        else:
            st.error(f"⚠  No text could be extracted from {uploaded_file.name}")

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
#  CHAT SECTION
# ══════════════════════════════════════════

st.markdown("""
<div class="sec-hdr">
    <span><span class="live-dot"></span></span>
    <span class="sec-hdr-text">Intelligence Chat</span>
    <div class="sec-hdr-line"></div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="content-pad">', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

# Chat input (must be outside content-pad to stick to bottom properly)
query = st.chat_input("› Ask anything about your documents or the web...")

if query:
    st.session_state.query_count += 1
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Rewriting query · Retrieving · Reranking · Generating"):
        response = ask_question(query)

    answer = response["answer"]
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

    # ── Citations ──
    if response.get("citations"):
        st.markdown("""
        <div class="sec-hdr" style="padding:14px 40px 8px">
            <span class="sec-hdr-text">Citations</span>
            <div class="sec-hdr-line"></div>
        </div>
        <div class="content-pad">
        """, unsafe_allow_html=True)

        for citation in response["citations"]:
            st.markdown(
                f'<div class="cite-card">↗ &nbsp;{citation}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Retrieved chunks ──
    if response.get("contexts"):
        with st.container():
            st.markdown('<div class="content-pad">', unsafe_allow_html=True)

            with st.expander("▶  View retrieved context chunks", expanded=False):

                doc_chunks = [
                    c for c in response["contexts"]
                    if c["metadata"].get("chunk_id") != "web"
                ]
                web_chunks = [
                    c for c in response["contexts"]
                    if c["metadata"].get("chunk_id") == "web"
                ]

                if doc_chunks:
                    st.markdown(
                        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:8px;'
                        'letter-spacing:2px;color:rgba(0,229,200,.5);text-transform:uppercase;'
                        'margin-bottom:10px">Document Chunks</div>',
                        unsafe_allow_html=True
                    )
                    for ctx in doc_chunks:
                        score = ctx.get("score", 0)
                        pct   = int(min(score, 1.0) * 100)
                        clr   = "#00e5c8" if score > 0.6 else "#94b8ff" if score > 0.3 else "rgba(74,127,255,.4)"
                        src   = ctx["metadata"].get("source", "unknown")
                        cid   = ctx["metadata"].get("chunk_id", "?")
                        st.markdown(f"""
                        <div class="chunk-card">
                            <div class="chunk-src">{src} · chunk {cid}</div>
                            <div class="chunk-score-row">
                                <div class="chunk-track">
                                    <div class="chunk-fill" style="width:{pct}%;background:{clr}"></div>
                                </div>
                                <span class="chunk-score-val" style="color:{clr}">{score:.4f}</span>
                            </div>
                            <div class="chunk-text">{ctx['chunk'][:350]}…</div>
                        </div>
                        """, unsafe_allow_html=True)

                if web_chunks:
                    st.markdown(
                        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:8px;'
                        'letter-spacing:2px;color:rgba(255,79,106,.5);text-transform:uppercase;'
                        'margin:14px 0 8px">Web Sources</div>',
                        unsafe_allow_html=True
                    )
                    for ctx in web_chunks:
                        src = ctx["metadata"].get("source", "web")
                        st.markdown(f"""
                        <div class="web-card">
                            <div class="web-url">↗ {src}</div>
                            <div class="web-snippet">{ctx['chunk'][:300]}…</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)