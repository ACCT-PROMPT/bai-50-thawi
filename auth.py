"""auth.py — Supabase-backed auth/entitlement client สำหรับ 📋 ใบ 50 ทวิ (AcctPrompt)

ใช้ Supabase Auth (JWT / refresh token / password hashing) + Postgres RLS โดยตรง
ไม่มี API กลางแยกต่าง—สคีมาอยู่ที่ github.com/acctprompt-cmyk/acctprompt-platform

จำกัดจำนวนหน้าจอที่ล็อกอินพร้อมกันได้ (1/3/5 จอ ตามแพ็กที่ซื้อ) บังคับผ่าน
Postgres function ฝั่ง Supabase (claim_session/heartbeat_session/release_session)
ดู acctprompt-platform/supabase/002_sessions.sql สำหรับรายละเอียด

หมายเหตุ: เขียนด้วย placeholder เนื่องจากยังไม่มี Supabase project จริง —
ยังไม่ได้ทดสอบ end-to-end จนกว่าจะมี SUPABASE_URL/SUPABASE_ANON_KEY จริง
"""
import os
import streamlit as st
from supabase import create_client, Client

SUPABASE_URL      = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
TOOL_SLUG         = "bai-50-thawi"

SESSION_COOKIE = "alter_refresh"     # Supabase refresh token
DEVICE_COOKIE  = "alter_device_sid"  # active_sessions.id ของหน้าจอนี้ — 1 คูกกี้ = 1 หน้าจอที่นับ

_sb: Client | None = None


def _client() -> Client:
    global _sb
    if _sb is None:
        _sb = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _sb


def _get_tool_id() -> str | None:
    """UUID ของ tool ตัวเองในตาราง tools — cache ไว้ใน session เพราะไม่เปลี่ยนบ่อย"""
    if "_tool_id" in st.session_state:
        return st.session_state["_tool_id"]
    try:
        res = _client().table("tools").select("id").eq("slug", TOOL_SLUG).single().execute()
    except Exception:
        return None
    tool_id = (res.data or {}).get("id")
    st.session_state["_tool_id"] = tool_id
    return tool_id


def _check_entitlement() -> tuple[bool, str | None]:
    """ถามตาราง entitlements ตรงๆ — RLS กรองให้เห็นแค่แถวของ customer ที่ล็อกอินอยู่เอง"""
    tool_id = _get_tool_id()
    if not tool_id:
        return False, None
    try:
        res = (_client().table("entitlements")
               .select("status,expires_at")
               .eq("tool_id", tool_id)
               .eq("status", "active")
               .execute())
    except Exception:
        return False, None
    rows = res.data or []
    return (True, rows[0].get("expires_at")) if rows else (False, None)


def _apply_session(session, user) -> bool:
    allowed, expires_at = _check_entitlement()
    full_name, role = user.email, "customer"
    try:
        prof = _client().table("customers").select("full_name,role").eq("id", user.id).single().execute()
        if prof.data:
            full_name = prof.data.get("full_name") or user.email
            role = prof.data.get("role", "customer")
    except Exception:
        pass
    st.session_state.update({
        "logged_in": True,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "customer_email": user.email,
        "customer_name": full_name,
        "customer_role": role,
        "entitlement_allowed": allowed,
        "entitlement_expires_at": expires_at,
    })
    return True


def login(email: str, password: str) -> bool:
    """ล็อกอินด้วย email/password ผ่าน Supabase Auth"""
    try:
        res = _client().auth.sign_in_with_password({"email": email, "password": password})
    except Exception:
        st.session_state["_auth_error"] = "อีเมลหรือรหัสผ่านไม่ถูกต้อง"
        return False
    if not res or not res.session:
        st.session_state["_auth_error"] = "เข้าสู่ระบบไม่สำเร็จ"
        return False
    return _apply_session(res.session, res.user)


def login_from_refresh_token(refresh_token: str) -> bool:
    """auto-login ตอนเปิดแอปใหม่ ด้วย refresh token ที่เก็บใน cookie"""
    try:
        res = _client().auth.refresh_session(refresh_token)
    except Exception:
        return False
    if not res or not res.session:
        return False
    return _apply_session(res.session, res.user)


def logout() -> None:
    try:
        _client().auth.sign_out()
    except Exception:
        pass
    for k in ["logged_in", "access_token", "refresh_token", "customer_email",
              "customer_name", "customer_role", "entitlement_allowed",
              "entitlement_expires_at", "_tool_id", "_device_session_id",
              "_last_heartbeat"]:
        st.session_state.pop(k, None)


def is_admin() -> bool:
    return st.session_state.get("customer_role") == "admin"


def can_access(_tool_id: str | None = None) -> bool:
    """_tool_id เก็บไว้เพื่อความเข้ากันได้กับ call site เดิม — แอปนี้มีเครื่องมือเดียวอยู่แล้ว"""
    return bool(st.session_state.get("logged_in") and st.session_state.get("entitlement_allowed"))


# ── จำกัดจำนวนหน้าจอ (concurrent screens) ───────────────────────────────

def claim_session(device_label: str | None = None) -> tuple[str | None, bool, int, int]:
    """เรียกตอนยังไม่มี slot ของหน้าจอนี้ (login ครั้งแรก หรือ cookie session id หาย)
    คืน (session_id, allowed, active_count, max_allowed)"""
    try:
        res = _client().rpc("claim_session", {"p_tool_slug": TOOL_SLUG, "p_device_label": device_label}).execute()
    except Exception:
        return None, False, 0, 0
    rows = res.data or []
    if not rows:
        return None, False, 0, 0
    row = rows[0]
    return row.get("session_id"), bool(row.get("allowed")), row.get("active_count", 0) or 0, row.get("max_allowed", 0) or 0


def heartbeat_session(session_id: str) -> bool:
    """เรียกเป็นระยะๆ เพื่อบอกว่า slot นี้ยังมีชีวิตอยู่ — False = slot หาย (ต้อง claim_session ใหม่)"""
    try:
        res = _client().rpc("heartbeat_session", {"p_session_id": session_id}).execute()
    except Exception:
        return False
    return bool(res.data)


def release_session(session_id: str) -> None:
    """เรียกตอน logout เพื่อหมนจอหน้าทันที ไม่ต้องรอ 30 นาที"""
    try:
        _client().rpc("release_session", {"p_session_id": session_id}).execute()
    except Exception:
        pass


def build_navigation():
    pages = [st.Page("home.py", title="หน้าหลัก", icon="🏠", url_path="home")]
    if can_access():
        pages.append(st.Page("pages/22_Bai_50_Thawi.py", title="📋 ใบ 50 ทวิ", icon="📋"))
    return st.navigation(pages, position="sidebar")
