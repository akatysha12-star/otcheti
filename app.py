# КЛИКАБЕЛЬНЫЕ КАРТОЧКИ С КНОПКАМИ
with col1:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']}; margin: 0;">📅 КР месяц</h4>
        <p style="color: {sky_style['text_color']}; margin: 5px 0 0; font-size: 1em;">Сводный отчёт за месяц с фильтрацией</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📅 Перейти к отчёту", key="btn_month", use_container_width=True):
        st.switch_page("pages/KR month.py")

with col2:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']}; margin: 0;"> КР неделя</h4>
        <p style="color: {sky_style['text_color']}; margin: 5px 0 0; font-size: 1em;">Еженедельный сводный отчёт</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📆 Перейти к отчёту", key="btn_week", use_container_width=True):
        st.switch_page("pages/KR week.py")

with col3:
    st.markdown(f"""
    <div class="report-card">
        <h4 style="color: {sky_style['text_color']}; margin: 0;">🍕 Продукт</h4>
        <p style="color: {sky_style['text_color']}; margin: 5px 0 0; font-size: 1em;">Полный отчёт по продуктам</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🍕 Перейти к отчёту", key="btn_produkt", use_container_width=True):
        st.switch_page("pages/prodykt.py")
