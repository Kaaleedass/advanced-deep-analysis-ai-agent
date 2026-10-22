import os
import io
import json
import re
import html
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pdfplumber

from docx import Document
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)

# ============================================================
# ADVANCED DEEP ANALYSIS AI AGENT
# Premium Streamlit UI + AI-assisted document/table analysis
# ============================================================

st.set_page_config(
    page_title="Advanced Deep Analysis AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------- PREMIUM UI -------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
      --bg: #080d19;
      --panel: rgba(17, 26, 47, .86);
      --panel2: rgba(23, 35, 61, .82);
      --line: rgba(148, 163, 184, .18);
      --muted: #9eacc7;
      --text: #f2f6ff;
      --cyan: #65e6ff;
      --violet: #a78bfa;
    }
    html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
    }
    .stApp {
      background:
        radial-gradient(ellipse at 12% 0%, rgba(45, 91, 180, .24), transparent 35%),
        radial-gradient(ellipse at 90% 8%, rgba(126, 65, 220, .18), transparent 30%),
        linear-gradient(145deg, #080d19 0%, #0b1222 48%, #090f1d 100%);
      color: var(--text);
    }
    [data-testid="stHeader"] {
      background: rgba(8, 13, 25, .82);
    }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #101a30 0%, #0b1221 100%);
      border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: #e8efff; }
    .block-container {
      max-width: 1550px;
      padding-top: 1.6rem;
      padding-bottom: 3.5rem;
    }
    h1, h2, h3, h4 {
      font-family: 'Space Grotesk', sans-serif !important;
      letter-spacing: -.025em;
      color: #f6f8ff !important;
    }
    p, label, span, li, div {
      /* Streamlit's individual widgets may override this. */
    }
    .hero {
      position: relative;
      overflow: hidden;
      padding: 30px 34px;
      margin: 0 0 22px 0;
      border-radius: 24px;
      border: 1px solid rgba(135, 167, 255, .27);
      background:
        radial-gradient(circle at 85% 20%, rgba(101,230,255,.18), transparent 25%),
        radial-gradient(circle at 72% 110%, rgba(167,139,250,.22), transparent 35%),
        linear-gradient(120deg, rgba(17,29,54,.98), rgba(26,39,76,.96) 58%, rgba(23,30,61,.98));
      box-shadow: 0 22px 65px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.08);
    }
    .hero:after {
      content: "";
      position: absolute;
      width: 230px; height: 230px;
      right: 4%; top: -95px;
      border: 1px solid rgba(101,230,255,.22);
      border-radius: 50%;
      box-shadow: 0 0 0 24px rgba(101,230,255,.025),
                  0 0 0 48px rgba(101,230,255,.018);
      pointer-events: none;
    }
    .hero-kicker {
      color: #83eaff;
      font-size: .76rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .16em;
      margin-bottom: 10px;
    }
    .hero h1 {
      margin: 0 0 10px 0;
      font-size: clamp(1.8rem, 3vw, 2.65rem);
      line-height: 1.12;
      color: #fff !important;
    }
    .hero p {
      max-width: 850px;
      margin: 0;
      color: #c0cce3;
      font-size: 1rem;
      line-height: 1.65;
    }
    .hero-pills {
      display: flex; flex-wrap: wrap; gap: 8px;
      margin-top: 20px;
    }
    .hero-pill {
      border: 1px solid rgba(171,194,255,.22);
      background: rgba(8,15,31,.36);
      color: #dce9ff;
      padding: 7px 11px;
      border-radius: 999px;
      font-size: .78rem;
    }
    .section-label {
      color: #8ea6d6;
      font-size: .74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .14em;
      margin: 6px 0 10px 0;
    }
    .glass-card {
      background: linear-gradient(145deg, rgba(25,38,66,.94), rgba(13,21,39,.94));
      border: 1px solid rgba(151,174,224,.17);
      border-radius: 18px;
      padding: 18px 20px;
      box-shadow: 0 12px 30px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.035);
      min-height: 110px;
    }
    .metric-label {
      color: #9eacc7;
      font-size: .78rem;
      margin-bottom: 9px;
    }
    .metric-value {
      color: #f5f8ff;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 1.8rem;
      line-height: 1.2;
    }
    .metric-foot {
      color: #7edff4;
      font-size: .76rem;
      margin-top: 8px;
    }
    div[data-testid="stMetric"] {
      background: linear-gradient(145deg, rgba(25,38,66,.94), rgba(13,21,39,.94));
      border: 1px solid rgba(151,174,224,.17);
      border-radius: 16px;
      padding: 16px 18px;
      box-shadow: 0 12px 28px rgba(0,0,0,.17);
    }
    div[data-testid="stMetric"] label {
      color: #a9b7d2 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
      color: #f4f7ff !important;
      font-family: 'Space Grotesk', sans-serif;
    }
    div[data-testid="stMetricDelta"] { color: #7ee8cf !important; }
    div[data-testid="stTabs"] button {
      color: #aebbd3;
      font-weight: 600;
      border-radius: 10px 10px 0 0;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
      color: #73e7ff !important;
      border-bottom: 2px solid #73e7ff !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
      gap: 8px;
      border-bottom: 1px solid var(--line);
    }
    div[data-testid="stFileUploader"] {
      background: rgba(16,25,45,.86);
      border: 1px dashed rgba(113,199,255,.45);
      border-radius: 17px;
      padding: 12px;
    }
    div[data-testid="stFileUploader"] * { color: #e9f0ff; }
    .stButton button, .stDownloadButton button {
      border-radius: 11px;
      font-weight: 700;
      border: 1px solid rgba(115,231,255,.3);
      transition: all .18s ease;
    }
    .stButton button[kind="primary"] {
      background: linear-gradient(110deg, #2878e8, #7654d6);
      color: white;
      box-shadow: 0 8px 24px rgba(65,101,223,.28);
    }
    .stButton button:hover, .stDownloadButton button:hover {
      border-color: #73e7ff;
      transform: translateY(-1px);
      box-shadow: 0 8px 25px rgba(74,164,255,.15);
    }
    div[data-testid="stExpander"] {
      border: 1px solid rgba(151,174,224,.16);
      border-radius: 13px;
      background: rgba(14,22,40,.55);
    }
    [data-testid="stDataFrame"] {
      border: 1px solid rgba(151,174,224,.15);
      border-radius: 12px;
      overflow: hidden;
    }
    .stAlert { border-radius: 12px; }
    code { color: #9ee8ff !important; }
    footer { visibility: hidden; }
    </style>

    <div class="hero">
      <div class="hero-kicker">AI intelligence workspace · document to decisions</div>
      <h1>🧠 Advanced Deep Analysis AI Agent</h1>
      <p>
        Transform complex documents into structured data, interactive visual insights,
        executive-ready summaries, Python analysis and evidence-grounded answers.
      </p>
      <div class="hero-pills">
        <span class="hero-pill">✦ Smart table extraction</span>
        <span class="hero-pill">◈ Interactive analytics</span>
        <span class="hero-pill">⌘ Python code generation</span>
        <span class="hero-pill">◎ Evidence-grounded AI</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------- CONFIG -----------------------------

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY is not configured.")
    st.code(
        '$env:OPENAI_API_KEY = "your-api-key"\n'
        "python -m streamlit run .\\AI_Data_2.py",
        language="powershell",
    )
    st.stop()

llm = ChatOpenAI(model=MODEL_NAME, temperature=0, api_key=api_key)

# ---------------------- UTILITIES --------------------------

def response_text(response):
    content = getattr(response, "content", response)
    if isinstance(content, list):
        return "\n".join(
            str(x.get("text", "")) if isinstance(x, dict) else str(x)
            for x in content
        )
    return str(content)


def strip_fences(text):
    text = str(text).strip()
    text = re.sub(r"^```(?:json|python)?\s*", "", text, flags=re.I)
    return re.sub(r"\s*```$", "", text).strip()


def unique_headers(headers):
    used, result = set(), []
    for i, value in enumerate(headers):
        name = str(value or "").strip()
        if not name or name.lower() in {"none", "nan"}:
            name = f"Column_{i+1}"
        base, j = name, 2
        while name in used:
            name = f"{base}_{j}"
            j += 1
        used.add(name)
        result.append(name)
    return result


def make_df(headers, rows):
    if not headers:
        return pd.DataFrame()
    headers = unique_headers(headers)
    clean_rows = []
    for row in rows or []:
        if not isinstance(row, (list, tuple)):
            continue
        row = list(row[:len(headers)])
        row += [""] * max(0, len(headers) - len(row))
        clean_rows.append([None if x is None else str(x).strip() for x in row])
    df = pd.DataFrame(clean_rows, columns=headers)
    if df.empty:
        return df
    df = df.dropna(axis=0, how="all")
    df = df.loc[~df.astype(str).apply(
        lambda r: r.str.strip().isin(["", "None", "nan"]).all(), axis=1
    )]
    # Remove completely empty columns and rows.
    df = df.dropna(axis=1, how="all")
    df = df.loc[:, [
        c for c in df.columns
        if not df[c].astype(str).str.strip().isin(["", "None", "nan"]).all()
    ]]
    return df.reset_index(drop=True)


def normalize_values(df):
    result = df.copy()
    for col in result.columns:
        if not (
            pd.api.types.is_object_dtype(result[col])
            or pd.api.types.is_string_dtype(result[col])
        ):
            continue
        original = result[col].astype("string").str.strip()
        cleaned = (
            original.str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.replace("£", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
        )
        nums = pd.to_numeric(cleaned, errors="coerce")
        nonempty = original.notna() & original.ne("")
        if nonempty.sum() and nums[nonempty].notna().mean() >= .8:
            result[col] = nums
    return result


def profile_df(df):
    clean = normalize_values(df)
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": [str(c) for c in df.columns],
        "data_types": {str(c): str(t) for c, t in clean.dtypes.items()},
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()) if len(df) else 0,
        "numeric_summary": clean.select_dtypes(include="number")
            .describe().round(2).to_dict(),
        "sample_rows": df.head(5).fillna("").astype(str).to_dict("records"),
    }


# ---------------------- PDF INGESTION ----------------------

def extract_pdf_text(raw):
    pages = []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[PAGE {i}]\n{text}")
    return "\n\n".join(pages)


def extract_native_tables(raw, filename):
    result = {}
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            try:
                tables = page.extract_tables() or []
            except Exception:
                tables = []
            for table_no, table in enumerate(tables, start=1):
                if not table or len(table) < 2:
                    continue
                # Try to remove top/bottom rows that are completely empty.
                rows = [
                    [str(c).strip() if c is not None else "" for c in row]
                    for row in table
                ]
                rows = [r for r in rows if any(x for x in r)]
                if len(rows) < 2:
                    continue
                df = make_df(rows[0], rows[1:])
                # Discard highly fragmented noise; AI extraction below can
                # produce better chart-ready tables from the full text.
                if df.empty or len(df.columns) < 2 or len(df) < 2:
                    continue
                key = f"{filename} | p.{page_no} native table {table_no}"
                result[key] = df
    return result


def ai_extract_chart_tables(document_text, filename):
    """
    Ask the model to identify chart-worthy, coherent tables from extracted
    document text. Unlike raw PDF table extraction, this runs even when
    native tables exist, because native PDF tables are often fragmented.
    """
    if not document_text.strip():
        return {}

    # Give the model a bounded but multi-page view of the PDF.
    text = document_text[:52000]
    prompt = f"""
You are an expert document data extraction analyst.

Extract only coherent, useful tables from the document text below.
Return ONLY valid JSON:
{{
  "tables": [
    {{
      "name": "Financial performance",
      "description": "Financial values by reporting period",
      "columns": ["Metric", "Q1 FY2026", "Q1 FY2025", "FY2026", "FY2025", "FY2024"],
      "rows": [
        ["Revenue from operations (₹ million)", 391729, 350323, 1468853, 1282184, 1095581]
      ]
    }}
  ]
}}

Rules:
- Use ONLY values and labels explicitly present in the text.
- Never invent, estimate, interpolate, or silently correct values.
- Do not use placeholder values such as [●] as numbers.
- Keep reporting periods and units in column/metric labels.
- Prefer meaningful tables with consistent columns, such as financial results,
  financial cash flows, shareholding, industry KPIs, or operating metrics.
- Avoid creating one table for every paragraph.
- Combine continued parts of the same table when the headers clearly match.
- Include no more than 8 tables, with at most 35 rows per table.
- Use JSON numbers for numeric values where possible; preserve percentages and
  text values as strings when needed.
- If no meaningful structured tables exist, return {{"tables": []}}.
- No commentary outside JSON.

FILE: {filename}

DOCUMENT TEXT:
{text}
"""
    raw = strip_fences(response_text(llm.invoke(prompt)))
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end <= start:
        return {}
    payload = json.loads(raw[start:end + 1])
    extracted = {}
    for i, table in enumerate(payload.get("tables", [])[:8], start=1):
        columns = table.get("columns", [])
        rows = table.get("rows", [])
        if not columns or not rows:
            continue
        df = make_df(columns, rows[:35])
        if df.empty or len(df.columns) < 2:
            continue
        title = str(table.get("name") or f"AI extracted table {i}")
        desc = str(table.get("description") or "")
        extracted[f"{filename} | AI: {title}"] = df
        if desc:
            st.session_state.setdefault("table_descriptions", {})[
                f"{filename} | AI: {title}"
            ] = desc
    return extracted


# ---------------------- FILE READERS -----------------------

def read_file(upload):
    name = upload.name
    suffix = Path(name).suffix.lower()
    raw = upload.getvalue()

    if suffix == ".pdf":
        text = extract_pdf_text(raw)
        native = extract_native_tables(raw, name)
        # Always use AI to identify coherent tables, even if PDF parsing
        # returned fragmented tables. These are the chart-friendly datasets.
        ai_tables = {}
        if text.strip():
            try:
                ai_tables = ai_extract_chart_tables(text, name)
            except Exception as exc:
                st.warning(f"AI table extraction for {name} failed: {exc}")
        # Prefer AI-curated tables over fragmented native tables for charting.
        frames = ai_tables if ai_tables else native
        return {"frames": frames, "text": text, "name": name, "kind": "pdf"}

    if suffix == ".csv":
        try:
            df = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig")
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(raw), encoding="latin-1")
        return {"frames": {name: df}, "text": "", "name": name, "kind": "table"}

    if suffix in {".xlsx", ".xls"}:
        sheets = pd.read_excel(io.BytesIO(raw), sheet_name=None)
        return {
            "frames": {f"{name} | {sheet}": df for sheet, df in sheets.items()},
            "text": "", "name": name, "kind": "table",
        }

    if suffix == ".json":
        obj = json.loads(raw.decode("utf-8-sig"))
        frames = {}
        if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
            frames[name] = pd.json_normalize(obj)
        elif isinstance(obj, dict):
            normalized = pd.json_normalize(obj)
            if not normalized.empty:
                frames[name] = normalized
        return {
            "frames": frames, "text": json.dumps(obj, indent=2, ensure_ascii=False),
            "name": name, "kind": "json",
        }

    if suffix == ".txt":
        return {
            "frames": {}, "text": raw.decode("utf-8", errors="replace"),
            "name": name, "kind": "text",
        }

    if suffix == ".docx":
        doc = Document(io.BytesIO(raw))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        frames = {}
        for i, table in enumerate(doc.tables, start=1):
            rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            if len(rows) > 1:
                df = make_df(rows[0], rows[1:])
                if not df.empty:
                    frames[f"{name} | Table {i}"] = df
        return {
            "frames": frames, "text": "\n".join(paragraphs),
            "name": name, "kind": "document",
        }

    raise ValueError(
        f"Unsupported file type {suffix}. Use PDF, XLSX, XLS, CSV, JSON, TXT, DOCX."
    )


# ---------------------- CHARTS -----------------------------

def chart_candidates(dataset_name, original_df):
    df = normalize_values(original_df)
    charts = []
    numeric = list(df.select_dtypes(include="number").columns)
    categorical = list(df.select_dtypes(include=["object", "string", "category"]).columns)

    # For financial tables, rows often represent metrics and columns represent
    # reporting periods. Convert wide data to long form for clear line/bar charts.
    first_col = df.columns[0] if len(df.columns) else None
    if first_col is not None and len(numeric) >= 2 and first_col not in numeric:
        nonempty_labels = df[first_col].astype(str).str.strip()
        if nonempty_labels.nunique() >= 2 and len(df) <= 40:
            period_cols = [c for c in numeric if c != first_col]
            if len(period_cols) >= 2:
                long_df = df[[first_col] + period_cols].melt(
                    id_vars=first_col, var_name="Reporting period", value_name="Value"
                ).dropna()
                # Avoid plotting every metric together when values have very
                # different units; let the user select a metric in the UI below.
                charts.append({
                    "kind": "wide_financial",
                    "title": f"{dataset_name}: Metrics by reporting period",
                    "df": df,
                    "metric_col": first_col,
                    "period_cols": period_cols,
                })

    # Categorical count chart.
    if categorical:
        col = categorical[0]
        counts = df[col].dropna().astype(str).value_counts().head(15)
        if len(counts) >= 2:
            counts_df = counts.rename_axis(col).reset_index(name="Count")
            charts.append({
                "kind": "bar",
                "title": f"{dataset_name}: Distribution of {col}",
                "fig": px.bar(counts_df, x=col, y="Count", template="plotly_dark"),
            })

    # Histograms are useful only for meaningful numeric columns.
    for col in numeric[:3]:
        vals = df[col].dropna()
        if len(vals) >= 4 and vals.nunique() >= 4:
            charts.append({
                "kind": "hist",
                "title": f"{dataset_name}: {col} distribution",
                "fig": px.histogram(df, x=col, title=f"{col} distribution",
                                    template="plotly_dark", color_discrete_sequence=["#65e6ff"]),
            })
            break

    if len(numeric) >= 2:
        # Numeric correlation chart.
        corr = df[numeric].corr()
        if corr.shape[0] >= 2:
            charts.append({
                "kind": "corr",
                "title": f"{dataset_name}: Numeric correlation",
                "fig": px.imshow(corr, text_auto=".2f", aspect="auto",
                                 template="plotly_dark", color_continuous_scale="Tealgrn"),
            })

    # Date/time line chart if present.
    date_cols = [
        c for c in df.columns
        if any(k in str(c).lower() for k in ("date", "month", "year", "period", "quarter"))
    ]
    if numeric and date_cols:
        dcol = date_cols[0]
        dates = pd.to_datetime(df[dcol], errors="coerce")
        if dates.notna().sum() >= 3:
            line_df = pd.DataFrame({"Date": dates, "Value": df[numeric[0]]}).dropna()
            if len(line_df) >= 3:
                line_df = line_df.groupby("Date", as_index=False)["Value"].sum()
                charts.append({
                    "kind": "line",
                    "title": f"{dataset_name}: {numeric[0]} over time",
                    "fig": px.line(line_df, x="Date", y="Value", markers=True,
                                   template="plotly_dark", color_discrete_sequence=["#a78bfa"]),
                })

    return charts


def render_wide_financial_chart(item, key_prefix):
    df = normalize_values(item["df"])
    label_col = item["metric_col"]
    period_cols = item["period_cols"]

    labels = df[label_col].astype(str).tolist()
    options = labels[:]
    selected_metric = st.selectbox(
        "Choose a metric to visualize",
        options=options,
        key=f"{key_prefix}_metric",
    )
    row = df[df[label_col].astype(str) == selected_metric].iloc[0]
    vals = [pd.to_numeric(row[c], errors="coerce") for c in period_cols]
    chart_df = pd.DataFrame({
        "Reporting period": [str(c) for c in period_cols],
        "Value": vals,
    }).dropna()

    if len(chart_df) >= 2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_df["Reporting period"],
            y=chart_df["Value"],
            mode="lines+markers",
            line=dict(color="#65e6ff", width=4, shape="spline"),
            marker=dict(size=10, color="#a78bfa", line=dict(color="#ffffff", width=1)),
            fill="tozeroy",
            fillcolor="rgba(101,230,255,.10)",
            name=selected_metric,
        ))
        fig.update_layout(
            title=selected_metric,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(12,20,38,.65)",
            font=dict(color="#e9f1ff", family="DM Sans"),
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_title="Reporting period",
            yaxis_title="Value (as stated in source)",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}_wide_chart")
    else:
        st.info("This metric does not have enough numeric period values to chart.")


