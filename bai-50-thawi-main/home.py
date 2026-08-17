"""home.py — หน้าแรกของ 📋 ใบ 50 ทวิ"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import style
from auth import can_access

st.set_page_config(page_title="📋 ใบ 50 ทวิ", page_icon="📋", layout="wide")
style.inject()

user_name = st.session_state.get("customer_name", "")

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0F2952 0%, #1A3F7A 50%, #2563EB 100%);
    border-radius: 20px; padding: 28px 36px; margin-bottom: 24px; color: white;
">
  <div style="display:inline-block;background:rgba(255,255,255,0.18);border-radius:20px;
              padding:3px 14px;font-size:13px;font-weight:600;margin-bottom:10px;">
    👤 {user_name}
  </div>
  <div style="font-size:24px;font-weight:700;margin:0 0 6px;">📋 ใบ 50 ทวิ</div>
</div>
""", unsafe_allow_html=True)

if can_access():
    st.success("บัญชีนี้มีสิทธิ์ใช้งานเครื่องมือนี้")
    exp = st.session_state.get("entitlement_expires_at")
    if exp:
        st.caption(f"สิทธิ์หมดอายุ: {exp}")
    if st.button("🚀 เปิด 📋 ใบ 50 ทวิ", type="primary"):
        st.switch_page("pages/22_Bai_50_Thawi.py")
else:
    st.warning("บัญชีนี้ยังไม่มีสิทธิ์ใช้งานเครื่องมือนี้ กรุณาซื้อเครื่องมือนี้ที่ Store ก่อน")
    st.link_button("ไปที่ Store", os.environ.get("STORE_URL", "https://store.alternatax.app"))
