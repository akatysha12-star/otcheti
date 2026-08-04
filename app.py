import streamlit as st
from datetime import datetime, timezone, timedelta

from config.brand import COLORS, SLOGAN, BRAND_NAME, FONT_FAMILY

st.set_page_config(
    page_title=f"{BRAND_NAME} | Отчёты",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
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

WEEKDAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
date_line = f"{WEEKDAYS[now.weekday()]}, {now.strftime('%d.%m.%Y')} · {now.strftime('%H:%M')} МСК"

css = f"""
<style> @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700;800&display=swap'); #MainMenu, footer {{visibility:hidden;}} .stApp, [data-testid="stAppViewContainer"] {{background-color:{COLORS['dough']};background-image:radial-gradient(rgba(225,45,38,0.05) 1.5px, transparent 1.5px);background-size:24px 24px;}} html, body, [class*="css"] {{font-family:{FONT_FAMILY};}} .block-container {{max-width:960px;padding-top:10vh;padding-bottom:6vh;}} .hero {{background:{COLORS['white']};border-radius:28px;padding:48px 40px;text-align:center;box-shadow:0 12px 32px rgba(17,72,52,0.10);animation:fadeIn .5s ease both;}} .badge {{display:inline-block;background:{COLORS['cheese']};color:{COLORS['olive']};font-weight:800;font-size:14px;letter-spacing:.5px;padding:8px 18px;border-radius:999px;transform:rotate(-2deg);box-shadow:0 4px 10px rgba(17,72,52,0.15);margin-bottom:22px;}} .logo {{display:inline-block;background:{COLORS['tomato']};color:{COLORS['white']};font-weight:800;font-size:20px;letter-spacing:1.5px;text-transform:uppercase;padding:10px 24px;border-radius:12px;}} .accent {{width:72px;height:8px;border-radius:999px;background:{COLORS['basil']};margin:26px auto;}} .hero h1 {{margin:0;font-size:52px;line-height:1.05;color:{COLORS['olive']};font-weight:800;text-transform:uppercase;}} .slogan {{margin:16px 0 0;color:{COLORS['baked_tomato']};font-size:18px;font-weight:700;letter-spacing:.3px;}} .cities {{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:30px;}} .city {{display:flex;align-items:center;gap:8px;background:{COLORS['white']};border:1px solid rgba(17,72,52,0.15);border-radius:999px;padding:8px 18px;font-size:14px;font-weight:700;color:{COLORS['olive']};}} .dot {{width:8px;height:8px;border-radius:50%;}} .spb {{background:{COLORS['tomato']};}} .tmn {{background:{COLORS['basil']};}} .footer {{margin-top:26px;text-align:center;color:{COLORS['basil']};font-weight:700;font-size:15px;letter-spacing:.3px;animation:fadeIn .7s ease both;}} @keyframes fadeIn {{from {{opacity:0;transform:translateY(10px);}} to {{opacity:1;transform:none;}}}} </style>
"""

st.markdown(css, unsafe_allow_html=True)

page_html = f"""
<div class="hero">
    <div class="badge">{date_line}</div>
    <div class="logo">{BRAND_NAME}</div>
    <div class="accent"></div>
    <h1>{greeting}!</h1>
    <p class="slogan">{SLOGAN}</p>
    <div class="cities">
        <div class="city"><span class="dot spb"></span>Санкт-Петербург · 12 ресторанов</div>
        <div class="city"><span class="dot tmn"></span>Тюмень · 2 ресторана</div>
    </div>
</div>
<p class="footer">Когда есть вкус, есть эмоции.</p>
"""

st.markdown(page_html, unsafe_allow_html=True)