# ---------------------- SIDEBAR ----------------------------

with st.sidebar:
    st.markdown("## 🧠 Analysis controls")
    st.markdown("**Workflow**")
    st.markdown("1. Upload documents\n2. Extract structured data\n3. Generate insights\n4. Explore charts\n5. Ask follow-up questions")
    st.divider()
    st.markdown("**Analysis engine**")
    st.caption(f"Model: `{MODEL_NAME}`")
    st.caption("AI extraction is used to recover coherent tables from PDFs.")
    st.divider()
    st.caption("Tip: financial PDFs often contain tables split across page layouts. Validate extracted values before making investment decisions.")


# ---------------------- UPLOAD -----------------------------

st.markdown('<div class="section-label">01 / Data sources</div>', unsafe_allow_html=True)
uploads = st.file_uploader(
    "Drop files here or browse",
    type=["pdf", "xlsx", "xls", "csv", "json", "txt", "docx"],
    accept_multiple_files=True,
    help="PDF, Excel, CSV, JSON, TXT and Word documents are supported.",
)

if not uploads:
    st.markdown(
        """
        <div class="glass-card">
          <div style="font-size:1.2rem;font-weight:700;color:#f4f7ff;margin-bottom:8px;">
            Your analysis workspace is ready
          </div>
          <div style="color:#a9b7d2;line-height:1.7;">
            Upload a report, prospectus, spreadsheet or document to generate
            a structured analysis. For PDFs, the agent extracts text and
            uses AI to identify coherent, chart-worthy tables.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

if st.button("↻ Reprocess uploaded files", help="Run file extraction again"):
    st.session_state.pop("analysis_cache", None)
    st.session_state.pop("summary", None)
    st.session_state.pop("chat_history", None)
    st.rerun()

# Cache processing for the same uploaded file names/byte sizes within session.
cache_key = tuple((f.name, f.size) for f in uploads)
if st.session_state.get("analysis_cache_key") != cache_key:
    all_frames, all_docs, errors = {}, {}, []
    st.markdown('<div class="section-label">02 / Extracting and structuring content</div>', unsafe_allow_html=True)
    progress = st.progress(0, text="Preparing files...")
    for i, upload in enumerate(uploads):
        progress.progress((i + 1) / len(uploads), text=f"Analyzing {upload.name}...")
        try:
            result = read_file(upload)
            all_frames.update(result["frames"])
            if result["text"].strip():
                all_docs[result["name"]] = result["text"]
        except Exception as exc:
            errors.append(f"{upload.name}: {exc}")
    progress.empty()
    st.session_state["analysis_cache_key"] = cache_key
    st.session_state["analysis_cache"] = {
        "frames": all_frames,
        "documents": all_docs,
        "errors": errors,
    }
    st.session_state.pop("summary", None)

cache = st.session_state["analysis_cache"]
frames = cache["frames"]
documents = cache["documents"]
for err in cache["errors"]:
    st.error(err)

# ---------------------- KPI STRIP --------------------------

st.markdown('<div class="section-label">03 / Workspace overview</div>', unsafe_allow_html=True)
total_rows = sum(len(df) for df in frames.values())
total_cols = sum(len(df.columns) for df in frames.values())
doc_chars = sum(len(t) for t in documents.values())
k1, k2, k3, k4 = st.columns(4)
k1.metric("Structured datasets", len(frames), help="Extracted or uploaded tabular datasets")
k2.metric("Total records", f"{total_rows:,}")
k3.metric("Document sources", len(documents))
k4.metric("Text extracted", f"{doc_chars:,} chars")

if not frames and not documents:
    st.error("No readable content was found in the uploaded files.")
    st.stop()

context_parts = []
for name, df in frames.items():
    context_parts.append(
        f"DATASET: {name}\nPROFILE: {json.dumps(profile_df(df), default=str)}\n"
        f"FIRST ROWS:\n{df.head(30).to_csv(index=False)}"
    )
for name, text_content in documents.items():
    context_parts.append(f"DOCUMENT: {name}\n{text_content[:24000]}")
evidence_context = "\n\n---\n\n".join(context_parts)

# ---------------------- TABS -------------------------------

overview_tab, data_tab, charts_tab, code_tab, ask_tab = st.tabs([
    "✦ Executive overview",
    "▦ Data explorer",
    "◈ Visual analytics",
    "⌘ Code & HTML export",
    "◎ Ask your data",
])

with overview_tab:
    st.markdown('<div class="section-label">Executive intelligence</div>', unsafe_allow_html=True)
    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("### Generate an executive brief")
        st.write("Create a concise, evidence-based summary suitable for understanding the document or preparing a business review.")
        if st.button("✦ Generate deep analysis", type="primary", use_container_width=True):
            prompt = f"""
You are an experienced business and data analyst. Use only the evidence below.

Create a polished report with:
- Executive summary
- Document purpose and scope
- Important findings and figures
- Financial/operational trends only where supported
- Risks, caveats, missing data and extraction uncertainty
- Recommended follow-up questions

Do not invent figures. Preserve the source's units and periods.
Clearly label any values that may have been extracted from complex tables and should be checked against the original.

EVIDENCE:
{evidence_context[:42000]}
"""
            with st.spinner("Building the executive brief..."):
                try:
                    st.session_state["summary"] = response_text(llm.invoke(prompt))
                except Exception as exc:
                    st.error(f"Could not generate summary: {exc}")

        if st.session_state.get("summary"):
            st.markdown(st.session_state["summary"])
            st.download_button(
                "Download executive brief",
                st.session_state["summary"],
                file_name="executive_analysis.md",
                mime="text/markdown",
            )
        else:
            st.markdown(
                """
                <div class="glass-card">
                  <div style="color:#73e7ff;font-weight:700;margin-bottom:8px;">What you will get</div>
                  <div style="color:#b8c5dc;line-height:1.8;">
                    • Key facts and metrics<br>
                    • Business implications<br>
                    • Data quality observations<br>
                    • Risks and limitations<br>
                    • Suggested next steps
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("### Data quality snapshot")
        if frames:
            quality = []
            for name, df in frames.items():
                quality.append({
                    "Dataset": name,
                    "Rows": len(df),
                    "Columns": len(df.columns),
                    "Missing cells": int(df.isna().sum().sum()),
                    "Duplicate rows": int(df.duplicated().sum()) if len(df) else 0,
                })
            quality_df = pd.DataFrame(quality)
            st.dataframe(quality_df, use_container_width=True, hide_index=True)
            st.caption("PDF extraction can produce fragmented or merged cells. Validate important values against the source.")
        else:
            st.info("No tabular data was detected. Document text is available for summarization and Q&A.")

    if documents:
        st.markdown("### Extracted document text")
        for name, text_content in documents.items():
            with st.expander(f"Read extracted text · {name}"):
                st.text(text_content[:10000] or "No selectable text was found.")

with data_tab:
    st.markdown('<div class="section-label">Inspect extracted datasets</div>', unsafe_allow_html=True)
    if not frames:
        st.info("No tables are available yet. If the PDF is scanned, OCR is needed.")
    else:
        dataset_name = st.selectbox("Choose dataset", list(frames.keys()), key="data_dataset")
        df = frames[dataset_name]
        st.markdown(f"### {dataset_name}")
        st.caption(f"{len(df):,} rows · {len(df.columns)} columns")
        st.dataframe(df, use_container_width=True, height=430)
        st.download_button(
            "Download this dataset as CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="extracted_table.csv",
            mime="text/csv",
        )
        st.markdown("#### Column profile")
        prof = pd.DataFrame({
            "Column": [str(c) for c in df.columns],
            "Detected type": [str(t) for t in normalize_values(df).dtypes],
            "Missing": [int(df[c].isna().sum()) for c in df.columns],
            "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns],
        })
        st.dataframe(prof, use_container_width=True, hide_index=True)

with charts_tab:
    st.markdown('<div class="section-label">Chart studio</div>', unsafe_allow_html=True)
    st.markdown("### Turn extracted data into business visuals")
    if not frames:
        st.info("No structured tables are available for charting.")
    else:
        selected = st.selectbox("Dataset for visualization", list(frames.keys()), key="chart_dataset")
        df = frames[selected]
        charts = chart_candidates(selected, df)

        if not charts:
            st.warning(
                "No reliable chart candidate was detected. Check the Data explorer "
                "for column names and extracted values. The AI extraction step may "
                "need a more specific table prompt for this document."
            )
        else:
            for i, item in enumerate(charts):
                with st.container(border=True):
                    if item["kind"] == "wide_financial":
                        st.markdown(f"#### ◈ {item['title']}")
                        render_wide_financial_chart(item, f"financial_{i}")
                    else:
                        st.markdown(f"#### ◈ {item['title']}")
                        fig = item["fig"]
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(12,20,38,.55)",
                            font=dict(color="#e8f0ff", family="DM Sans"),
                            margin=dict(l=20, r=20, t=55, b=25),
                            title_font=dict(color="#f3f6ff", size=17),
                        )
                        st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")

        st.caption("Charts are generated from extracted values. Check table labels, units and periods before using them in presentations.")

