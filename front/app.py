import os
import requests
import streamlit as st

try:
    from streamlit_geolocation import streamlit_geolocation
except Exception:
    streamlit_geolocation = None


API_URL = os.getenv("API_URL", "http://localhost:8000/recommend")


st.set_page_config(
    page_title="오늘 뭐 먹고 걸을까?",
    page_icon="🍽️",
    layout="wide",
)


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff8ed 0%, #f7fff4 45%, #eef7ff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    .hero-card {
        background: linear-gradient(135deg, #ff8a3d 0%, #ffb347 45%, #6abf69 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 28px;
        color: white;
        box-shadow: 0 18px 40px rgba(255, 138, 61, 0.28);
        margin-bottom: 1.4rem;
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 900;
        margin-bottom: 0.45rem;
        letter-spacing: -0.04em;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        opacity: 0.96;
        line-height: 1.65;
        max-width: 760px;
    }

    .mini-badge {
        display: inline-block;
        padding: 0.4rem 0.75rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.23);
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.85);
        border-radius: 24px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 12px 32px rgba(57, 72, 86, 0.08);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 850;
        color: #263238;
        margin-bottom: 0.25rem;
    }

    .section-desc {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 0.8rem;
    }

    .result-hero {
        background: linear-gradient(135deg, #263238 0%, #355c4b 60%, #ff8a3d 100%);
        color: white;
        border-radius: 28px;
        padding: 2rem 2.2rem;
        box-shadow: 0 18px 42px rgba(38, 50, 56, 0.22);
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
    }

    .result-title {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 0.5rem;
    }

    .result-subtitle {
        font-size: 1rem;
        opacity: 0.92;
        line-height: 1.65;
    }

    .score-box {
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 22px;
        padding: 1rem;
        text-align: center;
    }

    .score-number {
        font-size: 2.2rem;
        font-weight: 900;
    }

    .score-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    .flow-box {
        background: white;
        border-radius: 24px;
        padding: 1.2rem;
        box-shadow: 0 12px 28px rgba(57, 72, 86, 0.08);
        text-align: center;
        margin-bottom: 1.1rem;
    }

    .flow-text {
        font-size: 1.35rem;
        font-weight: 850;
        color: #263238;
    }

    .course-card {
        background: white;
        border-radius: 26px;
        padding: 1.35rem 1.35rem;
        box-shadow: 0 14px 34px rgba(57, 72, 86, 0.1);
        border: 1px solid rgba(226, 232, 240, 0.85);
        height: 100%;
    }

    .course-step {
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        background: #fff2df;
        color: #e56f21;
        font-weight: 850;
        font-size: 0.78rem;
        margin-bottom: 0.65rem;
    }

    .course-title {
        font-size: 1.35rem;
        font-weight: 900;
        color: #263238;
        margin-bottom: 0.4rem;
    }

    .keyword-box {
        background: #f8fafc;
        padding: 0.85rem;
        border-radius: 16px;
        color: #334155;
        font-weight: 800;
        margin: 0.75rem 0;
    }

    .reason-text {
        color: #64748b;
        line-height: 1.65;
        font-size: 0.94rem;
        min-height: 6rem;
    }

    .summary-chip {
        display: inline-block;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 999px;
        padding: 0.45rem 0.75rem;
        margin: 0.2rem;
        color: #334155;
        font-size: 0.88rem;
        font-weight: 700;
    }

    div.stButton > button:first-child {
        border-radius: 18px;
        height: 3.2rem;
        font-weight: 850;
        font-size: 1.02rem;
        background: linear-gradient(135deg, #ff8a3d 0%, #ffb347 100%);
        border: none;
        box-shadow: 0 10px 24px rgba(255, 138, 61, 0.25);
    }

    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(255, 138, 61, 0.34);
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.78);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 10px 26px rgba(57, 72, 86, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero-card">
        <div class="mini-badge">Streamlit + FastAPI + Docker + AWS EC2</div>
        <div class="hero-title">🍽️ 오늘 뭐 먹고 걸을까?</div>
        <div class="hero-subtitle">
            현재 위치와 식사 취향을 바탕으로 식당, 카페, 산책 코스를 하나의 흐름으로 추천하는
            위치 기반 식후 코스 추천 웹 애플리케이션입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


left_col, right_col = st.columns([0.92, 1.08], gap="large")

with left_col:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">📍 Step 1. 오늘의 출발지</div>
            <div class="section-desc">현재 위치를 허용하거나 직접 지역명을 입력하세요.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    location_data = None
    latitude = None
    longitude = None

    with st.expander("현재 위치 허용하기", expanded=False):
        st.write("브라우저에서 위치 권한을 허용하면 현재 위치 좌표를 추천 요청에 함께 보낼 수 있습니다.")

        if streamlit_geolocation is not None:
            location_data = streamlit_geolocation()

            if location_data:
                latitude = location_data.get("latitude")
                longitude = location_data.get("longitude")

                if latitude and longitude:
                    st.success(f"현재 위치 확인 완료: 위도 {latitude}, 경도 {longitude}")
                else:
                    st.warning("위치 권한이 허용되지 않았거나 위치 정보를 가져오지 못했습니다.")
            else:
                st.info("위치 기능이 작동하지 않으면 아래에 직접 지역명을 입력하세요.")
        else:
            st.warning("현재 위치 컴포넌트를 불러오지 못했습니다. 직접 지역명을 입력하세요.")

    location_text = st.text_input(
        "지역명",
        value="광운대",
        placeholder="예: 광운대, 수유역, 강남역, 성수동"
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🍚 Step 2. 오늘의 식사 취향</div>
            <div class="section-desc">식사 유형, 건강 목표, 허기짐 정도를 선택하세요.</div>
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

with right_col:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">☕ Step 3. 식후 디저트 취향</div>
            <div class="section-desc">식사 후 어떤 디저트를 먹고 싶은지 선택하세요.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dessert_type = st.selectbox(
        "선호하는 디저트 유형",
        ["커피", "베이커리", "저당 음료", "아이스크림", "과일/요거트"]
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">👥 Step 4. 오늘의 식사 분위기</div>
            <div class="section-desc">동행 유형과 원하는 분위기를 선택하세요.</div>
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

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🚶 Step 5. 식후 산책 루틴</div>
            <div class="section-desc">식사 후 걸을 수 있는 시간을 선택하세요.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    walk_time = st.selectbox(
        "식사 후 산책 가능시간",
        ["0분", "10분", "20분", "30분 이상"]
    )


st.markdown("---")

recommend_button = st.button("✨ 오늘의 맞춤 코스 추천받기", use_container_width=True)


if recommend_button:
    payload = {
        "location_text": location_text,
        "latitude": latitude,
        "longitude": longitude,
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
                    <div class="mini-badge">{result['course_badge']}</div>
                    <div class="result-title">✨ {result['course_title']}</div>
                    <div class="result-subtitle">{result['course_summary']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            score_col, flow_col = st.columns([0.32, 0.68], gap="medium")

            with score_col:
                st.metric(
                    label="오늘의 코스 적합도",
                    value=f"{result['recommendation_score']}점"
                )

            with flow_col:
                st.markdown(
                    """
                    <div class="flow-box">
                        <div class="flow-text">🍚 식사 → ☕ 디저트 → 🚶 산책</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            summary = result["input_summary"]

            st.markdown("### 📌 입력 요약")
            st.markdown(
                f"""
                <div>
                    <span class="summary-chip">📍 {summary['location']}</span>
                    <span class="summary-chip">🍚 {summary['meal_type']}</span>
                    <span class="summary-chip">🎯 {summary['health_goal']}</span>
                    <span class="summary-chip">☕ {summary['dessert_type']}</span>
                    <span class="summary-chip">🔥 {summary['hunger_level']}</span>
                    <span class="summary-chip">👥 {summary['companion']}</span>
                    <span class="summary-chip">✨ {summary['mood']}</span>
                    <span class="summary-chip">🚶 {summary['walk_time']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 🧭 추천 코스")

            restaurant = result["restaurant"]
            cafe = result["cafe"]
            walk = result["walk"]

            card1, card2, card3 = st.columns(3, gap="medium")

            with card1:
                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-step">{restaurant['step']}</div>
                        <div class="course-title">{restaurant['emoji']} {restaurant['title']}</div>
                        <div class="keyword-box">{restaurant['search_keyword']}</div>
                        <div class="reason-text">{restaurant['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("네이버 지도에서 식당 보기", restaurant["map_url"], use_container_width=True)

            with card2:
                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-step">{cafe['step']}</div>
                        <div class="course-title">{cafe['emoji']} {cafe['title']}</div>
                        <div class="keyword-box">{cafe['search_keyword']}</div>
                        <div class="reason-text">{cafe['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("네이버 지도에서 카페 보기", cafe["map_url"], use_container_width=True)

            with card3:
                st.markdown(
                    f"""
                    <div class="course-card">
                        <div class="course-step">{walk['step']}</div>
                        <div class="course-title">{walk['emoji']} {walk['title']}</div>
                        <div class="keyword-box">{walk['search_keyword']}</div>
                        <div class="reason-text">{walk['reason']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.link_button("네이버 지도에서 산책 코스 보기", walk["map_url"], use_container_width=True)

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
st.caption("본 서비스는 Streamlit 프론트엔드와 FastAPI 백엔드가 HTTP 통신으로 연결된 추천 웹 애플리케이션입니다.")