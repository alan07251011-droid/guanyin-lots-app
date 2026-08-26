import streamlit as st
import random
import os
from guanyin_lots import get_lot_data

# 頁面基本配置
st.set_page_config(
    page_title="綠藝國際學苑 ╳ 老臣聊心室 ╳ 觀音靈籤調頻",
    page_icon="🪷",
    layout="centered"
)

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
        font-size: 1.05rem;
        font-weight: bold;
        border: 1px solid #C2DCC8;
        margin-bottom: 0.5rem;
    }

    /* 六大生活指引網格 */
    .judgment-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-top: 10px;
    }
    .judgment-item {
        background-color: #F4F8F5;
        border-radius: 10px;
        padding: 12px 14px;
        border-left: 4px solid #2D4F38;
    }
    .judgment-label {
        font-weight: bold;
        color: #2D4F38;
        font-size: 0.88rem;
        margin-bottom: 6px;
    }
    .judgment-val {
        font-size: 0.9rem;
        color: #333333;
        line-height: 1.5;
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
if "drawn_lot" not in st.session_state:
    st.session_state.drawn_lot = None
if "divine_result" not in st.session_state:
    st.session_state.divine_result = None
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

# --- 一、頂部品牌識別與慈悲視覺 ---
st.markdown("""
<div class="guanyin-banner">
    <div style="font-size: 2.3rem; margin-bottom: 0.3rem;">🪷</div>
    <div class="guanyin-title">綠藝國際學苑 ╳ 老臣聊心室</div>
    <div style="font-size: 1.25rem; font-weight: bold; color: #E5C378; margin-bottom: 0.5rem;">觀音靈籤身心靈調頻</div>
    <div class="guanyin-subtitle">以慈悲智慧照見本心 ╳ 以靜心書寫梳理思緒 ╳ 以自然綠植調和頻率</div>
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

    # 步驟三：稟報資訊與明確祈求
    with st.container():
        st.markdown("""
        <div class="step-card">
            <div class="step-header">
                <span class="step-badge">步驟三</span>
                <span>稟報資訊與明確祈求（傳遞訊息）</span>
            </div>
            <p style="color: #4A5B4C; line-height: 1.6; font-size: 0.93rem; margin-bottom: 10px;">
                在心中或輕聲默念：『弟子/信女（姓名），生於農曆/國曆〇年〇月〇日〇時，現居地址為〇〇〇。』<br>
                <b>每一支籤只能請示一件具體的事項，避免泛泛而問。</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 請示原則指引折疊
        with st.expander("💡 點此查看【良好請示範例】與【應避免的問法】"):
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
            st.session_state.user_question = st.text_area("具體請示事項（單一明確事項）", value=st.session_state.user_question, placeholder="例如：下半年規劃轉換至綠色文創產業，未來發展方向與調頻建議為何？", height=68)

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
                st.session_state.drawn_lot = random.randint(1, 100)
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
                outcome = random.choices(["sheng", "xiao", "yin"], weights=[55, 25, 20], k=1)[0]
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
    st.markdown(f"**親愛的 {st.session_state.user_name if st.session_state.user_name else '朋友'}**，針對您請示的：*「{st.session_state.user_question}」*，觀音菩薩賜予指引如下：")
    
    # 籤號與雙典故大標
    lot_num = lot.get("num", st.session_state.drawn_lot)
    lot_story = lot.get("story", "心誠則靈")
    st.markdown(f"""
    <div class="step-card" style="text-align:center; border-top: 5px solid #2D4F38;">
        <span style="background-color:#E2ECE5; color:#2D4F38; padding:4px 14px; border-radius:16px; font-weight:bold; font-size:0.9rem;">
            觀音靈籤 第 {lot_num} 籤
        </span>
        <h2 style="color:#2D4F38; margin: 10px 0 5px 0;">典故：{lot_story}</h2>
    </div>
    """, unsafe_allow_html=True)

    # 步驟一：當下能量狀態（淡化吉凶，著重指引）
    energy_state = lot.get("energy_state", "🌿 蓄勢待發・向下扎根")
    energy_desc = lot.get("energy_desc", "扎根期：當前宜厚積薄發，充實專業底蘊，耐心等待成熟之時。")
    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟一</span>
            <span>當下能量狀態（能量流轉與定調）</span>
        </div>
        <div style="text-align:center; padding: 0.5rem 0;">
            <div class="energy-badge">{energy_state}</div>
            <p style="color:#3B4B3D; font-size:0.95rem; margin-top:8px; line-height:1.6;">
                {energy_desc}
            </p>
            <p style="color:#7A8B7C; font-size:0.85rem; margin:0; font-style:italic;">
                🌿 溫馨提醒：吉凶無絕對，一切皆是當下心念與能量的流轉。
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 步驟二：籤詩故事與詩句解讀（核心靈魂）
    poem_lines = lot.get("poem", ["一片明心照大千", "吉凶禍福在心田", "靜心自省無罣礙", "自然福報慶豐年"])
    poem_lines_html = "".join([f'<div class="poem-line">{line}</div>' for line in poem_lines])
    context_guidance = lot.get("context_guidance", "本籤提醒我們，無論外在境遇如何變化，只要心存善念、專注當下，就能找到安頓自心的力量。")
    poem_meaning = lot.get("poem_meaning", "順應自然規律，看懂時局起伏。好運之時謙遜扎根，沉潛之時蓄積能量，則無往不利。")
    
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
            <p style="color:#2D4F38; font-weight:bold; margin:0 0 6px 0;">📜 【歷史典故主角處境與啟示】：</p>
            <p style="color:#4A5B4C; font-size:0.92rem; line-height:1.6; margin:0 0 10px 0;">
                {context_guidance}
            </p>
            <p style="color:#2D4F38; font-weight:bold; margin:0 0 6px 0;">💡 【白話詩意指引】：</p>
            <p style="color:#4A5B4C; font-size:0.92rem; line-height:1.6; margin:0;">
                {poem_meaning}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 步驟三：老臣聊心・六大面向生活指引（100% 深度客製典故剖析）
    judgment = lot.get("judgment", {})
    val_overall = judgment.get("整體時局") or judgment.get("整體運勢") or "順應時節因緣，保持自性清明。"
    val_career = judgment.get("事業職場") or judgment.get("事業功名") or "深耕專業核心，靜候良機展現。"
    val_love = judgment.get("感情關係") or judgment.get("感情婚姻") or "以真誠與同理相伴，細水長流。"
    val_wealth = judgment.get("財富投資") or judgment.get("求財投資") or "穩健理財配置，謹守風險底線。"
    val_health = judgment.get("身心修復") or judgment.get("健康調養") or "調和作息節奏，親近自然綠意。"
    val_people = judgment.get("貴人機緣") or judgment.get("出行尋人") or "廣結善緣，以誠相待自得助益。"

    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">
            <span class="step-badge">步驟三</span>
            <span>🧭 老臣聊心・六大面向生活指引</span>
        </div>
        <div class="judgment-grid">
            <div class="judgment-item">
                <div class="judgment-label">🧭 整體時局</div>
                <div class="judgment-val">{val_overall}</div>
            </div>
            <div class="judgment-item">
                <div class="judgment-label">💼 事業職場</div>
                <div class="judgment-val">{val_career}</div>
            </div>
            <div class="judgment-item">
                <div class="judgment-label">❤️ 感情關係</div>
                <div class="judgment-val">{val_love}</div>
            </div>
            <div class="judgment-item">
                <div class="judgment-label">💰 財富投資</div>
                <div class="judgment-val">{val_wealth}</div>
            </div>
            <div class="judgment-item">
                <div class="judgment-label">🌿 身心修復</div>
                <div class="judgment-val">{val_health}</div>
            </div>
            <div class="judgment-item">
                <div class="judgment-label">🤝 貴人機緣</div>
                <div class="judgment-val">{val_people}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 步驟四：老臣專屬身心靈調頻實踐（落地轉化 - 原生組件渲染）
    st.markdown("### 🌿 步驟四：老臣專屬身心靈調頻實踐")

    # 1. 靜心書寫引導卡片
    with st.container(border=True):
        st.markdown("#### ✍️ 【老臣靜心書寫引導】")
        writing_data = lot.get('writing_prompts') or lot.get('mindful_writing') or lot.get('writing_guide') or []
        if isinstance(writing_data, list):
            for idx, q in enumerate(writing_data, 1):
                st.markdown(f"**📝 提問 {idx}：** {q}")
        elif isinstance(writing_data, dict):
            for k, v in writing_data.items():
                st.markdown(f"**📝 {k}：** {v}")
        else:
            st.markdown(f"**📝 覺察提問：** {writing_data}")
        
        st.caption("（邀請您拿出筆記本或在下方梳理，倒空雜訊，讓智慧自然浮現。）")

    # 2. 園藝治療能量處方卡片
    with st.container(border=True):
        st.markdown("#### 🌿 【國際園藝治療師的能量處方】")
        plant_data = lot.get('plant_prescription') or lot.get('plant_energy') or {}
        
        if isinstance(plant_data, dict):
            plant_name = plant_data.get('plant') or plant_data.get('name') or '專屬開運綠植'
            element = plant_data.get('element') or plant_data.get('five_elements') or '木'
            insight = plant_data.get('wisdom') or plant_data.get('insight') or plant_data.get('message') or '順應自然節奏，靜心生長。'
            
            st.markdown(f"**🪴 建議調頻綠植：** **{plant_name}**（五行能量：{element}）")
            st.markdown(f"**🌱 大自然植物照顧啟示：** {insight}")
        else:
            st.markdown(f"**🪴 綠植能量指引：** {plant_data}")

    # 靜心書寫互動筆記區
    user_note = st.text_area("📝 此刻您的靜心筆記 / 心靈轉念紀錄（可自由寫下帶走）：", placeholder="寫下此時此刻浮現在腦海的感受、看見與決定...", height=80)
    if user_note:
        st.success("🌿 很好，看見便是療癒的開始。將這份覺察帶入今日的生活中。")

    # 重新求籤按鈕
    if st.button("🔄 請示另一項具體事項（重新抽籤）"):
        st.session_state.drawn_lot = None
        st.session_state.divine_result = None
        st.session_state.show_explanation = False
        st.session_state.chant_count = 0
        st.rerun()

# --- 四、底部品牌頁尾與心靈共鳴模組 ---
st.markdown("""
<div class="support-card">
    <h4 style="color:#2D4F38; margin-top:0;">🌱 一份來自心靈的共鳴與支持</h4>
    <p style="color:#444; font-size:0.95rem; line-height:1.7; margin-bottom:14px;">
        如果這份小小的心靈陪伴工具，曾為此刻的你帶來一點清晰與安頓，<br>
        歡迎前往<b>官方 LINE</b>留下你的感受與好評，讓老臣知道這份陪伴傳遞到了你心裡。<br><br>
        若你認同這份理念，也歡迎<b>隨緣贊助支持</b>，陪伴老臣持續灌溉、開發更多有益於大眾的心靈陪伴工具！
    </p>
</div>
""", unsafe_allow_html=True)

# 單一聚焦導流按鈕
st.link_button(
    label="🌿 前往官方 LINE 聊心、回饋與支持老臣",
    url=LINE_OFFICIAL_URL,
    use_container_width=True
)

st.markdown("---")
st.caption("綠藝國際學苑 ╳ 老臣聊心室 LUYILIFE © 2026 ｜ 聽你的心，陪你調頻 ｜ 設計者：陳信忠 (老臣/Alan)")
