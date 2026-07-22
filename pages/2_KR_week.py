import streamlit as st
import pandas as pd
import io
import warnings
warnings.filterwarnings('ignore')

# ==================== НАСТРОЙКИ ====================
RESTAURANT_MAP = {
    "Санкт-Петербург №1": "01 Транспортный", "Санкт-Петербург №2": "02 Димитрова",
    "Санкт-Петербург №4": "04 Шмидта", "Санкт-Петербург №5": "05 Пулковская",
    "Санкт-Петербург №6": "06 Благодатная", "Санкт-Петербург №7": "07 Энтузиастов",
    "Санкт-Петербург №8": "08 Серебристый", "Санкт-Петербург №13": "13 Мурино",
    "Санкт-Петербург №15": "15 Ветеранов", "Санкт-Петербург №16": "16 Туристская",
    "Санкт-Петербург №18": "18 Наука", "Санкт-Петербург №20": "20 Ленинский",
    "Тюмень №2 – Орджоникидзе": "ТМН 2 (Орджоникидзе)", "Тюмень №3 – Мельникайте": "ТМН 3 (Мельникайте)"
}

COMPLAINT_KEYWORDS = {
    "Жалоба на продукт": ["сух", "холодн", "остыл", "невкусн", "плох", "ужас", "отврат", "прогоркл", "испорч", "стар", "жестк", "резин", "волос", "металл", "гряз", "воняет", "гнил", "сырой"],
    "Ошибки приготовления": ["пережар", "недожар", "сыро", "сгорел", "пригорел", "пересолен", "недосолен", "мало соли", "много соли", "непропеч"],
    "Перепутанные / недоложенные позиции": ["не положили", "не доложили", "забыли", "не было", "не дали", "перепутали", "не тот", "вместо", "заменя", "замен", "не хватает", "недоложили", "недодали", "не пришло", "не привезли"],
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
def map_restaurant_file1(val):
    if pd.isna(val): return None
    return RESTAURANT_MAP.get(str(val).strip(), None)

def map_restaurant_address(val):
    if pd.isna(val): return None
    val_lower = str(val).lower()
    address_map = {
        "транспортный": "01 Транспортный", "димитрова": "02 Димитрова",
        "шмидта": "04 Шмидта", "13-я линия": "04 Шмидта", "васильевск": "04 Шмидта",
        "пулковская": "05 Пулковская", "благодатная": "06 Благодатная",
        "энтузиастов": "07 Энтузиастов", "серебристый": "08 Серебристый",
        "мурино": "13 Мурино", "петровский бульвар": "13 Мурино",
        "ветеранов": "15 Ветеранов", "туристская": "16 Туристская",
        "науки": "18 Наука", "ленинский": "20 Ленинский",
        "орджоникидзе": "ТМН 2 (Орджоникидзе)", "мельникайте": "ТМН 3 (Мельникайте)"
    }
    for key, value in address_map.items():
        if key in val_lower: return value
    return None

def analyze_text(text, keywords_dict):
    if pd.isna(text) or not str(text).strip(): return []
    text_lower = str(text).lower()
    return [cat for cat, kws in keywords_dict.items() if any(kw in text_lower for kw in kws)]

def calc_stats(df):
    results = []
    for rest in sorted(df["Ресторан"].unique()):
        sub = df[df["Ресторан"] == rest]
        row = {"Ресторан": rest}
        for i in range(1, 6): row[str(i)] = int((sub["Рейтинг"] == i).sum())
        row["всего:"] = sum(row[str(i)] for i in range(1, 6))
        row["Средний рейтинг"] = round(sum(i * row[str(i)] for i in range(1, 6)) / row["всего:"], 2) if row["всего:"] > 0 else 0
        results.append(row)
    return pd.DataFrame(results)

def add_totals(df, region):
    subset = df[~df["Ресторан"].str.contains("ТМН", na=False)] if region == "СПб" else df[df["Ресторан"].str.contains("ТМН", na=False)]
    if len(subset) == 0: return df
    totals = {"Ресторан": f"Итого {region}:"}
    for i in range(1, 6): totals[str(i)] = subset[str(i)].sum()
    totals["всего:"] = sum(totals[str(i)] for i in range(1, 6))
    totals["Средний рейтинг"] = round(sum(i * totals[str(i)] for i in range(1, 6)) / totals["всего:"], 2) if totals["всего:"] > 0 else 0
    return pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

def calc_summary_transposed(df, keywords_dict):
    results = []
    for rest in sorted(df["Ресторан"].unique()):
        sub = df[df["Ресторан"] == rest]
        counts = {cat: 0 for cat in keywords_dict.keys()}
        for _, row in sub.iterrows():
            for c in analyze_text(row["Текст"], keywords_dict): counts[c] += 1
        row_data = {"Ресторан": rest, **counts}
        row_data["Всего:"] = sum(counts.values())
        results.append(row_data)
    return pd.DataFrame(results)

# ==================== ИНТЕРФЕЙС ====================
st.title("📆 Отчет «КР неделя»")
st.markdown("Загрузите выгрузки из 3 источников для формирования еженедельного отчета.")

col1, col2, col3 = st.columns(3)
with col1: file1 = st.file_uploader("1. Сайт/приложение", type=["xlsx", "xls"])
with col2: file2 = st.file_uploader("2. Агрегаторы", type=["xlsx", "xls"])
with col3: file3 = st.file_uploader("3. Геосервисы", type=["xlsx", "xls"])

if st.button("🚀 Сформировать отчет", type="primary"):
    if not (file1 and file2 and file3):
        st.error("Пожалуйста, загрузите все 3 файла!")
    else:
        with st.spinner("Обработка данных..."):
            try:
                df1 = pd.read_excel(file1)
                df1["Ресторан"] = df1["Ресторан"].apply(map_restaurant_file1)
                df1["Текст"] = df1["Комментарий"].fillna("")
                df1["Рейтинг"] = pd.to_numeric(df1["Рейтинг"], errors="coerce")
                df1 = df1[["Ресторан", "Рейтинг", "Текст"]].dropna(subset=["Ресторан", "Рейтинг"])

                df2 = pd.read_excel(file2)
                df2["Ресторан"] = df2["Адрес"].apply(map_restaurant_address)
                df2["Текст"] = df2["Отзыв"].fillna("")
                df2["Рейтинг"] = pd.to_numeric(df2["Оценка"], errors="coerce")
                df2 = df2[["Ресторан", "Рейтинг", "Текст"]].dropna(subset=["Ресторан", "Рейтинг"])

                df3 = pd.read_excel(file3)
                df3["Ресторан"] = df3.apply(lambda row: map_restaurant_address(row.get("Название филиала", "")) or map_restaurant_address(row.get("Адрес филиала", "")), axis=1)
                df3["Текст"] = df3["Текст отзыва"].fillna("")
                df3["Рейтинг"] = pd.to_numeric(df3["Оценка"], errors="coerce")
                df3 = df3[["Ресторан", "Рейтинг", "Текст"]].dropna(subset=["Ресторан", "Рейтинг"])

                df_all = pd.concat([df1, df2, df3], ignore_index=True)
                spb = [r for r in df_all["Ресторан"].unique() if "ТМН" not in r]
                tmn = [r for r in df_all["Ресторан"].unique() if "ТМН" in r]

                stats1, stats2, stats3, stats_all = calc_stats(df1), calc_stats(df2), calc_stats(df3), calc_stats(df_all)
                
                complaints_all = calc_summary_transposed(df_all, COMPLAINT_KEYWORDS)
                positives_all = calc_summary_transposed(df_all, POSITIVE_KEYWORDS)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    row_pos = 0
                    for name, df_stat in [("Сайт/приложение", stats1), ("Агрегаторы", stats2), ("Геосервисы", stats3), ("Общий итог", stats_all)]:
                        pd.DataFrame([[name] + [None]*7]).to_excel(writer, sheet_name="Оценки", index=False, header=False, startrow=row_pos)
                        row_pos += 2
                        df_spb = add_totals(df_stat[df_stat["Ресторан"].isin(spb)], "СПб")
                        df_tmn = add_totals(df_stat[df_stat["Ресторан"].isin(tmn)], "Тюмень")
                        df_combined = pd.concat([df_spb, pd.DataFrame([[None]*8]), df_tmn])
                        df_combined.to_excel(writer, sheet_name="Оценки", index=False, startrow=row_pos)
                        row_pos += len(df_combined) + 3

                    row_pos = 0
                    for name, df_comp in [("Сводная по жалобам (СПб)", complaints_all[complaints_all["Ресторан"].isin(spb)]), 
                                          ("Сводная по жалобам (Тюмень)", complaints_all[complaints_all["Ресторан"].isin(tmn)]),
                                          ("Сводная по положительным моментам (СПб)", positives_all[positives_all["Ресторан"].isin(spb)]),
                                          ("Сводная по положительным моментам (Тюмень)", positives_all[positives_all["Ресторан"].isin(tmn)])]:
                        pd.DataFrame([[name] + [None]*6]).to_excel(writer, sheet_name="Анализ отзывов", index=False, header=False, startrow=row_pos)
                        row_pos += 2
                        df_comp.to_excel(writer, sheet_name="Анализ отзывов", index=False, startrow=row_pos)
                        row_pos += len(df_comp) + 3

                output.seek(0)
                st.success("✅ Отчет успешно сформирован!")
                st.download_button("📥 Скачать Excel", output, "КР_неделя_отчет.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                st.subheader("Превью: Общий итог")
                st.dataframe(stats_all)
                
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
