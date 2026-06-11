import os
import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000/recommend")


st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍱",
    layout="centered",
)

st.title("🍱 오늘 뭐 먹지?")
st.caption("식사 상황과 건강 목표를 바탕으로 오늘 먹기 좋은 메뉴를 추천해주는 웹 애플리케이션입니다.")

st.divider()

st.subheader("1. 식사 상황 입력")

meal_time = st.selectbox(
    "식사 시간",
    ["아침", "점심", "저녁", "야식"]
)

food_type = st.selectbox(
    "선호하는 식사 유형",
    ["한식", "일식", "양식", "중식", "분식", "샐러드/건강식"]
)

health_goal = st.selectbox(
    "건강 목표",
    ["다이어트", "단백질 보충", "든든한 한 끼", "가볍게 먹기", "균형 잡힌 식사"]
)

hunger_level = st.radio(
    "현재 허기짐 정도",
    ["조금 출출함", "보통", "매우 배고픔"],
    horizontal=True
)

st.divider()

st.subheader("2. 세부 선호 입력")

spicy_preference = st.radio(
    "매운맛 선호",
    ["안 매운 음식", "약간 매운 음식", "매운 음식"],
    horizontal=True
)

eating_style = st.selectbox(
    "조리/섭취 방식",
    ["집밥", "외식", "배달", "간편식"]
)

avoid_ingredient = st.selectbox(
    "피하고 싶은 재료",
    ["없음", "밀가루", "튀김", "유제품", "고기"]
)

st.divider()

st.subheader("3. 메뉴 추천 받기")

if st.button("메뉴 추천받기", type="primary", use_container_width=True):
    payload = {
        "meal_time": meal_time,
        "food_type": food_type,
        "health_goal": health_goal,
        "hunger_level": hunger_level,
        "spicy_preference": spicy_preference,
        "eating_style": eating_style,
        "avoid_ingredient": avoid_ingredient,
    }

    try:
        with st.spinner("FastAPI 서버에 메뉴 추천 요청을 보내는 중입니다..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            recommendation = result["recommendation"]
            summary = result["input_summary"]

            st.success("추천 결과를 FastAPI에서 받아왔습니다.")
            st.info(result["message"])

            st.subheader("📌 입력 요약")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**식사 시간:** {summary['meal_time']}")
                st.write(f"**식사 유형:** {summary['food_type']}")
                st.write(f"**건강 목표:** {summary['health_goal']}")
                st.write(f"**허기짐:** {summary['hunger_level']}")

            with col2:
                st.write(f"**매운맛 선호:** {summary['spicy_preference']}")
                st.write(f"**식사 방식:** {summary['eating_style']}")
                st.write(f"**피하고 싶은 재료:** {summary['avoid_ingredient']}")

            st.divider()

            st.subheader("🍽️ 추천 메뉴")

            with st.container(border=True):
                st.markdown(f"## {recommendation['main_menu']}")
                st.write(f"**함께 먹기 좋은 메뉴:** {recommendation['side_menu']}")
                st.write(f"**추천 음료:** {recommendation['drink']}")

            st.subheader("💡 추천 이유")

            with st.container(border=True):
                st.write(recommendation["reason"])

            st.subheader("🥗 영양 포인트")

            with st.container(border=True):
                st.write(recommendation["nutrition_point"])

            st.subheader("⚠️ 선택 팁")

            with st.container(border=True):
                st.write(f"**피하고 싶은 재료 관련:** {recommendation['avoid_tip']}")
                st.write(f"**매운맛 관련:** {recommendation['spicy_tip']}")

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

st.divider()

st.caption("본 서비스는 Streamlit 프론트엔드와 FastAPI 백엔드가 HTTP 통신으로 연결된 메뉴 추천 웹 애플리케이션입니다.")