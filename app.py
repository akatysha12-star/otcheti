import base64
import json
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

# ==================== ПУТИ К ФАЙЛАМ ====================

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
HOLIDAYS_FILE = BASE_DIR / "holidays.json"

# ==================== ОПРЕДЕЛЕНИЕ ВРЕМЕНИ СУТОК ====================

def get_time_of_day():
    hour = datetime.now().hour
    if 0 <= hour < 5:
        return "night"
    elif 5 <= hour < 7:
        return "dawn"
    elif 7 <= hour < 10:
        return "morning"
    elif 10 <= hour < 17:
        return "day"
    elif 17 <= hour < 20:
        return "evening"
    elif 20 <= hour < 22:
        return "dusk"
    else:
        return "night"

def get_sky_css():
    time_of_day = get_time_of_day()
    
    styles = {
        "night": {
            "header_bg": "linear-gradient(90deg, #1e3a5f 0%, #2d5a87 100%)",
            "body_bg": "linear-gradient(180deg, #0f3460 0%, #1a1a2e 40%, #16213e 100%)",
            "cloud_color": "rgba(255,255,255,0.1)",
            "celestial": "🌙",
            "text_color": "#e0e0e0",
            "card_bg": "rgba(30, 30, 60, 0.85)",
            "info_border": "#4a5568",
            "sidebar_bg": "linear-gradient(180deg, #2d5a87 0%, #1e3a5f 100%)",
            "sidebar_text": "#b8d4e8"
        },
        "dawn": {
            "header_bg": "linear-gradient(90deg, #ff9a76 0%, #ffcf48 100%)",
            "body_bg": "linear-gradient(180deg, #ff9a9e 0%, #fad0c4 40%, #ffd1ff 100%)",
            "cloud_color": "rgba(255,200,200,0.6)",
            "celestial": "",
            "text_color": "#2d3748",
            "card_bg": "rgba(255, 240, 245, 0.9)",
            "info_border": "#ff6b6b",
            "sidebar_bg": "linear-gradient(180deg, #ffe4e1 0%, #ffd1dc 100%)",
            "sidebar_text": "#8b4513"
        },
        "morning": {
            "header_bg": "linear-gradient(90deg, #87ceeb 0%, #98d8e8 100%)",
            "body_bg": "linear-gradient(180deg, #87ceeb 0%, #b0e0e6 40%, #e0f6ff 100%)",
            "cloud_color": "rgba(255,255,255,0.7)",
            "celestial": "🌤️",
            "text_color": "#1a365d",
            "card_bg": "rgba(255, 255, 255, 0.9)",
            "info_border": "#74b9ff",
            "sidebar_bg": "linear-gradient(180deg, #e0f2fe 0%, #bae6fd 100%)",
            "sidebar_text": "#1e3a5f"
        },
        "day": {
            "header_bg": "linear-gradient(90deg, #87ceeb 0%, #b0e0e6 100%)",
            "body_bg": "linear-gradient(180deg, #87CEEB 0%, #B0E0E6 40%, #E0F6FF 100%)",
            "cloud_color": "rgba(255,255,255,0.8)",
            "celestial": "☀️",
            "text_color": "#1a365d",
            "card_bg": "rgba(255, 255, 255, 0.9)",
            "info_border": "#2c5282",
            "sidebar_bg": "linear-gradient(180deg, #e0f2fe 0%, #bae6fd 100%)",
            "sidebar_text": "#1e3a5f"
        },
        "evening": {
            "header_bg": "linear-gradient(90deg, #ff9a76 0%, #ffcf48 100%)",
            "body_bg": "linear-gradient(180deg, #ff9a76 0%, #ffcf48 40%, #ff6b6b 100%)",
            "cloud_color": "rgba(255,220,180,0.7)",
            "celestial": "🌇",
            "text_color": "#2d3748",
            "card_bg": "rgba(255, 245, 230, 0.9)",
            "info_border": "#ff7e5f",
            "sidebar_bg": "linear-gradient(180deg, #ffe4e1 0%, #ffd1dc 100%)",
            "sidebar_text": "#8b4513"
        },
        "dusk": {
            "header_bg": "linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
            "body_bg": "linear-gradient(180deg, #667eea 0%, #764ba2 40%, #2d3561 100%)",
            "cloud_color": "rgba(200,180,255,0.5)",
            "celestial": "🌆",
            "text_color": "#e0e0e0",
            "card_bg": "rgba(40, 40, 80, 0.85)",
            "info_border": "#764ba2",
            "sidebar_bg": "linear-gradient(180deg, #e6e6fa 0%, #d8bfd8 100%)",
            "sidebar_text": "#4a4a6a"
        }
    }
    
    return styles[time_of_day], time_of_day

