import streamlit as st
from datetime import datetime, timezone, timedelta

from config.brand import COLORS, SLOGAN, BRAND_NAME, FONT_FAMILY

st.set_page_config(
    page_title=f"{BRAND_NAME} | Отчёты",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MSK = timezone(timedelta(hours=3))
hour = datetime.now(MSK).hour

if 5 <= hour < 12:
    greeting = "Доброе утро"
elif 12 <= hour < 18:
    greeting = "Добрый день"
elif 18 <= hour < 23:
    greeting = "Добрый вечер"
else:
    greeting = "Доброй ночи"

css = f"""
<style> @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700;800&display=swap'); #MainMenu, footer {{visibility:hidden;}} .stApp {{background:{COLORS['dough']};}} html, body, [class*="css"] {{font-family:{FONT_FAMILY};}} .block-container {{max-width:960px;padding-top:14vh;padding-bottom:8vh;}} .hero {{background:{COLORS['white']};border-radius:28px;padding:56px 40px;text-align:center;box-shadow:0 12px 32px rgba(17,72,52,0.10);animation:fadeIn .5s ease both;}} .logo {{display:inline-block;background:{COLORS['tomato']};color:{COLORS['white']};font-weight:800;font-size:20px;letter-spacing:1.5px;text-transform:uppercase;padding:10px 24px;border-radius:12px;}} .accent {{width:72px;height:8px;border-radius:999px;background:{COLORS['basil']};margin:26px auto;}} .hero h1 {{margin:0;font-size:52px;line-height:1.05;color:{COLORS['olive']};font-weight:800;text-transform:uppercase;}} .slogan {{margin:16px 0 0;color:{COLORS['baked_tomato']};font-size:18px;font-weight:700;letter-spacing:.3px;}} @keyframes fadeIn {{from {{opacity:0;transform:translateY(10px);}} to {{opacity:1;transform:none;}}}} </style>
"""

st.markdown(css, unsafe_allow_html=True)

hero_html = f"""
<div class="hero">
    <div class="logo">{BRAND_NAME}</div>
    <div class="accent"></div>
    <h1>{greeting}!</h1>
    <p class="slogan">{SLOGAN}</p>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)
