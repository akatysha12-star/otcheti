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

# ==================== CSS СТИЛИ ====================

st.markdown("""
<style>
    /* Основной фон - градиент как в отчёте Продукт */
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #B0E0E6 40%, #E0F6FF 100%);
        min-height: 100vh;
    }
    
    /* Облака */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(ellipse 120px 60px at 15% 20%, rgba(255,255,255,0.8) 0%, transparent 70%),
            radial-gradient(ellipse 180px 80px at 25% 18%, rgba(255,255,255,0.6) 0%, transparent 70%),
            radial-gradient(ellipse 100px 50px at 60% 15%, rgba(255,255,255,0.7) 0%, transparent 70%),
            radial-gradient(ellipse 150px 70px at 70% 12%, rgba(255,255,255,0.5) 0%, transparent 70%),
            radial-gradient(ellipse 200px 90px at 85% 25%, rgba(255,255,255,0.6) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Контент */
    .stApp > div {
        position: relative;
        z-index: 1;
    }
    
    /* ВЕРХНЯЯ ПОЛОСКА (HEADER) - измените цвет здесь */
    .stApp header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Заголовок */
    h1 {
        color: #1a365d;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        font-size: 3em;
        font-weight: bold;
    }
    
    /* Карточки */
    .report-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .report-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Боковое меню */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Праздничная строка с гифкой */
    .holiday-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .holiday-banner {
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
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Гифка контейнер */
    .gif-container {
        text-align: center;
        flex: 0 0 auto;
    }
    
    .gif-container img {
        max-width: 200px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Блоки информации */
    .info-block {
        background: rgba(255,255,255,0.85);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ==================== ФУНКЦИЯ ДЛЯ ПРАЗДНИКОВ ====================

def get_today_holiday():
    """Получает праздник на сегодня из JSON файла"""
    try:
        # Путь к файлу holidays.json
        holidays_file = os.path.join(os.path.dirname(__file__), 'holidays.json')
        
        if os.path.exists(holidays_file):
            with open(holidays_file, 'r', encoding='utf-8') as f:
                holidays = json.load(f)
            
            # Получаем сегодняшнюю дату в формате ММ-ДД
            today = datetime.now()
            today_key = f"{today.month:02d}-{today.day:02d}"
            
            # Проверяем, есть ли праздник сегодня
            if today_key in holidays:
                return holidays[today_key]
        
        return " Хорошего дня!"
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

# Заголовок
st.title(" Система формирования отчётов")

# Приветствие
st.markdown("""
<div class="info-block">
    <h3 style="color: #1a365d; margin-top: 0;">👋 Доброго прекрасного денёчка!</h3>
    <p style="font-size: 1.1em;">
        Здесь вы можете формировать отчёты в один клик.<br>
        👈 <b>Выберите нужный отчёт в боковом меню слева.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# Доступные отчёты
st.markdown("""
<div class="report-card">
    <h3 style="color: #1a365d; margin-top: 0;">📋 Доступные отчёты:</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="report-card">
        <h4 style="color: #667eea;">📅 КР месяц</h4>
        <p>Сводный отчёт за месяц с фильтрацией</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="report-card">
        <h4 style="color: #667eea;">📆 КР неделя</h4>
        <p>Еженедельный сводный отчёт</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="report-card">
        <h4 style="color: #667eea;">🍕 Продукт</h4>
        <p>Полный отчёт по продуктам (5 листов)</p>
    </div>
    """, unsafe_allow_html=True)

# Праздник и GIF внизу
holiday_message = get_today_holiday()
gif_data = get_local_gif()

# Если есть локальная GIF, показываем её рядом с праздником
if gif_data:
    st.markdown(f"""
    <div class="holiday-section">
        <div class="holiday-banner">
             {holiday_message}
        </div>
        <div class="gif-container">
            <img src="{gif_data}" alt="Праздничная анимация">
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Если GIF нет, показываем только праздник
    st.markdown(f"""
    <div class="holiday-banner" style="max-width: 600px; margin: 30px auto;">
         {holiday_message}
    </div>
    """, unsafe_allow_html=True)

# Дополнительная информация
st.markdown("""
<div style="margin-top: 40px; text-align: center; color: #1a365d; opacity: 0.8;">
    <p> <i>Все отчёты генерируются автоматически и сохраняются в формате Excel</i></p>
    <p style="font-size: 0.9em; margin-top: 20px;">
        Система отчётов КР © 2026
    </p>
</div>
""", unsafe_allow_html=True)
