"""CSS ที่ใช้ร่วมกันทุกหน้า — import แล้วเรียก inject()"""
import streamlit as st

def inject():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== Base Typography ===== */
    html, body, [class*="css"], .stApp, .stMarkdown, .stText,
    .stSelectbox, .stRadio, .stTextInput, .stTextArea,
    label, p, button, input, textarea, select,
    [data-testid="stMarkdownContainer"] {
        font-family: 'Prompt', sans-serif !important;
    }
    .material-icons,
    [data-testid="stExpanderToggleIcon"] span,
    [class*="material"] {
        font-family: 'Material Icons' !important;
    }
    code, pre, [data-testid="stCode"],
    .stDataFrame, .dataframe {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* ===== App background ===== */
    .stApp {
        background: #F4F6FB !important;
    }

    /* ===== Main content area ===== */
    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1200px !important;
    }

    /* ===== Sidebar ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #0F2952 0%, #1A3F7A 55%, #1E4D8C 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 20px rgba(15,41,82,0.18) !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebarContent"] {
        padding-top: 0 !important;
    }
    /* Sidebar nav links */
    [data-testid="stSidebarNavLink"] {
        border-radius: 10px !important;
        margin: 2px 8px !important;
        padding: 8px 12px !important;
        transition: background 0.18s !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background: rgba(255,255,255,0.12) !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(255,255,255,0.18) !important;
        font-weight: 700 !important;
        box-shadow: inset 3px 0 0 #60A5FA !important;
    }
    /* Sidebar section labels */
    [data-testid="stSidebarNavSeparator"] {
        opacity: 0.25 !important;
        margin: 6px 16px !important;
    }

    /* ===== Top header bar ===== */
    [data-testid="stHeader"] {
        background: transparent !important;
        border-bottom: none !important;
    }

    /* ===== Remove sidebar expand button ===== */
    [data-testid="stExpandSidebarButton"] { display: none !important; }

    /* ===== Page title headings ===== */
    h1 {
        color: #0F2952 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }
    h2 {
        color: #1A3F7A !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    h3 {
        color: #1E4D8C !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* ===== Primary button ===== */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #1A3F7A, #2563EB) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 11px 28px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 10px rgba(37,99,235,0.28) !important;
        letter-spacing: 0.2px !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #0F2952, #1A3F7A) !important;
        box-shadow: 0 5px 18px rgba(37,99,235,0.38) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.2) !important;
    }

    /* ===== Secondary button ===== */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: #FFFFFF !important;
        color: #1A3F7A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.18s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #2563EB !important;
        color: #2563EB !important;
        background: #EFF6FF !important;
    }

    /* ===== Download button ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #065F46, #059669) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 11px 28px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        box-shadow: 0 2px 10px rgba(5,150,105,0.28) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #064E3B, #065F46) !important;
        box-shadow: 0 5px 18px rgba(5,150,105,0.38) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== File uploader ===== */
    [data-testid="stFileUploader"] {
        border: 2px dashed #93C5FD !important;
        border-radius: 14px !important;
        padding: 10px !important;
        background: linear-gradient(135deg, #EFF6FF, #F0FDF4) !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #2563EB !important;
        background: linear-gradient(135deg, #DBEAFE, #D1FAE5) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
    }

    /* ===== Tabs ===== */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 4px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding-bottom: 0 !important;
    }
    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        color: #64748B !important;
        border: 1px solid transparent !important;
        border-bottom: none !important;
        transition: all 0.15s !important;
    }
    [data-testid="stTabs"] button[role="tab"]:hover {
        background: #EFF6FF !important;
        color: #2563EB !important;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1A3F7A !important;
        font-weight: 700 !important;
        border-color: #E2E8F0 !important;
        border-bottom: 2px solid #FFFFFF !important;
        margin-bottom: -2px !important;
    }

    /* ===== Alerts ===== */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border-left-width: 4px !important;
        font-size: 14px !important;
    }

    /* ===== Dataframe ===== */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
    }

    /* ===== Expander ===== */
    [data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    }

    /* ===== Divider ===== */
    hr {
        border-color: #E2E8F0 !important;
        margin: 1.2rem 0 !important;
    }

    /* ===== Spinner ===== */
    [data-testid="stSpinner"] > div {
        border-top-color: #2563EB !important;
    }

    /* ===== Select / Input ===== */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stTextArea"] > div > div > textarea,
    [data-testid="stNumberInput"] > div > div > input {
        border-radius: 10px !important;
        border-color: #CBD5E1 !important;
        background: #FFFFFF !important;
        font-size: 14px !important;
    }
    [data-testid="stTextInput"] > div > div > input:focus,
    [data-testid="stTextArea"] > div > div > textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }

    /* ===== Metric cards ===== */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stMetricValue"] {
        color: #0F2952 !important;
        font-weight: 700 !important;
    }

    /* ===== Form container ===== */
    [data-testid="stForm"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        padding: 4px !important;
    }

    /* ===== Caption / small text ===== */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #64748B !important;
        font-size: 13px !important;
    }

    /* ===== Progress bar ===== */
    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #1A3F7A, #2563EB) !important;
        border-radius: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ── Page header helper ─────────────────────────────────────────────────────────

def page_header(icon: str, title: str, desc: str, badge: str = "", badge_color: str = "#1A3F7A"):
    """Consistent page header: badge tag + title + description."""
    if badge:
        st.markdown(
            f'<span style="background:linear-gradient(135deg,{badge_color},{badge_color}cc);'
            f'color:white;border-radius:20px;padding:4px 14px;font-size:11.5px;'
            f'font-weight:700;letter-spacing:0.5px;">{badge}</span>',
            unsafe_allow_html=True,
        )
    st.title(f"{icon} {title}")
    if desc:
        st.caption(desc)
    st.divider()


def back_home():
    """ปุ่มกลับหน้าหลัก"""
    if st.button("← หน้าหลัก", key="_back_home_btn", type="secondary"):
        st.switch_page("home.py")
    st.divider()


# ── Upload Reset Helpers ────────────────────────────────────────────────────────

def upload_key(page: str) -> int:
    k = f"_upkey_{page}"
    if k not in st.session_state:
        st.session_state[k] = 0
    return st.session_state[k]


def clear_files_button(page: str) -> None:
    if st.button("🗑️ ล้างไฟล์", key=f"_clearbtn_{page}", help="ล้างไฟล์ที่อัปโหลดทั้งหมด"):
        st.session_state[f"_upkey_{page}"] += 1
        st.rerun()
