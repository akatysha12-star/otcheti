import streamlit as st
import pandas as pd
import io
import warnings
warnings.filterwarnings('ignore')

# ==================== НАСТРОЙКИ ====================
SPB_ORDER = ["Транспортный", "Димитрова", "Шмидта", "Пулковская", "Благодатная",
             "Энтузиастов", "Серебристый", "Мурино", "Ветеранов", "Туристская",
             "Наука", "Ленинский"]
TMN_ORDER = ["Орджоникидзе", "Мельникайте"]
ALL_RESTAURANTS = SPB_ORDER + TMN_ORDER

RESTAURANT_MAP_FILE1 = {
    "Санкт-Петербург №1": "Транспортный", "Санкт-Петербург №2": "Димитрова",
    "Санкт-Петербург №4": "Шмидта", "Санкт-Петербург №5": "Пулковская",
    "Санкт-Петербург №6": "Благодатная", "Санкт-Петербург №7": "Энтузиастов",
    "Санкт-Петербург №8": "Серебристый", "Санкт-Петербург №13": "Мурино",
    "Санкт-Петербург №15": "Ветеранов", "Санкт-Петербург №16": "Туристская",
    "Санкт-Петербург №18": "Наука", "Санкт-Петербург №20": "Ленинский",
    "Тюмень №2 – Орджоникидзе": "Орджоникидзе", "Тюмень №3 – Мельникайте": "Мельникайте"
}

ADDRESS_MAP = {
    "транспортный": "Транспортный", "димитрова": "Димитрова",
    "шмидта": "Шмидта", "13-я линия": "Шмидта", "васильевск": "Шмидта",
    "пулковская": "Пулковская", "благодатная": "Благодатная",
    "энтузиастов": "Энтузиастов", "серебристый": "Серебристый",
    "мурино": "Мурино", "петровский бульвар": "Мурино",
    "ветеранов": "Ветеранов", "туристская": "Туристская",
    "науки": "Наука", "ленинский": "Ленинский",
    "орджоникидзе": "Орджоникидзе", "мельникайте": "Мельникайте"
}

COMPLAINT_KEYWORDS = {
    "Жалоба на продукт": ["сух", "холодн", "остыл", "невкусн", "плох", "ужас", "отврат", "прогоркл", "испорч", "стар", "жестк", "резин", "волос", "металл", "гряз", "воняет", "гнил", "сырой"],
    "Ошибки приготовления": ["пережар", "недожар", "сыро", "сгорел", "пригорел", "пересолен", "недосолен", "мало соли", "много соли", "непропеч"],
    "Перепутанные/недоложенные позиции": ["не положили", "не доложили", "забыли", "не было", "не дали", "перепутали", "не тот", "вместо", "заменя", "замен", "не хватает", "недоложили", "недодали", "не пришло", "не привезли"],
    "Жалобы на сервис": ["хам", "груб", "невежлив", "неприятн", "игнор", "сбросил", "отказал", "не ответил", "не помог", "не решил", "проблем", "жалоб", "администратор"],
    "Опоздание": ["опозда", "опоздал", "опоздание", "долго", "задерж", "задержк", "не вовремя", "не успел", "час", "полчаса", "30 минут", "40 минут", "50 минут", "1 час", "1.5 часа", "полтора часа"]
}

POSITIVE_KEYWORDS = {
    "Вкус": ["вкусн", "отличн", "превосходн", "восхитит", "бомб", "огонь", "пушк", "шедевр", "идеальн", "сочн"],
    "Быстрая доставка": ["быстр", "оперативн", "вовремя", "минут", "горяч", "с пылу с жару", "молниеносн"],
    "Вежливый персонал": ["вежлив", "приятн", "доброжелат", "внимател", "учтив", "милый", "отзывчив", "профессионал"],
    "Качество": ["качеств", "свеж", "хорош", "отличн", "превосходн", "много начинк", "много сыра"],
    "Атмосфера": ["уютн", "атмосфер", "чист", "комфортн", "приятн", "красив", "интерьер"]
}

# ==================== ФУНКЦИИ ====================
def parse_price(val):
    if pd.isna(val): return None
    s = str(val).replace(",", "").replace(" ", "").strip()
    try: return float(s)
    except: return None

def map_restaurant_file1(val):
    if pd.isna(val): return None
    return RESTAURANT_MAP_FILE1.get(str(val).strip(), None)

def map_restaurant_address(val):
    if pd.isna(val): return None
    val_lower = str(val).lower()
    for key, value in ADDRESS_MAP.items():
        if key in val_lower: return value
    return None

def analyze_text(text, keywords_dict):
    if pd.isna(text) or not str(text).strip(): return []
    text_lower = str(text).lower()
    return [cat for cat, kws in keywords_dict.items() if any(kw in text_lower for kw in kws)]