with code_tab:
    st.markdown('<div class="section-label">Developer workspace</div>', unsafe_allow_html=True)
    st.markdown("### Generate a reusable Python analysis script")
    if st.button("⌘ Generate Python code", type="primary"):
        if not frames:
            st.warning("Upload a spreadsheet or extract a table from a document first.")
        else:
            schema = {
                name: {
                    "columns": [str(c) for c in df.columns],
                    "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
                    "sample": df.head(3).fillna("").astype(str).to_dict("records"),
                }
                for name, df in frames.items()
            }
            prompt = f"""
Generate clean Python source code only, no Markdown fences.
Use pandas and plotly or matplotlib to analyze these datasets.
Include data quality checks, descriptive summaries, appropriate charts,
and export outputs to a new output directory.
Do not invent column names or results. Do not execute code, delete files,
make network requests, or include secrets.

Dataset schemas and sample rows:
{json.dumps(schema, ensure_ascii=False, default=str)[:22000]}
"""
            with st.spinner("Generating Python script..."):
                try:
                    st.session_state["python_code"] = strip_fences(
                        response_text(llm.invoke(prompt))
                    )
                except Exception as exc:
                    st.error(f"Code generation failed: {exc}")

    if st.session_state.get("python_code"):
        st.code(st.session_state["python_code"], language="python")
        st.download_button(
            "Download Python script",
            st.session_state["python_code"],
            file_name="deep_analysis.py",
            mime="text/x-python",
        )
        st.warning("Review AI-generated code before running it. The app does not execute the generated script.")

    st.divider()
    st.markdown("### Export an executive HTML dashboard")
    if st.button("Generate HTML dashboard"):
        sections = []
        summary = st.session_state.get("summary", "No executive summary generated yet.")
        sections.append(
            "<section><h2>Executive brief</h2><pre>"
            + html.escape(summary) + "</pre></section>"
        )

        for name, df in frames.items():
            sections.append(
                "<section><h2>" + html.escape(name) + "</h2>"
                + "<p>" + str(len(df)) + " records · "
                + str(len(df.columns)) + " columns</p>"
                + df.head(30).to_html(index=False, escape=True, border=0)
                + "</section>"
            )
            for item in chart_candidates(name, df):
                if item["kind"] == "wide_financial":
                    # Include one chart per numeric metric for wide tables.
                    wide_df = normalize_values(item["df"])
                    label_col = item["metric_col"]
                    for metric in wide_df[label_col].astype(str).tolist()[:8]:
                        row = wide_df[wide_df[label_col].astype(str) == metric].iloc[0]
                        values = [pd.to_numeric(row[c], errors="coerce") for c in item["period_cols"]]
                        chart_df = pd.DataFrame({
                            "Reporting period": item["period_cols"],
                            "Value": values,
                        }).dropna()
                        if len(chart_df) >= 2:
                            fig = px.line(
                                chart_df, x="Reporting period", y="Value",
                                markers=True, title=metric, template="plotly_dark",
                            )
                            fig.update_layout(
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(12,20,38,.55)",
                                font=dict(color="#e8f0ff"),
                            )
                            sections.append(
                                pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
                            )
                else:
                    fig = item["fig"]
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(12,20,38,.55)",
                        font=dict(color="#e8f0ff"),
                    )
                    sections.append(
                        pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
                    )

        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Advanced Deep Analysis AI Agent</title>
