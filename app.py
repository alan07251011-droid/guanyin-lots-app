import streamlit as st
import random
import os
from guanyin_lots import get_lot_data

# 頁面基本配置
st.set_page_config(
    page_title="觀音靈籤 身心靈調頻 ｜ 老臣聊心室",
    page_icon="🌸",
    layout="centered"
)

# 8 大提問面向定義與範例
CATEGORIES_INFO = {
    "本運": {
        "icon": "🧭",
        "example": "想了解我近期整體的氣運走勢、心境卡點與轉折契機。"
    },
    "事業": {
        "icon": "💼",
        "example": "我現任職...，正面臨（轉職/升遷/創業），求指引時機與盲點。"
    },
    "財運": {
        "icon": "💰",
        "example": "想了解近期投資／正財／合約買賣的走向與需注意的破口。"
    },
    "姻緣": {
        "icon": "❤️",
        "example": "我與（對象名/單身），想了解近期關係核心功課與正緣走向。"
    },
    "家運": {
        "icon": "🏡",
        "example": "想了解家中成員關係／買房搬遷／整體家庭氣場是否有需調和之處。"
    },
    "健康": {
        "icon": "🌿",
        "example": "近期身心容易疲憊，想了解身體調養與情緒平衡的方向。"
    },
    "學業": {
        "icon": "📚",
        "example": "我正準備（考試/進修），想了解考運起伏與備考心態指引。"
    },
    "求子": {
        "icon": "👶",
        "example": "我正處於（備孕/孕期），求指引安胎養身與順應自然的心法。"
    }
}

