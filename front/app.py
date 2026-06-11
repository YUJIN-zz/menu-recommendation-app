import os
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000/recommend")


st.set_page_config(
    page_title="오늘의 메뉴 추천",
    page_icon="🥗",
    layout="wide",
)


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f4fbf6 0%, #eef8f0 45%, #f8fff9 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1120px;
    }

    .main-hero {
        background: linear-gradient(135deg, #14532d 0%, #1f7a3f 50%, #7dbb73 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 28px;
        color: white;
        box-shadow: 0 18px 42px rgba(20, 83, 45, 0.22);
        margin-bottom: 1.4rem;
    }

    .hero-label {
        display: inline-block;
        padding: 0.42rem 0.78rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.18);
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 0.85rem;
    }

    .hero-title {
        font-size: 2.55rem;
        font-weight: 900;
        letter-spacing: -0.045em;
        margin-bottom: 0.45rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        line-height: 1.65;
        opacity: 0.94;
        max-width: 760px;
    }

    .panel {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(220, 238, 224, 0.95);
        border-radius: 26px;
        padding: 1.45rem;
        box-shadow: 0 12px 34px rgba(30, 85, 45, 0.08);
        height: 100%;
        margin-bottom: 0.6rem;
    }

    .panel-title {
        font-size: 1.22rem;
        font-weight: 900;
        color: #14532d;
        margin-bottom: 0.3rem;
    }

    .panel-desc {
        font-size: 0.92rem;
        color: #647067;
        margin-bottom: 0.3rem;
        line-height: 1.55;
    }

    .result-hero {
        background: white;
        border: 1px solid #dceee0;
        border-left: 8px solid #1f7a3f;
        border-radius: 26px;
        padding: 1.75rem 1.9rem;
        box-shadow: 0 16px 36px rgba(30, 85, 45, 0.1);
        margin-top: 1.3rem;
        margin-bottom: 1.1rem;
    }

    .result-badge {
        display: inline-block;
        background: #e7f6ea;
        color: #14532d;
        border-radius: 999px;
        padding: 0.42rem 0.78rem;
        font-size: 0.86rem;
        font-weight: 850;
        margin-bottom: 0.7rem;
    }

    .result-title {
        font-size: 2rem;
        font-weight: 900;
        color: #123524;
        letter-spacing: -0.04em;
        margin-bottom: 0.45rem;
    }

    .result-summary {
        color: #5f6f64;
        font-size: 1rem;
        line-height: 1.65;
    }

    .score-card {
        background: linear-gradient(135deg, #14532d 0%, #2e8b57 100%);
        color: white;
        border-radius: 24px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 14px 32px rgba(20, 83, 45, 0.18);
        height: 100%;
    }

    .score-number {
        font-size: 2.35rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }

    .score-label {
        font-size: 0.92rem;
        opacity: 0.92;
    }

    .flow-card {
        background: #f2faf4;
        border: 1px solid #dceee0;
        border-radius: 24px;
        padding: 1.25rem;
        text-align: center;
        color: #14532d;
        font-weight: 900;
        font-size: 1.25rem;
        height: 100%;
    }

    .chip {
        display: inline-block;
        background: #ffffff;
        border: 1px solid #dbeadd;
        color: #2f4f3a;
        border-radius: 999px;
        padding: 0.45rem 0.78rem;
        margin: 0.18rem;
        font-size: 0.87rem;
        font-weight: 750;
    }

    .menu-card {
        background: white;
        border: 1px solid #dceee0;
        border-radius: 26px;
        padding: 1.45rem;
        box-shadow: 0 14px 34px rgba(30, 85, 45, 0.08);
        min-height: 330px;
    }

    .menu-emoji {
        font-size: 2.2rem;
        margin-bottom: 0.55rem;
    }

    .menu-title {
        color: #14532d;
        font-size: 1.08rem;
        font-weight: 850;
        margin-bottom: 0.35rem;
    }

    .menu-name {
        color: #123524;
        font-size: 1.4rem;
        font-weight: 950;
        margin-bottom: 0.8rem;
        line-height: 1.35;
    }

    .menu-box {
        background: #f4fbf6;
        border-radius: 18px;
        border: 1px solid #dceee0;
        padding: 0.9rem;
        color: #26382c;
        font-weight: 750;
        line-height: 1.55;
        margin-bottom: 0.9rem;
    }

    .reason-text {
        color: #637468;
        line-height: 1.65;
        font-size: 0.94rem;
    }

    .tip-card {
        background: #ffffff;
        border: 1px solid #dceee0;
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 10px 26px rgba(30, 85, 45, 0.07);
        height: 100%;
    }

    .tip-title {
        color: #14532d;
        font-size: 1.1rem;
        font-weight: 900;
        margin-bottom: 0.45rem;
    }

    .tip-main {
        color: #123524;
        font-weight: 850;
        font-size: 1.05rem;
        margin-bottom: 0.45rem;
    }

    .tip-desc {
        color: #637468;
        line-height: 1.55;
        font-size: 0.93rem;
    }

    div.stButton > button:first-child {
        border-radius: 18px;
        height: 3.2rem;
        font-weight: 900;
        font-size: 1.02rem;
        background: linear-gradient(135deg, #14532d 0%, #2e8b57 100%);
        border: none;
        box-shadow: 0 12px 26px rgba(20, 83, 45, 0.2);
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 30px rgba(20, 83, 45, 0.28);
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label {
        color: #123524;
        font-weight: 750;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="main-hero">
        <div class="hero-label">Streamlit + FastAPI + Docker + AWS EC2</div>
        <div class="hero-title">🥗 오늘의 메뉴 추천</div>
        <div class="hero-subtitle">
            식사 유형, 건강 목표, 허기짐 정도, 동행 상황을 바탕으로
            오늘 먹기 좋은 식사 메뉴를 추천하는 웹 애플리케이션입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


input_col1, input_col2 = st.columns(2, gap="large")

with input_col1:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">🍚 식사 조건</div>
            <div class="panel-desc">
                오늘 먹고 싶은 식사 유형과 건강 목표를 선택하세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    meal_type = st.selectbox(
        "선호하는 식사 유형",
        ["한식", "일식", "양식", "중식", "분식", "샐러드/건강식"]
    )

    health_goal = st.selectbox(
        "건강 목표",
        ["가볍게 먹기", "단백질 중심", "든든하게 먹기", "다이어트 중", "균형 잡힌 식사"]
    )

    hunger_level = st.radio(
        "현재 허기짐 정도",
        ["조금 출출함", "보통", "매우 배고픔"],
        horizontal=True
    )

with input_col2:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">✨ 상황 조건</div>
            <div class="panel-desc">
                함께 먹는 사람, 원하는 분위기, 식후 취향을 선택하세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    companion = st.selectbox(
        "누구와 함께하나요?",
        ["혼자", "친구", "연인", "가족"]
    )

    mood = st.selectbox(
        "원하는 분위기",
        ["조용한 곳", "가성비 좋은 곳", "사진 찍기 좋은 곳", "든든한 한 끼", "건강한 느낌", "편하게 오래 머물 수 있는 곳"]
    )

    dessert_type = st.selectbox(
        "식후 디저트 취향",
        ["커피", "베이커리", "저당 음료", "아이스크림", "과일/요거트"]
    )

    walk_time = st.selectbox(
        "식후 움직임 가능 시간",
        ["0분", "10분", "20분", "30분 이상"]
    )


st.markdown("")

recommend_button = st.button("🥗 오늘의 메뉴 추천받기", use_container_width=True)


if recommend_button:
    payload = {
        "meal_type": meal_type,
        "health_goal": health_goal,
        "dessert_type": dessert_type,
        "hunger_level": hunger_level,
        "companion": companion,
        "mood": mood,
        "walk_time": walk_time,
    }

    try:
        with st.spinner("FastAPI 서버에 추천 요청을 보내는 중입니다..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            st.markdown(
                f"""
                <div class="result-hero">
                    <div class="result-badge">{result['recommendation_badge']}</div>
                    <div class="result-title">{result['recommendation_title']}</div>
                    <div class="result-summary">{result['recommendation_summary']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            score_col, flow_col = st.columns([0.32, 0.68], gap="medium")

            with score_col:
                st.markdown(
                    f"""
                    <div class="score-card">
                        <div class="score-number">{result['recommendation_score']}점</div>
                        <div class="score-label">메뉴 적합도</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with flow_col:
                st.markdown(
                    """
                    <div class="flow-card">
                        🍚 메인 메뉴 &nbsp; | &nbsp; 🥗 대체 메뉴 &nbsp; | &nbsp; 🥪 가벼운 메뉴
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            summary = result["input_summary"]

            st.markdown("### 선택한 조건")
            st.markdown(
                f"""
                <div>
                    <span class="chip">🍚 {summary['meal_type']}</span>
                    <span class="chip">🎯 {summary['health_goal']}</span>
                    <span class="chip">🔥 {summary['hunger_level']}</span>
                    <span class="chip">👥 {summary['companion']}</span>
                    <span class="chip">✨ {summary['mood']}</span>
                    <span class="chip">☕ {summary['dessert_type']}</span>
                    <span class="chip">🌿 {summary['walk_time']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 추천 메뉴")

            main_menu = result["main_menu"]
            alternative_menu = result["alternative_menu"]
            light_menu = result["light_menu"]

            card1, card2, card3 = st.columns(3, gap="medium")

            with card1:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div class="menu-emoji">{main_menu['emoji']}</div>
                        <div class="menu-title">{main_menu['title']}</div>
                        <div class="menu-name">{main_menu['name']}</div>
                        <div class="menu-box">{main_menu['description']}</div>
                        <div class="reason-text">{main_menu['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with card2:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div class="menu-emoji">{alternative_menu['emoji']}</div>
                        <div class="menu-title">{alternative_menu['title']}</div>
                        <div class="menu-name">{alternative_menu['name']}</div>
                        <div class="menu-box">{alternative_menu['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with card3:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div class="menu-emoji">{light_menu['emoji']}</div>
                        <div class="menu-title">{light_menu['title']}</div>
                        <div class="menu-name">{light_menu['name']}</div>
                        <div class="menu-box">{light_menu['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### 식후 참고 추천")

            dessert_tip = result["dessert_tip"]
            after_meal_tip = result["after_meal_tip"]

            tip_col1, tip_col2 = st.columns(2, gap="medium")

            with tip_col1:
                st.markdown(
                    f"""
                    <div class="tip-card">
                        <div class="tip-title">☕ {dessert_tip['title']}</div>
                        <div class="tip-main">{dessert_tip['recommendation']}</div>
                        <div class="tip-desc">{dessert_tip['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with tip_col2:
                st.markdown(
                    f"""
                    <div class="tip-card">
                        <div class="tip-title">🌿 {after_meal_tip['title']}</div>
                        <div class="tip-main">{after_meal_tip['activity']}</div>
                        <div class="tip-desc">{after_meal_tip['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.success("추천 결과를 FastAPI에서 받아왔습니다.")
            st.info(result["message"])

            with st.expander("FastAPI JSON 응답 확인하기"):
                st.json(result)

        else:
            st.error(f"FastAPI 서버 오류가 발생했습니다. 상태 코드: {response.status_code}")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error("FastAPI 서버에 연결할 수 없습니다. Docker 컨테이너 또는 API 주소를 확인하세요.")

    except requests.exceptions.Timeout:
        st.error("FastAPI 서버 응답 시간이 초과되었습니다.")

    except Exception as e:
        st.error(f"예상하지 못한 오류가 발생했습니다: {e}")


st.markdown("---")
st.caption("본 서비스는 Streamlit 프론트엔드와 FastAPI 백엔드가 HTTP 통신으로 연결된 메뉴 추천 웹 애플리케이션입니다.")