def calc_stats_site(df, threshold):
    results = []
    for rest in ALL_RESTAURANTS:
        sub = df[df["Ресторан"] == rest]
        five_low = sub[(sub["Рейтинг"] == 5) & (sub["Сумма"] <= threshold)]
        low_count = len(five_low)
        sub_filtered = sub[~((sub["Рейтинг"] == 5) & (sub["Сумма"] <= threshold))]
        row = {"Ресторан": rest}
        for i in range(1, 6): row[str(i)] = int((sub_filtered["Рейтинг"] == i).sum())
        row["всего:"] = sum(row[str(i)] for i in range(1, 6))
        row["Средний рейтинг"] = round(sum(i * row[str(i)] for i in range(1, 6)) / row["всего:"], 2) if row["всего:"] > 0 else 0
        row["Отзывы ≤ порог"] = low_count
        results.append(row)
    return pd.DataFrame(results)

def calc_stats_standard(df):
    results = []
    for rest in ALL_RESTAURANTS:
        sub = df[df["Ресторан"] == rest]
        row = {"Ресторан": rest}
        for i in range(1, 6): row[str(i)] = int((sub["Рейтинг"] == i).sum())
        row["всего:"] = sum(row[str(i)] for i in range(1, 6))
        row["Средний рейтинг"] = round(sum(i * row[str(i)] for i in range(1, 6)) / row["всего:"], 2) if row["всего:"] > 0 else 0
        results.append(row)
    return pd.DataFrame(results)

def add_totals(df, region):
    subset = df[df["Ресторан"].isin(SPB_ORDER)] if region == "СПб" else df[df["Ресторан"].isin(TMN_ORDER)]
    totals = {"Ресторан": f"Итого {region}:"}
    for i in range(1, 6): totals[str(i)] = subset[str(i)].sum()
    totals["всего:"] = sum(totals[str(i)] for i in range(1, 6))
    totals["Средний рейтинг"] = round(sum(i * totals[str(i)] for i in range(1, 6)) / totals["всего:"], 2) if totals["всего:"] > 0 else 0
    if "Отзывы ≤ порог" in df.columns: totals["Отзывы ≤ порог"] = subset["Отзывы ≤ порог"].sum()
    return pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

def calc_summary(df, keywords):
    results = []
    for rest in ALL_RESTAURANTS:
        sub = df[df["Ресторан"] == rest]
        counts = {cat: 0 for cat in keywords.keys()}
        for _, row in sub.iterrows():
            for c in analyze_text(row["Текст"], keywords): counts[c] += 1
        row_data = {"Ресторан": rest, **counts}
        row_data["Всего:"] = sum(counts.values())
        results.append(row_data)
    return pd.DataFrame(results)

def add_summary_totals(df, region, keywords):
    subset = df[df["Ресторан"].isin(SPB_ORDER)] if region == "СПб" else df[df["Ресторан"].isin(TMN_ORDER)]
    totals = {"Ресторан": f"Всего {region}:"}
    for cat in keywords.keys(): totals[cat] = subset[cat].sum()
    totals["Всего:"] = sum(totals[cat] for cat in keywords.keys())
    return pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

# ==================== ИНТЕРФЕЙС ====================
st.title("📅 Отчет «КР месяц»")
st.markdown("Загрузите выгрузки из 3 источников. Пятёрки с суммой заказа ниже порога будут исключены из расчётов.")

col1, col2, col3 = st.columns(3)
with col1: file1 = st.file_uploader("1. Сайт/приложение", type=["xlsx", "xls"])
with col2: file2 = st.file_uploader("2. Агрегаторы", type=["xlsx", "xls"])
with col3: file3 = st.file_uploader("3. Геосервисы", type=["xlsx", "xls"])

price_threshold = st.number_input("Порог суммы (пятёрки ≤ этой суммы исключаются)", value=749, step=10)