# 森林系與心靈調頻安全 CSS（嚴格隱藏預設選單，確保行動端無遮罩阻擋）
st.markdown("""
    <style>
    /* 全域背景與字體風格 */
    .stApp {
        background-color: #F8F5EE;
        color: #2C3E2E;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans TC", sans-serif;
    }

    /* 頂部 Header & 預設元件隱藏（安全與隱私規範） */
    header[data-testid="stHeader"], header {
        display: none !important;
        height: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
    }
    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], .viewerBadge_container__1QSob {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        height: 0 !important;
        width: 0 !important;
    }

    /* 慈悲觀音意象卡片 */
    .guanyin-banner {
        background: linear-gradient(135deg, #2D4F38 0%, #3D6A4E 60%, #5B886B 100%);
        color: #FFFFFF;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(45, 79, 56, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .guanyin-title {
        font-size: 1.45rem;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        color: #F7F4EE;
    }
    .guanyin-subtitle {
        font-size: 0.95rem;
        color: #D2E4D8;
        line-height: 1.6;
    }

    /* 引言卡片 */
    .quote-card {
        background-color: #FFFFFF;
        border-left: 5px solid #C49A45;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        line-height: 1.7;
        font-size: 0.95rem;
        color: #3B4B3D;
    }

    /* 步驟 Wizard 卡片 */
    .step-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
        border: 1px solid #E6ECE8;
    }
    .step-header {
        display: flex;
        align-items: center;
        font-weight: bold;
        color: #2D4F38;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
    }
    .step-badge {
        background-color: #2D4F38;
        color: #FFFFFF;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        margin-right: 8px;
    }

    /* 能量狀態徽章 */
    .energy-badge {
        display: inline-block;
        background-color: #EBF3ED;
        color: #2D4F38;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 1.02rem;
        font-weight: bold;
        border: 1px solid #C2DCC8;
        margin-bottom: 0.5rem;
    }

    /* 籤詩毛筆風格展示盒 */
    .poem-box {
        background-color: #FAF7F0;
        border: 2px dashed #C49A45;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin: 1.2rem 0;
    }
    .poem-line {
        font-size: 1.25rem;
        font-weight: bold;
        letter-spacing: 3px;
        color: #2D4F38;
        margin: 8px 0;
    }

    /* 擲筊視覺展示 */
    .bwa-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 1.2rem 0;
    }
    .bwa-cup {
        width: 84px;
        height: 50px;
        border-radius: 42px 42px 12px 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .bwa-front {
        background: linear-gradient(145deg, #B23A22, #8E2510);
        color: #FFF;
    }
    .bwa-back {
        background: linear-gradient(145deg, #E6C280, #D4A757);
        color: #5A3906;
    }

    /* 主請示面向置頂高亮卡 */
    .focused-category-card {
        background: linear-gradient(135deg, #EBF3ED 0%, #DCECE0 100%);
        border: 2px solid #2D4F38;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(45, 79, 56, 0.08);
    }

    /* 溫暖支持卡片 */
    .support-card {
        background-color: #EFF5F1;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px dashed #2D4F38;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Streamlit 原生按鈕樣式美化與全寬優化 */
    .stButton>button {
        background-color: #2D4F38;
        color: #FFFFFF !important;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        width: 100%;
        border: none;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        cursor: pointer !important;
        pointer-events: auto !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover, .stButton>button:active {
        background-color: #1E3525 !important;
        color: #E8E3D9 !important;
    }

    .stLinkButton {
        width: 100% !important;
    }
    .stLinkButton > a {
        background-color: #2D4F38 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: 1px solid #2D4F38 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        transition: all 0.2s ease !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 0.65rem 1rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        text-decoration: none !important;
    }
    .stLinkButton > a:hover, .stLinkButton > a:active {
        background-color: #1E3525 !important;
        color: #E8E3D9 !important;
        border-color: #1E3525 !important;
    }

    /* 確保所有互動元素能正常點擊 */
    a, button, input, select, textarea {
        pointer-events: auto !important;
        cursor: pointer !important;
    }

    /* 隱藏右上角選單、GitHub 標記與頂部工具列 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# 官方 LINE 原生 Scheme 網址
LINE_OFFICIAL_URL = "https://line.me/R/ti/p/@mir4855b"

# 初始化 Session State
if "chant_count" not in st.session_state:
    st.session_state.chant_count = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "本運"
if "drawn_lot" not in st.session_state:
    st.session_state.drawn_lot = None
if "divine_result" not in st.session_state:
    st.session_state.divine_result = None
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

# --- 一、頂部品牌識別與慈悲視覺 ---
st.markdown("""
<div style="background-color: #2D5A3F; border-radius: 16px; padding: 24px 20px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 12px;">
        <svg width="52" height="52" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));">
            <circle cx="50" cy="50" r="46" fill="#1C3826" opacity="0.6"/>
            <g opacity="0.9">
                <path d="M50 50 C35 25 35 15 50 10 C65 15 65 25 50 50Z" fill="#F8BBD0" transform="rotate(45 50 50)"/>
                <path d="M50 50 C35 25 35 15 50 10 C65 15 65 25 50 50Z" fill="#F8BBD0" transform="rotate(135 50 50)"/>
                <path d="M50 50 C35 25 35 15 50 10 C65 15 65 25 50 50Z" fill="#F8BBD0" transform="rotate(225 50 50)"/>
                <path d="M50 50 C35 25 35 15 50 10 C65 15 65 25 50 50Z" fill="#F8BBD0" transform="rotate(315 50 50)"/>
            </g>
            <path d="M50 50 C32 28 32 14 50 8 C68 14 68 28 50 50Z" fill="#F06292"/>
            <path d="M50 50 C32 28 32 14 50 8 C68 14 68 28 50 50Z" fill="#F06292" transform="rotate(90 50 50)"/>
            <path d="M50 50 C32 28 32 14 50 8 C68 14 68 28 50 50Z" fill="#F06292" transform="rotate(180 50 50)"/>
            <path d="M50 50 C32 28 32 14 50 8 C68 14 68 28 50 50Z" fill="#F06292" transform="rotate(270 50 50)"/>
            <circle cx="50" cy="50" r="16" fill="#E91E63" opacity="0.85"/>
            <circle cx="50" cy="50" r="8" fill="#FDD835"/>
            <circle cx="50" cy="50" r="4" fill="#FFF59D"/>
        </svg>
    </div>
    <h1 style="font-size: 1.65rem; font-weight: bold; letter-spacing: 1.5px; color: #F5DF9E; margin: 0 0 0.5rem 0; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">
        觀音靈籤 身心靈調頻
    </h1>
    <p style="font-size: 0.95rem; color: #E8F5ED; letter-spacing: 0.8px; font-weight: 300; margin: 0 0 0.8rem 0; opacity: 0.95; line-height: 1.6;">
        以慈悲智慧照見本心 ╳ 以靜心書寫梳理思緒 ╳ 以自然綠植調和頻率
    </p>
    <div style="width: 100px; height: 1px; background: rgba(210, 235, 218, 0.35); margin: 0.7rem auto;"></div>
    <p style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.6); letter-spacing: 1.2px; font-family: monospace, sans-serif; margin: 0; user-select: none;">
        綠藝國際學苑 ╳ 老臣聊心室 LUYILIFE ｜ 聽你的心，陪你調頻 ｜ 設計者：陳信忠 (老臣/Alan)
    </p>
