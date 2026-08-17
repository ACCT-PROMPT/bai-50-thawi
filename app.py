import streamlit as st
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from streamlit_cookies_controller import CookieController
from auth import (
    login, login_from_refresh_token, logout, build_navigation,
    SESSION_COOKIE, DEVICE_COOKIE, claim_session, heartbeat_session, release_session,
)

cookie = CookieController()


def _acquire_screen_slot() -> bool:
    """หลัง auth สำเร็จ — ตรวจ/จอง screen-slot ของอุปกรณ์นี้
    คืน True ถ้าถือ slot อยู่ หรือ False ถ้าถึงจำนวนหน้าจอสูงสุดแล้ว"""
    existing_sid = cookie.get(DEVICE_COOKIE)
    if existing_sid and heartbeat_session(existing_sid):
        st.session_state["_device_session_id"] = existing_sid
        st.session_state["_last_heartbeat"] = time.time()
        return True

    sid, allowed, count, max_allowed = claim_session(device_label=st.session_state.get("customer_email"))
    if allowed:
        cookie.set(DEVICE_COOKIE, sid, max_age=30 * 24 * 3600)
        st.session_state["_device_session_id"] = sid
        st.session_state["_last_heartbeat"] = time.time()
        return True

    st.session_state["_session_full"] = (count, max_allowed)
    return False


# ── Auth check ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    try:
        token = cookie.get(SESSION_COOKIE)
    except Exception:
        token = None

    if token:
        if login_from_refresh_token(token):
            if _acquire_screen_slot():
                st.session_state["_auth_init"] = True
                st.rerun()
            else:
                logout()
                try:
                    cookie.remove(SESSION_COOKIE)
                    cookie.remove(DEVICE_COOKIE)
                except Exception:
                    pass
        else:
            try:
                cookie.remove(SESSION_COOKIE)
            except Exception:
                pass

    if not st.session_state.get("_auth_init"):
        st.session_state["_auth_init"] = True
        st.stop()

    # ────── Login Page ──────────────────────────────────────────────────────
    st.set_page_config(
        page_title="📋 ใบ 50 ทวิ — เข้าสู่ระบบ",
        page_icon="🔐",
        layout="centered",
    )
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Prompt', sans-serif !important; }
    .stApp { background: linear-gradient(145deg, #0F2952 0%, #1A3F7A 40%, #2563EB 100%) !important; }
    [data-testid="stHeader"] { display:none; }
    [data-testid="stSidebar"] { display:none; }
    .block-container { padding-top: 60px !important; }
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.97) !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.25) !important;
        padding: 8px !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1A3F7A, #2563EB) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 14px rgba(37,99,235,0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0F2952, #1A3F7A) !important;
        box-shadow: 0 6px 20px rgba(37,99,235,0.5) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stTextInput"] > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid #CBD5E1 !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    [data-testid="stTextInput"] > div > div > input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.6, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px">
          <div style="font-size:52px;margin-bottom:8px;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.3))">📋</div>
          <div style="color:white;font-size:24px;font-weight:700;margin:0 0 6px;letter-spacing:-0.3px">📋 ใบ 50 ทวิ</div>
          <div style="color:rgba(255,255,255,0.7);font-size:13.5px">เข้าสู่ระบบด้วยบัญชีที่ซื้อเครื่องมือนี้</div>
        </div>
        """, unsafe_allow_html=True)

        session_full = st.session_state.pop("_session_full", None)
        if session_full:
            count, max_allowed = session_full
            st.warning(f"ถึงจำนวนหน้าจอสูงสุดของแพ็กนี้แล้ว ({count}/{max_allowed} จอ) กรุณาออกจากระบบในอุปกรณ์อื่นก่อน จึงจะเข้าใช้งานจอนี้ได้")

        with st.form("login_form", border=True):
            st.markdown('<div style="padding:8px 8px 4px">', unsafe_allow_html=True)
            email = st.text_input("อีเมล", placeholder="you@example.com",
                                   label_visibility="collapsed")
            password = st.text_input("รหัสผ่าน", type="password",
                                      placeholder="รหัสผ่าน...",
                                      label_visibility="collapsed")
            submitted = st.form_submit_button(
                "🔐 เข้าสู่ระบบ", type="primary", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if login(email, password):
                cookie.set(SESSION_COOKIE, st.session_state["refresh_token"], max_age=30 * 24 * 3600)
                if _acquire_screen_slot():
                    st.session_state["_auth_init"] = True
                    st.rerun()
                else:
                    logout()
                    cookie.remove(SESSION_COOKIE)
                    st.rerun()
            else:
                st.error(st.session_state.get("_auth_error", "เข้าสู่ระบบไม่สำเร็จ"))

    st.stop()


# ── คง heartbeat ของ screen-slot นี้เป็นระยะๆ ขณะใช้งาน ─────────────────────────────
_sid = st.session_state.get("_device_session_id")
if _sid and time.time() - st.session_state.get("_last_heartbeat", 0) > 300:
    if heartbeat_session(_sid):
        st.session_state["_last_heartbeat"] = time.time()
    # heartbeat ล้มเหลว (slot ถูกเก็บไปแล้ว) — ปล่อยไว้ rerun ถัดไปจะเข้า auth check สู่การ re-claim เอง

# ── Sidebar: user info + logout ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 14px 16px;
        margin: 10px 8px 8px 8px;
        backdrop-filter: blur(8px);
    ">
      <div style="font-size:11px;opacity:0.6;margin-bottom:4px;letter-spacing:0.5px;text-transform:uppercase;">ล็อกอินเป็น</div>
      <div style="font-weight:700;font-size:15px;margin-bottom:2px;">👤 {st.session_state.get('customer_name', '')}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 ออกจากระบบ", use_container_width=True):
        sid = st.session_state.get("_device_session_id")
        if sid:
            release_session(sid)
        cookie.remove(SESSION_COOKIE)
        cookie.remove(DEVICE_COOKIE)
        logout()
        st.rerun()

# ── Navigation ─────────────────────────────────────────────────────────────────
pg = build_navigation()
pg.run()