if st.button("🚀 Сформировать отчет", type="primary"):
    if not (file1 and file2 and file3):
        st.error("Пожалуйста, загрузите все 3 файла!")
    else:
        with st.spinner("Обработка данных..."):
            try:
                df1 = pd.read_excel(file1)
                df1["Ресторан"] = df1["Ресторан"].apply(map_restaurant_file1)
                df1["Сумма"] = df1["Сумма заказа со скидкой"].apply(parse_price)
                df1["Рейтинг"] = pd.to_numeric(df1["Рейтинг"], errors="coerce")
                df1["Текст"] = df1["Комментарий"].fillna("")
                df1 = df1[["Ресторан", "Рейтинг", "Текст", "Сумма"]].dropna(subset=["Ресторан", "Рейтинг"])

                df2 = pd.read_excel(file2)
                df2["Ресторан"] = df2["Адрес"].apply(map_restaurant_address)
                df2["Рейтинг"] = pd.to_numeric(df2["Оценка"], errors="coerce")
                df2["Текст"] = df2["Отзыв"].fillna("")
                df2 = df2[["Ресторан", "Рейтинг", "Текст"]].dropna(subset=["Ресторан", "Рейтинг"])

                df3_raw = pd.read_excel(file3)
                df3 = df3_raw[df3_raw.get("Статус отзыва", "") != "Удален"].copy() if "Статус отзыва" in df3_raw.columns else df3_raw.copy()
                df3["Ресторан"] = df3.apply(lambda row: map_restaurant_address(row.get("Название филиала", "")) or map_restaurant_address(row.get("Адрес филиала", "")), axis=1)
                df3["Рейтинг"] = pd.to_numeric(df3["Оценка"], errors="coerce")
                df3["Текст"] = df3["Текст отзыва"].fillna("")
                df3 = df3[["Ресторан", "Рейтинг", "Текст"]].dropna(subset=["Ресторан", "Рейтинг"])

                df1_filtered = df1[~((df1["Рейтинг"] == 5) & (df1["Сумма"] <= price_threshold))]
                df_all = pd.concat([df1_filtered[["Ресторан", "Рейтинг", "Текст"]], df2, df3], ignore_index=True)
                df_all_texts = pd.concat([df1[["Ресторан", "Текст"]], df2[["Ресторан", "Текст"]], df3[["Ресторан", "Текст"]]], ignore_index=True)

                stats1, stats2, stats3 = calc_stats_site(df1, price_threshold), calc_stats_standard(df2), calc_stats_standard(df3)
                low_counts = {rest: len(df1[(df1["Ресторан"] == rest) & (df1["Рейтинг"] == 5) & (df1["Сумма"] <= price_threshold)]) for rest in ALL_RESTAURANTS}
                stats_all_results = []
                for rest in ALL_RESTAURANTS:
                    sub = df_all[df_all["Ресторан"] == rest]
                    row = {"Ресторан": rest}
                    for i in range(1, 6): row[str(i)] = int((sub["Рейтинг"] == i).sum())
                    row["всего:"] = sum(row[str(i)] for i in range(1, 6))
                    row["Средний рейтинг"] = round(sum(i * row[str(i)] for i in range(1, 6)) / row["всего:"], 2) if row["всего:"] > 0 else 0
                    row["Отзывы ≤ порог"] = low_counts[rest]
                    stats_all_results.append(row)
                stats_all = pd.DataFrame(stats_all_results)

                for df_stat in [stats1, stats2, stats3, stats_all]:
                    df_stat = add_totals(df_stat, "СПб")
                    df_stat = add_totals(df_stat, "Тюмень")

                comp_all = calc_summary(df_all_texts, COMPLAINT_KEYWORDS)
                pos_all = calc_summary(df_all_texts, POSITIVE_KEYWORDS)
                comp_all = add_summary_totals(comp_all, "СПб", COMPLAINT_KEYWORDS)
                comp_all = add_summary_totals(comp_all, "Тюмень", COMPLAINT_KEYWORDS)
                pos_all = add_summary_totals(pos_all, "СПб", POSITIVE_KEYWORDS)
                pos_all = add_summary_totals(pos_all, "Тюмень", POSITIVE_KEYWORDS)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    cols_site = ["Ресторан", "1", "2", "3", "4", "5", "всего:", "Средний рейтинг", "Отзывы ≤ порог"]
                    cols_standard = ["Ресторан", "1", "2", "3", "4", "5", "всего:", "Средний рейтинг"]
                    
                    stats1[cols_site].to_excel(writer, sheet_name="Оценки", index=False, startrow=0)
                    stats2[cols_standard].to_excel(writer, sheet_name="Оценки", index=False, startrow=len(stats1) + 3)
                    stats3[cols_standard].to_excel(writer, sheet_name="Оценки", index=False, startrow=len(stats1) + len(stats2) + 6)
                    stats_all[cols_site].to_excel(writer, sheet_name="Оценки", index=False, startrow=len(stats1) + len(stats2) + len(stats3) + 9)
                    
                    comp_all.to_excel(writer, sheet_name="Анализ отзывов", index=False, startrow=0)
                    pos_all.to_excel(writer, sheet_name="Анализ отзывов", index=False, startrow=len(comp_all) + 3)

                output.seek(0)
                st.success("✅ Отчет успешно сформирован!")
                st.download_button("📥 Скачать Excel", output, "КР_месяц_отчет.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                st.subheader("Превью: Общий итог")
                st.dataframe(stats_all)
                
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
