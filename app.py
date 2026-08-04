import streamlit as st
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="Главная",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MSK = timezone(timedelta(hours=3))
now = datetime.now(MSK)
hour = now.hour

if 5 <= hour < 12:
    greeting = "Доброе утро"
elif 12 <= hour < 18:
    greeting = "Добрый день"
elif 18 <= hour < 23:
    greeting = "Добрый вечер"
else:
    greeting = "Доброй ночи"

BRAND = {
    "bg": "#FFF8F2",
    "card": "#FFFFFF",
    "primary": "#E23B2E",
    "text": "#2B211C",
    "border": "#F0E3D7",
}

css = f"""
<style>
#MainMenu, footer {{visibility:hidden;}}
.stApp {{background:{BRAND['bg']};}}
.block-container {{max-width:920px;padding-top:18vh;padding-bottom:10vh;}}
.hero {{background:{BRAND['card']};border:1px solid {BRAND['border']};border-radius:28px;padding:64px 32px;text-align:center;box-shadow:0 12px 32px rgba(0,0,0,0.06);animation:fadeIn .5s ease both;}}
.hero .accent {{width:64px;height:8px;border-radius:999px;background:{BRAND['primary']};margin:0 auto 26px;}}
.hero h1 {{margin:0;font-size:46px;line-height:1.1;color:{BRAND['text']};font-weight:700;}}
@keyframes fadeIn {{from {{opacity:0;transform:translateY(10px);}} to {{opacity:1;transform:none;}}}}
</style>
"""

st.markdown(css)

st.markdown(
    f"""
    <div class="hero">
        <div class="accent"></div>
        <h1>{greeting}!</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
