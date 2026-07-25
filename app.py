import streamlit as st
import json
from datetime import datetime
import os
import base64

st.set_page_config(
    page_title="Система отчетов КР", 
    layout="wide",
    page_icon="📊"
)

# ==================== ОПРЕДЕЛЕНИЕ ВРЕМЕНИ СУТОК ====================

def get_time_of_day():
    """Определяет время суток"""
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
    """Возвращает CSS в зависимости от времени суток"""
    time_of_day = get_time_of_day()
    
    styles = {
        "night": {
            "header_bg": "linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
            "body_bg": "linear-gradient(180deg, #0f3460 0%, #1a1a2e 40%, #16213e 100%)",
            "cloud_color": "rgba(255,255,255,0.1)",
            "celestial": "🌙",
            "celestial_pos": "top: 10%; right: 10%;",
            "text_color": "#e0e0e0",
            "card_bg": "rgba(30, 30, 60, 0.85)",
            "info_border": "#4a5568"
        },
        "dawn": {
            "header_bg": "linear-gradient(90deg, #ff6b6b 0%, #feca57 50%, #ff9ff3 100%)",
            "body_bg": "linear-gradient(180deg, #ff9a9e 0%, #fad0c4 40%, #ffd1ff 100%)",
            "cloud_color": "rgba(255,200,200,0.6)",
            "celestial": "🌅",
            "celestial_pos": "top: 15%; right: 15%;",
            "text_color": "#2d3748",
            "card_bg": "rgba(255, 240, 245, 0.9)",
            "info_border": "#ff6b6b"
        },
        "morning": {
            "header_bg": "linear-gradient(90deg, #74b9ff 0%, #a29bfe 50%, #fd79a8 100%)",
            "body_bg": "linear-gradient(180deg, #74b9ff 0%, #a8e6cf 40%, #dcedc1 100%)",
            "cloud_color": "rgba(255,255,255,0.7)",
            "celestial": "☀️",
            "celestial_pos": "top: 10%; right: 20%;",
            "text_color": "#1a365d",
            "card_bg": "rgba(255, 255, 255, 0.9)",
            "info_border": "#74b9ff"
        },
        "day": {
            "header_bg": "linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
            "body_bg": "linear-gradient(180deg, #87CEEB 0%, #B0E0E6 40%, #E0F6FF 100%)",
            "cloud_color": "rgba(255,255,255,0.8)",
            "celestial": "☀️",
            "celestial_pos": "top: 5%; right: 10%;",
            "text_color": "#1a365d",
            "card_bg": "rgba(255, 255, 255, 0.9)",
            "info_border": "#667eea"
        },
        "evening": {
            "header_bg": "linear-gradient(90deg, #ff7e5f 0%, #feb47b 50%, #ff6b6b 100%)",
            "body_bg": "linear-gradient(180deg, #ff9a76 0%, #ffcf48 40%, #ff6b6b 100%)",
            "cloud_color": "rgba(255,220,180,0.7)",
            "celestial": "🌇",
            "celestial_pos": "top: 20%; right: 15%;",
            "text_color": "#2d3748",
            "card_bg": "rgba(255, 245, 230, 0.9)",
            "info_border": "#ff7e5f"
        },
        "dusk": {
            "header_bg": "linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
            "body_bg": "linear-gradient(180deg, #667eea 0%, #764ba2 40%, #2d3561 100%)",
            "cloud_color": "rgba(200,180,255,0.5)",
            "celestial": "🌆",
            "celestial_pos": "top: 15%; right: 10%;",
            "text_color": "#e0e0e0",
            "card_bg": "rgba(40, 40, 80, 0.85)",
            "info_border": "#764ba2"
        }
    }
    
    return styles[time_of_day], time_of_day

# Получаем стили
sky_style, time_of_day = get_sky_css()

# ==================== CSS СТИЛИ ====================

