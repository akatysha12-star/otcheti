"""Страница VOC: только интерфейс. Вся логика — в logic/voc.py."""

import streamlit as st

from logic.voc import (
    PDF_LIB_OK,
    build_summary,
    excel_file_name,
    generate_excel,
    make_preview,
    parse_files,
)

st.set_page_config(page_title="VOC | Отчёты", page_icon="🍕", layout="wide")

st.title("VOC: сводная таблица нарушений")
st.caption(
    "Загрузите PDF-файлы VOC. В свод попадут только пункты, "
    "по которым хотя бы в одном ресторане есть результат НЕТ."
)

if not PDF_LIB_OK:
    st.error(
        "Не установлен pdfplumber. "
        "Добавьте в requirements.txt строку: pdfplumber==0.11.4"
    )

files = st.file_uploader(
    "Загрузить файлы VOC PDF или TXT",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

if not files:
    st.info("Загрузите от 1 до 14 файлов.")
    st.stop()

if len(files) > 14:
    st.warning("Можно обработать не более 14 файлов. Будут обработаны первые 14.")
    files = files[:14]

st.markdown("---")

include_all = st.checkbox(
    "Добавить все стандартные рестораны "
    "(1, 2, 4, 5, 6, 7, 8, 13, 15, 16, 18, 20), "
    "даже если файл по ресторану не загружен",
    value=False,
)

if st.button("Обработать файлы", type="primary"):
    with st.spinner("Читаем файлы и извлекаем пункты..."):
        parsed, errors = parse_files(files)
    st.session_state["voc_parsed"] = parsed
    st.session_state["voc_errors"] = errors
    st.session_state["voc_file_names"] = [f.name for f in files]

if "voc_parsed" not in st.session_state:
    st.stop()

parsed = st.session_state.get("voc_parsed", [])
errors = st.session_state.get("voc_errors", [])
saved_names = st.session_state.get("voc_file_names", [])
current_names = [f.name for f in files]

if saved_names != current_names:
    st.info("Список файлов изменен. Нажмите «Обработать файлы» заново.")

if errors:
    with st.expander("Ошибки обработки файлов"):
        for err in errors:
            st.write(err)

if not parsed:
    st.error("Не удалось распознать ни одного файла.")
    st.stop()

blocks, rest_labels, rest_info, matrix, loaded_labels = build_summary(
    parsed=parsed,
    include_default=include_all,
    only_uploaded=not include_all,
)

st.markdown("---")

if not blocks:
    st.warning(
        "Нарушения с результатом НЕТ не найдены. "
        "Проверьте, что файлы являются текстовыми PDF-выгрузками VOC."
    )
    st.stop()

total_items = sum(len(items) for items in blocks.values())
total_no = sum(
    1
    for block, items in blocks.items()
    for norm_key in items.keys()
    for label in rest_labels
    if matrix.get((label, block, norm_key), 0) == 1
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Файлов обработано", len(parsed))
c2.metric("Ресторанов в столбцах", len(rest_labels))
c3.metric("Пунктов с нарушениями", total_items)
c4.metric("Всего отметок НЕТ", total_no)

excel_bytes = generate_excel(blocks, rest_labels, rest_info, matrix)

st.download_button(
    label="Скачать сводный Excel",
    data=excel_bytes,
    file_name=excel_file_name(),
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
)

with st.expander("Предпросмотр таблицы"):
    preview = make_preview(blocks, rest_labels, matrix, limit=500)
    st.dataframe(preview, use_container_width=True)
    if total_items > len(preview):
        st.caption(
            "В предпросмотре показаны первые 500 строк. "
            "В Excel выгружаются все строки."
        )