</div>
""", unsafe_allow_html=True)

# 老臣心靈引言卡片
st.markdown("""
<div class="quote-card">
    <b>老臣聊心室 心靈引言：</b><br>
    『籤詩與吉凶，只是映照當下心境與盲點的「明鏡」，而非限制宿命的「框架」。真正的開運，在於透過靜心書寫梳理思緒、藉由綠植能量調和身心，由內而外活出從容自在。』
</div>
""", unsafe_allow_html=True)

# --- 二、求籤互動流程（第一階段：求籤五步驟精靈） ---
if not st.session_state.show_explanation:
    st.markdown("### 📥 第一階段：沉浸式求籤五步驟")
    
    # 步驟一：洗手靜心
    st.markdown("""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟一</span>
            <span>洗手靜心（安頓身心）</span>
        </div>
        <p style="margin: 0; color: #4A5B4C; line-height: 1.6; font-size: 0.93rem;">
            抽籤前請先洗手，找一個安靜、不被打擾的舒適空間。<br>
            輕輕閉上雙眼，端正坐姿，做三次深長的腹式呼吸，讓紛擾雜亂的思緒沉澱下來。
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 步驟二：唸誦聖號
    with st.container():
        st.markdown("""
        <div class="step-card">
            <div class="step-header">
                <span class="step-badge">步驟二</span>
                <span>唸誦聖號（建立連結）</span>
            </div>
            <p style="color: #4A5B4C; line-height: 1.6; font-size: 0.93rem; margin-bottom: 10px;">
                輕聲唸誦『<b>南無大慈大悲救苦救難觀世音菩薩</b>』或『<b>南無觀世音菩薩</b>』。<br>
                最少三遍；若心境浮躁可增至七或十遍，直到呼吸平穩、內心平靜。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            if st.button(f"🪷 唸誦觀音聖號（目前已唸：{st.session_state.chant_count} 遍）"):
                st.session_state.chant_count += 1
                st.rerun()
        with col_c2:
            if st.session_state.chant_count >= 3:
                st.success(f"✨ 已虔誠唸誦 {st.session_state.chant_count} 遍，心念已安頓，可進行下一步。")
            else:
                st.info(f"🌿 請至少點擊唸誦滿 3 遍（尚差 {3 - st.session_state.chant_count} 遍）。")

    # 步驟三：稟報資訊與聚焦請示（升級 8 大面向 Tag 與動態範例）
    with st.container():
        st.markdown("""
        <div class="step-card">
            <div class="step-header">
                <span class="step-badge">步驟三</span>
                <span>稟報資訊與聚焦請示（8 大面向引導）</span>
            </div>
            <p style="color: #4A5B4C; line-height: 1.6; font-size: 0.93rem; margin-bottom: 12px;">
                在心中默念：『弟子/信女（姓名），生於農曆/國曆〇年〇月〇日〇時，現居地址為〇〇〇。』<br>
                <b>請先點選下方【8 大請示面向】，每一支籤聚焦請示一件具體事項：</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 8 大面向按鈕選擇區 (4x2 網格排版)
        cat_keys = list(CATEGORIES_INFO.keys())
        cat_cols1 = st.columns(4)
        for i in range(4):
            cat = cat_keys[i]
            info = CATEGORIES_INFO[cat]
            is_active = (st.session_state.selected_category == cat)
            btn_label = f"✨ {info['icon']} 【{cat}】" if is_active else f"{info['icon']} 【{cat}】"
            if cat_cols1[i].button(btn_label, key=f"cat_btn_{cat}"):
                st.session_state.selected_category = cat
                st.rerun()

        cat_cols2 = st.columns(4)
        for i in range(4, 8):
            cat = cat_keys[i]
            info = CATEGORIES_INFO[cat]
            is_active = (st.session_state.selected_category == cat)
            btn_label = f"✨ {info['icon']} 【{cat}】" if is_active else f"{info['icon']} 【{cat}】"
            if cat_cols2[i-4].button(btn_label, key=f"cat_btn_{cat}"):
                st.session_state.selected_category = cat
                st.rerun()

        active_cat = st.session_state.selected_category
        active_info = CATEGORIES_INFO[active_cat]

        # 面向範例與一鍵套用卡片
        with st.container(border=True):
            st.markdown(f"**🎯 當前選擇面向：{active_info['icon']} 【{active_cat}】**")
            st.markdown(f"💡 **建議請示範例：** *「{active_info['example']}」*")
            if st.button(f"📋 一鍵套用【{active_cat}】範例文字", key="apply_example_btn"):
                st.session_state.user_question = active_info["example"]
                st.rerun()

        # 請示原則指引折疊
        with st.expander("💡 點此查看【良好請示原則】與【應避免的問法】"):
            st.markdown("""
            * **✅ 良好範例：**
              - 「今年底前若轉職到新產業，發展是否合適？」
              - 「目前這段交往關係，半年內是否有步入婚姻的契機？」
              - 「下半年籌備的新品牌計畫，整體運勢與注意事項為何？」
            * **⚠️ 應避免的問法：**
              - 「我什麼時候會發財？」（缺乏主動性與具體時間範疇）
              - 「我該選 A 公司還是 B 公司？」（二選一請分兩次分別請示，或改問「去 A 公司的發展」）
            """)

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.session_state.user_name = st.text_input("信士 / 信女 姓名", value=st.session_state.user_name, placeholder="例如：陳信忠 或 小晴")
            birth_info = st.text_input("出生年月日（國曆/農曆皆可）", placeholder="例如：國曆 1988年5月10日 巳時")
        with col_u2:
            address_info = st.text_input("現居地址（縣市/行政區即可）", placeholder="例如：台中市西屯區")
            st.session_state.user_question = st.text_area("具體請示事項（可直接手動輸入或一鍵套用）", value=st.session_state.user_question, placeholder="例如：想了解我近期整體的氣運走勢、心境卡點與轉折契機。", height=68)

    # 步驟四：點選抽籤
    with st.container():
        st.markdown("""
        <div class="step-card">
            <div class="step-header">
                <span class="step-badge">步驟四</span>
                <span>請示抽籤（請示賜籤）</span>
            </div>
            <p style="color: #4A5B4C; line-height: 1.6; font-size: 0.93rem;">
                心中默念：『<b>請大慈大悲觀世音菩薩賜一支靈籤指引迷津。</b>』
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎋 虔心請示・抽取靈籤"):
            if not st.session_state.user_name or not st.session_state.user_question:
                st.warning("⚠️ 請先於步驟三填寫您的【姓名】與【具體請示事項】，再行抽籤。")
            elif st.session_state.chant_count < 3:
                st.warning("⚠️ 請先於步驟二點擊唸誦觀音聖號滿 3 遍，安頓心神。")
            else:
                # 預設支援抽籤（支援 1~100 籤，測試時包含 1, 7 等）
                st.session_state.drawn_lot = random.choice([1, 7, 2, 100]) if os.getenv("TEST_MOCK_MODE") else random.randint(1, 100)
                st.session_state.divine_result = None
                st.rerun()

        if st.session_state.drawn_lot is not None:
            st.info(f"🎋 觀音菩薩初步賜予：【第 {st.session_state.drawn_lot} 籤】。請進行【步驟五：擲筊確認】天意。")

    # 步驟五：擲筊確認
    if st.session_state.drawn_lot is not None:
        with st.container():
            st.markdown(f"""
            <div class="step-card">
                <div class="step-header">
                    <span class="step-badge">步驟五</span>
                    <span>擲筊確認（確認天意）</span>
                </div>
                <p style="color: #4A5B4C; line-height: 1.6; font-size: 0.93rem;">
                    請在心中默念：『<b>弟子/信女求得第 {st.session_state.drawn_lot} 籤，若是觀音菩薩賜予之聖籤，請賜一個聖筊。</b>』
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🪵 線上擲筊確認天意"):
                outcome = random.choices(["sheng", "xiao", "yin"], weights=[60, 20, 20], k=1)[0]
                st.session_state.divine_result = outcome
                st.rerun()

            if st.session_state.divine_result == "sheng":
                st.markdown("""
                <div class="bwa-container">
                    <div class="bwa-cup bwa-front">正 (凸)</div>
                    <div class="bwa-cup bwa-back">反 (平)</div>
                </div>
                """, unsafe_allow_html=True)
                st.success("🌟【聖筊（一正一反）】！觀音菩薩已確認此籤正是為您當下心境量身開示之明鏡。")
                if st.button("📖 立即解鎖【解籤四步驟與專屬調頻處方】"):
                    st.session_state.show_explanation = True
                    st.rerun()

            elif st.session_state.divine_result == "xiao":
                st.markdown("""
                <div class="bwa-container">
                    <div class="bwa-cup bwa-back">反 (平)</div>
                    <div class="bwa-cup bwa-back">反 (平)</div>
                </div>
                """, unsafe_allow_html=True)
                st.warning("🌿【笑筊（兩平朝上）】：菩薩微笑不語，可能請示事項不夠具體、時機未到，或您心中已有答案。請重新梳理思緒後再次請示。")
                if st.button("🔄 重新抽籤請示"):
                    st.session_state.drawn_lot = None
                    st.session_state.divine_result = None
                    st.rerun()

            elif st.session_state.divine_result == "yin":
                st.markdown("""
                <div class="bwa-container">
                    <div class="bwa-cup bwa-front">正 (凸)</div>
                    <div class="bwa-cup bwa-front">正 (凸)</div>
                </div>
                """, unsafe_allow_html=True)
                st.error("🍃【陰筊（兩凸朝上）】：非此籤詩。菩薩提醒暫勿躁進，請深呼吸三次、重新收攝心神後再次請示。")
                if st.button("🔄 重新抽籤請示"):
                    st.session_state.drawn_lot = None
                    st.session_state.divine_result = None
                    st.rerun()

    # 求籤核心祕訣展示區
    st.markdown("""
    <div style="background-color:#F5EFE6; border-radius:10px; padding:12px 16px; font-size:0.88rem; color:#5D4A32; margin-top:1.5rem;">
        <b>💡 老臣求籤核心祕訣：</b><br>
        在求籤過程中，「專注與清晰」遠比念誦次數更關鍵。字句念得清楚、速度放慢，感覺內心不再雜亂時，便是最適合稟報與接收指引的時機。
    </div>
    """, unsafe_allow_html=True)

# --- 三、解籤展示（第二階段：解籤四步驟與專屬調頻處方） ---
else:
    lot = get_lot_data(st.session_state.drawn_lot)
    
    st.markdown("### 📖 第二階段：觀音靈籤解讀 ╳ 老臣身心靈調頻處方")
    st.markdown(f"**親愛的 {st.session_state.user_name if st.session_state.user_name else '朋友'}**，針對您請示的【{st.session_state.selected_category}】事項：*「{st.session_state.user_question}」*，觀音菩薩賜予指引如下：")
    
    # 籤號與雙典故大標
    lot_id = lot.get("id", st.session_state.drawn_lot)
    lot_number = lot.get("number", f"第 {lot_id} 籤")
    lot_level = lot.get("level", "吉籤")
    lot_title = lot.get("title", f"第 {lot_id} 籤典故")
    
    st.markdown(f"""
    <div class="step-card" style="text-align:center; border-top: 5px solid #2D4F38;">
        <span style="background-color:#E2ECE5; color:#2D4F38; padding:4px 14px; border-radius:16px; font-weight:bold; font-size:0.9rem; margin-right:6px;">
            觀音靈籤 {lot_number}（{lot_level}）
        </span>
        <h2 style="color:#2D4F38; margin: 10px 0 5px 0;">典故：{lot_title}</h2>
    </div>
    """, unsafe_allow_html=True)

    # 步驟一：當下能量狀態
    energy_status = lot.get("energy_status") or lot.get("energy_state") or "順應自然・修持本心：回歸心靈澄澈，在日常行持中蓄積豐碩福報。"
    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟一</span>
            <span>當下能量狀態（能量流轉與定調）</span>
        </div>
        <div style="text-align:center; padding: 0.5rem 0;">
            <div class="energy-badge">{energy_status}</div>
            <p style="color:#7A8B7C; font-size:0.85rem; margin:8px 0 0 0; font-style:italic;">
                🌿 溫馨提醒：吉凶無絕對，一切皆是當下心念與能量的流轉。
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 步驟二：籤詩故事與詩句解讀
    poem_lines = lot.get("poem", ["一片明心照大千", "吉凶禍福在心田", "靜心自省無罣礙", "自然福報慶豐年"])
    poem_lines_html = "".join([f'<div class="poem-line">{line}</div>' for line in poem_lines])
    oracle_exp = lot.get("oracle_explanation") or "吉星高照。福祿自來。守正行善。百福駢臻。"
    poem_meaning = lot.get("poem_meaning") or "此卦順應天時之象。凡事正道而行皆吉也。"
    
    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟二</span>
            <span>籤詩故事與詩句解讀（核心靈魂）</span>
        </div>
        <div class="poem-box">
            {poem_lines_html}
        </div>
        <div style="background-color:#F7F4EE; border-radius:10px; padding:12px 14px; margin-top:10px;">
            <p style="color:#2D4F38; font-weight:bold; margin:0 0 6px 0;">📜 【聖意/斷曰】：</p>
            <p style="color:#4A5B4C; font-size:0.92rem; line-height:1.6; margin:0 0 10px 0;">
                {oracle_exp}
            </p>
            <p style="color:#2D4F38; font-weight:bold; margin:0 0 6px 0;">💡 【白話詩意指引】：</p>
            <p style="color:#4A5B4C; font-size:0.92rem; line-height:1.6; margin:0;">
                {poem_meaning}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 步驟三：老臣聊心・八大生活指引（支援主請示置頂高亮 + 8大面向Tab切換）
    meanings = lot.get("meanings", {})
    focused_cat = st.session_state.selected_category
    focused_meaning = meanings.get(focused_cat, "順應時節因緣，保持自性清明。")
    focused_icon = CATEGORIES_INFO.get(focused_cat, {}).get("icon", "🎯")

    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟三</span>
            <span>🧭 老臣聊心・八大生活指引</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. 優先高亮置頂主請示面向
    st.markdown(f"""
    <div class="focused-category-card">
        <div style="font-weight: bold; color: #2D4F38; font-size: 1.05rem; margin-bottom: 6px;">
            🎯 您當前聚焦請示的【{focused_icon} {focused_cat}】專屬指引：
        </div>
        <div style="color: #2C3E2E; font-size: 0.96rem; line-height: 1.7;">
            {focused_meaning}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 八大面向 Tab 切換查看
    all_cats = list(CATEGORIES_INFO.keys())
    tab_labels = [f"{CATEGORIES_INFO[c]['icon']} {c}" for c in all_cats]
    tabs = st.tabs(tab_labels)

    for idx, cat_name in enumerate(all_cats):
        with tabs[idx]:
            cat_text = meanings.get(cat_name, "順應時節因緣，保持自性清明。")
            st.markdown(f"""
            <div style="background-color:#FFFFFF; border-radius:10px; padding:14px; border-left:4px solid #2D4F38; margin-top:8px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-weight:bold; color:#2D4F38; margin-bottom:6px; font-size:0.95rem;">
                    {CATEGORIES_INFO[cat_name]['icon']} 【{cat_name}】生活指引：
                </div>
                <div style="color:#333333; font-size:0.92rem; line-height:1.65;">
                    {cat_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 步驟四：老臣專屬身心靈調頻實踐（原生組件渲染）
    st.markdown("### 🌿 步驟四：老臣專屬身心靈調頻實踐")
    
    practice = lot.get("practice", {})
    writing_prompt = practice.get("writing_prompt") or "寫下你目前最想開創或療癒的一件事，感受內在深處的平靜與力量。"
    plant_prescription = practice.get("plant_prescription", {})
    
    # 1. 靜心書寫引導卡片
    with st.container(border=True):
        st.markdown("#### ✍️ 【老臣靜心書寫引導】")
        st.markdown(f"**📝 覺察提問：** {writing_prompt}")
        st.caption("（邀請您拿出筆記本或在下方梳理，倒空雜訊，讓智慧自然浮現。）")
        
        # 互動筆記輸入框
        user_note = st.text_area("📝 此刻您的靜心筆記 / 心靈轉念紀錄（可自由寫下帶走）：", placeholder="寫下此時此刻浮現在腦海的感受、看見與決定...", height=80)
        if user_note:
            st.success("🌿 很好，看見便是療癒的開始。將這份覺察帶入今日的生活中。")

    # 2. 園藝治療能量處方卡片
    with st.container(border=True):
        st.markdown("#### 🌿 【國際園藝治療師的能量處方】")
        p_element = plant_prescription.get("element", "木行生發能量")
        p_name = plant_prescription.get("plant_name", "開運竹 / 馬拉巴栗（發財樹）")
        p_energy = plant_prescription.get("energy", "生機勃發、節節高升、穩固扎根")
        p_placement = plant_prescription.get("placement_guide", "放在平時最常專注工作的工作桌或書房視線前方。")
        
        st.markdown(f"**🪴 調頻五行與植栽：** **{p_name}**（{p_element}）")
        st.markdown(f"**🌱 綠植能量意涵：** {p_energy}")
        st.markdown(f"**🏡 綠植擺放指南：** {p_placement}")

    # 重新求籤按鈕
    if st.button("🔄 請示另一項具體事項（重新抽籤）"):
        st.session_state.drawn_lot = None
        st.session_state.divine_result = None
        st.session_state.show_explanation = False
        st.session_state.chant_count = 0
        st.rerun()

# --- 四、底部心靈共振與行動呼籲模組（CTA） ---
footer_html = (
    '<div style="background: rgba(46, 125, 50, 0.06); border: 1px solid rgba(46, 125, 50, 0.2); border-radius: 16px; padding: 24px 20px; margin-top: 35px; text-align: center;">'
    '<div style="font-size: 1.15rem; font-weight: 700; color: #1B4332; margin-bottom: 8px;">🌲 受過傷的地方，細心灌溉，依然能長出翠綠的風景</div>'
    '<div style="font-size: 0.9rem; color: #4A5568; margin-bottom: 16px; line-height: 1.5;">心靈指引只是起點，真正的智慧在於回到日常生活，溫柔地接住自己。</div>'
    '<div style="border-top: 1px solid rgba(46, 125, 50, 0.15); padding-top: 14px; margin-bottom: 18px;">'
    '<div style="font-weight: 700; color: #1B4332; font-size: 1.05rem; margin-bottom: 6px;">作者：老臣（陳信忠）</div>'
    '<div style="margin-bottom: 8px;">'
    '<span style="font-size: 0.75rem; background: #1B5E20; color: #FFFFFF; padding: 3px 10px; border-radius: 12px; margin: 0 3px; display: inline-block; white-space: nowrap;">心靈陪伴者</span>'
    '<span style="font-size: 0.75rem; background: #004D40; color: #FFFFFF; padding: 3px 10px; border-radius: 12px; margin: 0 3px; display: inline-block; white-space: nowrap;">國際園藝治療師</span>'
    '</div>'
    '<p style="font-size: 0.85rem; color: #2D3748; margin-top: 6px; margin-bottom: 0; line-height: 1.5;">科技企業設計工程主管轉身・綠藝國際學苑創辦人<br>以「觀音心法 × 靜心書寫 × 生命密碼 × 園藝療法」陪你找回靈魂的原廠設定。</p>'
    '</div>'
    '<a href="https://line.me/R/ti/p/@mir4855b" target="_blank" style="display: block; background: linear-gradient(135deg, #2E7D32, #1B5E20); color: #FFFFFF; text-decoration: none; padding: 14px 16px; border-radius: 10px; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15); line-height: 1.4;">💬 免費加入官方 LINE@ ｜ 領取深度指引・預約諮詢・新書作品・隨喜贊助研發</a>'
    '<div style="font-size: 0.75rem; color: #718096; margin-top: 16px;">綠藝國際學苑 ✕ 老臣聊心室 LUYILIFE © 2026 ｜ 聽你的心，陪你調頻 ｜設計者：陳信忠 (老臣/Alan)</div>'
    '</div>'
)

st.markdown(footer_html, unsafe_allow_html=True)
