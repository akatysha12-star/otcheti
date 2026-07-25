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