st.markdown(f"""
<style>
    /* Основной фон - меняется в зависимости от времени суток */
    .stApp {{
        background: {sky_style['body_bg']};
        min-height: 100vh;
        transition: background 1s ease;
    }}
    
    /* Облака */
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
    
    /* Контент */
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    
    /* ВЕРХНЯЯ ПОЛОСКА (HEADER) - меняется в зависимости от времени суток */
    .stApp header {{
        background: {sky_style['header_bg']} !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: background 1s ease;
    }}
    
    /* Солнце/Луна */
    .celestial-body {{
        position: fixed;
        {sky_style['celestial_pos']}
        font-size: 3em;
        z-index: 2;
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
    }}
    
    /* Звёзды для ночи */
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
    
    /* Заголовок */
    h1 {{
        color: {sky_style['text_color']};
        text-shadow: 2px 2px 4px rgba(255,255,255,0.3);
        font-size: 3em;
        font-weight: bold;
    }}
    
    /* Карточки */
    .report-card {{
        background: {sky_style['card_bg']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    
    .report-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }}
    
    /* Боковое меню */
    .css-1d391kg {{
        background: {sky_style['header_bg']};
    }}
    
    /* Кнопки */
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
    
    /* Праздничная секция с GIF */
    .holiday-section {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
        padding: 20px;
        background: {sky_style['card_bg']};
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex-wrap: wrap;
    }}
    
    .holiday-banner {{
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 50%, #ffd700 100%);
        color: #1a365d;
        padding: 15px 30px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3em;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
        animation: shimmer 3s infinite;
        flex: 1;
        min-width: 250px;
    }}
    
    @keyframes shimmer {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    /* GIF контейнер */
    .gif-container {{
        text-align: center;
        flex: 0 0 auto;
    }}
    
    .gif-container img {{
        max-width: 200px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    /* Блоки информации */
    .info-block {{
        background: {sky_style['card_bg']};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid {sky_style['info_border']};
    }}
    
    /* Время суток индикатор */
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

# ==================== ФУНКЦИЯ ДЛЯ ПРАЗДНИКОВ ====================

def get_today_holiday():
    """Получает праздник на сегодня из JSON файла"""
    try:
        holidays_file = os.path.join(os.path.dirname(__file__), 'holidays.json')
        
        if os.path.exists(holidays_file):
            with open(holidays_file, 'r', encoding='utf-8') as f:
                holidays = json.load(f)
            
            today = datetime.now()
            today_key = f"{today.month:02d}-{today.day:02d}"
            
            if today_key in holidays:
                return holidays[today_key]
        
        return "🌟 Хорошего дня!"
    except Exception as e:
        return "🌟 Отличного настроения!"

# ==================== ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ GIF ====================

def get_local_gif():
    """Загружает локальную GIF из папки assets/"""
    try:
        gif_path = os.path.join(os.path.dirname(__file__), 'assets', 'animation.gif')
        if os.path.exists(gif_path):
            with open(gif_path, 'rb') as f:
                gif_bytes = f.read()
                gif_base64 = base64.b64encode(gif_bytes).decode()
                return f"data:image/gif;base64,{gif_base64}"
        return None
    except:
        return None

# ==================== ГЛАВНАЯ СТРАНИЦА ====================

# Солнце/Луна
st.markdown(f'<div class="celestial-body">{sky_style["celestial"]}</div>', unsafe_allow_html=True)

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

# Заголовок
st.title("📊 Система формирования отчётов")

# Приветствие
st.markdown(f"""
<div class="info-block">
    <h3 style="color: {sky_style['text_color']}; margin-top: 0;"> Доброго прекрасного денёчка!</h3>
    <p style="font-size: 1.1em; color: {sky_style['text_color']};">
        Здесь вы можете формировать отчёты в один клик.<br>
        👈 <b>Выберите нужный отчёт в боковом меню слева.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# Доступные отчёты
st.markdown(f"""
<div class="report-card">
    <h3 style="color: {sky_style['text_color']}; margin-top: 0;">📋 Доступные отчёты:</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']};">📅 КР месяц</h4>
        <p style="color: {sky_style['text_color']};">Сводный отчёт за месяц с фильтрацией</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']};">📆 КР неделя</h4>
        <p style="color: {sky_style['text_color']};">Еженедельный сводный отчёт</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']};">🍕 Продукт</h4>
        <p style="color: {sky_style['text_color']};">Полный отчёт по продуктам (5 листов)</p>
    </div>
    """, unsafe_allow_html=True)

# Праздник и GIF внизу
holiday_message = get_today_holiday()
gif_data = get_local_gif()

if gif_data:
    st.markdown(f"""
    <div class="holiday-section">
        <div class="holiday-banner">
            🎉 {holiday_message}
        </div>
        <div class="gif-container">
            <img src="{gif_data}" alt="Праздничная анимация">
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="holiday-banner" style="max-width: 600px; margin: 30px auto;">
        🎉 {holiday_message}
    </div>
    """, unsafe_allow_html=True)

# Индикатор времени суток
time_names = {
    "night": "🌙 Ночь",
    "dawn": "🌅 Рассвет",
    "morning": "🌤️ Утро",
    "day": "☀️ День",
    "evening": "🌇 Вечер",
    "dusk": " Сумерки"
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
