# Skill: LuyiLife Streamlit App Builder

## 觸發情境
當使用者提出開發、修改或部署任何 Streamlit 互動測算 / 工具 Web App 時套用此規範。

## 開發與安全硬性規範

1. **隱私與安全隔離（零機密外洩）**
   - 專案初始化時，必須自動建立 `.gitignore`。
   - 強制排除所有多媒體與文稿格式：`*.png`, `*.jpg`, `*.jpeg`, `*.mp4`, `*.mov`, `*.mp3`, `*.docx`, `*.xlsx`, `*.pdf`, `*.env` 以及產圖產文產影暫存目錄。
   - 僅將核心程式碼（如 `app.py`、模組檔）與 `requirements.txt` 納入 Git 追蹤。

2. **前端介面乾淨化（隱藏後台入口）**
   - 在 `app.py` 中自動注入標準 CSS，隱藏 Streamlit 預設選單、頁尾與原始碼連結：
     ```python
     hide_streamlit_style = """
     <style>
     #MainMenu {visibility: hidden;}
     footer {visibility: hidden;}
     header {visibility: hidden;}
     [data-testid="stToolbar"] {visibility: hidden !important;}
     [data-testid="stDecoration"] {visibility: hidden !important;}
     [data-testid="stStatusWidget"] {visibility: hidden !important;}
     </style>
     """
     st.markdown(hide_streamlit_style, unsafe_allow_html=True)
     ```

3. **手機與 LINE 內嵌瀏覽器 100% 相容**
   - 所有外部導流連結（LINE 官方帳號、Portaly、預約諮詢等）一律採用原生 `st.link_button(label, url, use_container_width=True)`，嚴禁使用易失效的純 HTML `<a>` 標籤刻按鈕。
   - 官方 LINE 導流連結一律格式化為原生跳轉格式（如 `https://lin.ee/xxxxx` 或 `https://line.me/R/ti/p/@xxx`），確保手機環境能自動喚醒 LINE App。

4. **雲端部署一鍵就緒**
   - 自動生成包含所有相依套件的 `requirements.txt`。
   - 程式邏輯撰寫完成後，自動執行 Git 初始化、建立主分支（`main`）、排除無關檔案、完成 Commit，並提示/執行推送至指定遠端倉庫。