sky_style, time_of_day = get_sky_css()

# ==================== CSS СТИЛИ ====================

st.markdown(f"""
<style>
    .stApp {{
        background: {sky_style['body_bg']};
        min-height: 100vh;
        transition: background 1s ease;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(ellipse 120px 60px at 15% 20%, {sky_style['cloud_color']} 0%, transparent 70%),
            radial-gradient(ellipse 180px 80px at 25% 18%, {sky_style['cloud_color']} 0%, transparent 70%),
            radial-gradient(ellipse 100px 50px at 60% 15%, {sky_style['cloud_color']} 0%, transparent 70%),
            radial-gradient(ellipse 150px 70px at 70% 12%, {sky_style['cloud_color']} 0%, transparent 70%),
            radial-gradient(ellipse 200px 90px at 85% 25%, {sky_style['cloud_color']} 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }}
    
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    
    .stApp header {{
        background: {sky_style['header_bg']} !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}
    
    /* ЗАГОЛОВОК С СОЛНЦЕМ - через flexbox */
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        padding: 10px 0;
    }}
    
    .title-container h1 {{
        margin: 0;
        flex: 1;
    }}
    
    /* СОЛНЦЕ С АНИМАЦИЕЙ */
    .celestial-body {{
        font-size: 3em;
        margin-left: 20px;
        flex-shrink: 0;
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-15px); }}
    }}
    
    .stars {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }}
    
    .star {{
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s ease-in-out infinite;
    }}
    
    @keyframes twinkle {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 1; }}
    }}
    
    h1 {{
        color: {sky_style['text_color']};
        text-shadow: 2px 2px 4px rgba(255,255,255,0.3);
        font-size: 3em;
        font-weight: bold;
    }}
    
    .report-card {{
        background: {sky_style['card_bg']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        cursor: pointer;
    }}
    
    .report-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    .stSidebar {{
        background: {sky_style['sidebar_bg']} !important;
    }}
    
    .stSidebar > div {{
        background: {sky_style['sidebar_bg']} !important;
    }}
    
    .stSidebar .stMarkdown,
    .stSidebar .stText,
    .stSidebar label,
    .stSidebar span,
    .stSidebar a {{
        color: {sky_style['sidebar_text']} !important;
        font-weight: 500;
    }}
    
    .stSidebar a:hover {{
        color: #ff6b6b !important;
    }}
    
    .stButton > button {{
        background: {sky_style['header_bg']};
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    .holiday-section {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
        padding: 25px;
        background: {sky_style['card_bg']};
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex-wrap: wrap;
        border: 3px solid gold;
    }}
    
    .holiday-banner {{
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 50%, #ffd700 100%);
        color: #1a365d;
        padding: 20px 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.4em;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255,215,0,0.4);
        animation: shimmer 3s infinite;
        flex: 1;
        min-width: 250px;
    }}
    
    @keyframes shimmer {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .gif-container {{
        text-align: center;
        flex: 0 0 auto;
    }}
    
    .gif-container img {{
        max-width: 250px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border: 3px solid gold;
    }}
    
    .info-block {{
        background: {sky_style['card_bg']};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid {sky_style['info_border']};
    }}
    
    .time-indicator {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 0.9em;
        color: {sky_style['text_color']};
        z-index: 10;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== ФУНКЦИИ ====================

def get_today_holiday():
    """Возвращает праздник на сегодняшний день."""
    try:
        if not HOLIDAYS_FILE.exists():
            return "🌟 Хорошего дня!"
        with open(HOLIDAYS_FILE, "r", encoding="utf-8") as f:
            holidays = json.load(f)
        today_key = datetime.now().strftime("%m-%d")
        return holidays.get(today_key, "🌟 Хорошего дня!")
    except Exception:
        return "🌟 Отличного настроения!"

def get_greeting():
    """Возвращает приветствие в зависимости от времени суток."""
    greetings = {
        "morning": "🌤 Доброго утречка!",
        "day": "☀ Доброго денёчка!",
        "evening": "🌙 Не засидись допоздна 😊",
        "dusk": "🌙 Не засидись допоздна 😊",
        "night": "👀 Пупупум... а кто это тут не спит?",
        "dawn": "🌤 Доброго утречка!"
    }
    return greetings.get(time_of_day, "👋 Добро пожаловать!")

def get_local_gif():
    """Загружает GIF из папки assets."""
    possible_names = ["animation.gif", "animation.GIF", "Animation.gif", "my_gif.gif"]
    try:
        for name in possible_names:
            gif_path = ASSETS_DIR / name
            if gif_path.exists():
                with open(gif_path, "rb") as f:
                    gif_base64 = base64.b64encode(f.read()).decode()
                return f"data:image/gif;base64,{gif_base64}"
    except Exception:
        pass
    return None
    try:
        possible_names = ['animation.gif', 'animation.GIF', 'Animation.gif', 'my_gif.gif']
        for name in possible_names:
            gif_path = os.path.join(os.path.dirname(__file__), 'assets', name)
            if os.path.exists(gif_path):
                with open(gif_path, 'rb') as f:
                    gif_bytes = f.read()
                    gif_base64 = base64.b64encode(gif_bytes).decode()
                    return f"data:image/gif;base64,{gif_base64}"
        return None
    except Exception as e:
        return None

# ==================== ГЛАВНАЯ СТРАНИЦА ====================

# Заголовок с солнцем через flexbox
st.markdown(f"""
<div class="title-container">
    <h1>📊 Система формирования отчётов</h1>
    <div class="celestial-body">{sky_style["celestial"]}</div>
</div>
""", unsafe_allow_html=True)

# Звёзды для ночи
if time_of_day == "night":
    stars_html = '<div class="stars">'
    import random
    for _ in range(50):
        left = random.randint(0, 100)
        top = random.randint(0, 50)
        size = random.randint(1, 3)
        delay = random.uniform(0, 3)
        stars_html += f'<div class="star" style="left: {left}%; top: {top}%; width: {size}px; height: {size}px; animation-delay: {delay}s;"></div>'
    stars_html += '</div>'
    st.markdown(stars_html, unsafe_allow_html=True)

# Приветствие
st.markdown(f"""
<div class="info-block">
   <h3 style="color: {sky_style['text_color']}; margin-top: 0;">
    {get_greeting()}
</h3>
    <p style="font-size: 1.1em; color: {sky_style['text_color']};">
        Здесь вы можете формировать отчёты в один клик.<br>
        👈 <b>Выберите нужный отчёт в боковом меню слева.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# Доступные отчёты
st.markdown(f"""
<div class="report-card">
    <h3 style="color: {sky_style['text_color']}; margin-top: 0;"> Доступные отчёты:</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# КЛИКАБЕЛЬНЫЕ КАРТОЧКИ С ПЕРЕХОДОМ НА ОТЧЁТЫ
def create_report_card(title, description, page_name, icon):
    st.markdown(f"""
    <div class="report-card" onclick="window.parent.document.location.href='/{page_name}'" style="cursor: pointer;">
        <h4 style="color: {sky_style['text_color']}; margin: 0;">{icon} {title}</h4>
        <p style="color: {sky_style['text_color']}; margin: 5px 0 0; font-size: 1em;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

with col1:
    create_report_card("КР месяц", "Сводный отчёт за месяц с фильтрацией", "kr_month", "📅")

with col2:
    create_report_card("КР неделя", "Еженедельный сводный отчёт", "kr_week", "📆")

with col3:
    create_report_card("Продукт", "Полный отчёт по продуктам", "produkt", "🍕")

# Праздник и GIF
holiday_message = get_today_holiday()
gif_data = get_local_gif()

congratulation = f"🎉 Сегодня праздник {holiday_message}! 🎊"

if gif_data:
    st.markdown(f"""
    <div class="holiday-section">
        <div class="holiday-banner">
            {congratulation}
        </div>
        <div class="gif-container">
            <img src="{gif_data}" alt="Праздничная анимация">
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="holiday-banner" style="max-width: 600px; margin: 30px auto;">
        {congratulation}
    </div>
    """, unsafe_allow_html=True)

# Индикатор времени
time_names = {
    "night": " Ночь",
    "dawn": " Рассвет",
    "morning": "🌤️ Утро",
    "day": "☀️ День",
    "evening": "🌇 Вечер",
    "dusk": "🌆 Сумерки"
}
current_time = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="time-indicator">{time_names[time_of_day]} | {current_time}</div>', unsafe_allow_html=True)

# Дополнительная информация
st.markdown(f"""
<div style="margin-top: 40px; text-align: center; color: {sky_style['text_color']}; opacity: 0.8;">
    <p>💡 <i>Все отчёты генерируются автоматически и сохраняются в формате Excel</i></p>
    <p style="font-size: 0.9em; margin-top: 20px;">
        Система отчётов КР © 2026
    </p>
</div>
""", unsafe_allow_html=True)