<style>
:root{{--bg:#080d19;--panel:#111a2f;--text:#f2f6ff;--muted:#9eacc7;--cyan:#65e6ff}}
*{{box-sizing:border-box}}
body{{margin:0;background:radial-gradient(ellipse at 15% 0%,#182b53 0,transparent 36%),linear-gradient(145deg,#080d19,#0b1222);font-family:Arial,sans-serif;color:var(--text)}}
main{{max-width:1400px;margin:0 auto;padding:32px 22px}}
header{{padding:34px;border-radius:24px;background:linear-gradient(120deg,#101d37,#263a70);border:1px solid #3b5280;box-shadow:0 25px 70px #0007;margin-bottom:24px}}
.kicker{{text-transform:uppercase;letter-spacing:.16em;color:var(--cyan);font-size:12px;font-weight:bold}}
h1{{font-size:clamp(28px,4vw,46px);margin:12px 0}}
header p{{color:#c0cce3;line-height:1.7}}
section{{background:linear-gradient(145deg,#15213a,#0f182b);border:1px solid #ffffff1c;border-radius:18px;padding:24px;margin:20px 0;box-shadow:0 16px 38px #0004;overflow-x:auto}}
h2{{color:#9beaff;margin-top:0}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;color:#dbe6ff;line-height:1.6}}
table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{border-bottom:1px solid #ffffff18;padding:10px;text-align:left}}th{{color:#8feaff;background:#ffffff08}}td{{color:#e5edff}}
footer{{color:#8798b8;text-align:center;padding:25px}}
</style>
</head>
<body><main>
<header><div class="kicker">AI intelligence workspace · document to decisions</div>
<h1>🧠 Advanced Deep Analysis AI Agent</h1>
<p>Executive-ready insights, structured data, interactive visual analytics and evidence-grounded findings.</p>
<p>Generated {datetime.now().strftime("%d %b %Y, %H:%M")}</p></header>
{''.join(sections)}
<footer>AI-generated analysis · Verify important figures against original source documents.</footer>
</main></body></html>"""
        st.session_state["html_dashboard"] = page

    if st.session_state.get("html_dashboard"):
        st.download_button(
            "Download premium HTML dashboard",
            st.session_state["html_dashboard"],
            file_name="advanced_deep_analysis_dashboard.html",
            mime="text/html",
        )
        st.caption("The HTML dashboard uses Plotly's CDN for interactive charts, so internet access is needed to render them.")

with ask_tab:
    st.markdown('<div class="section-label">Evidence-grounded assistant</div>', unsafe_allow_html=True)
    st.markdown("### Ask questions about the uploaded files")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask about a metric, trend, definition, risk or table...")
    if question:
        st.session_state["chat_history"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Finding evidence in your files..."):
                try:
                    # Use direct LLM over table profiles and document text in this
                    # starter version; avoid unsafe arbitrary code execution.
                    prompt = f"""
Answer the question using only the evidence below.
If a calculation is requested and the supplied rows do not contain enough data,
say so. Never invent figures. Clearly state the units and periods.
If PDF extraction may be imperfect, tell the user to verify the source table.

EVIDENCE:
{evidence_context[:42000]}

QUESTION:
{question}
"""
                    answer = response_text(llm.invoke(prompt))
                except Exception as exc:
                    answer = f"Could not answer this question: {exc}"
                st.markdown(answer)
                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": answer}
                )

    if st.button("Clear conversation"):
        st.session_state["chat_history"] = []
        st.rerun()

st.markdown(
    '<div style="text-align:center;color:#7283a2;font-size:.78rem;padding-top:28px;">'
    'ADVANCED DEEP ANALYSIS AI AGENT · DOCUMENT INTELLIGENCE · DATA VISUALIZATION'
    '</div>',
    unsafe_allow_html=True,
)
