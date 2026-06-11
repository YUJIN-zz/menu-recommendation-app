from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Meal Course Recommendation API",
    description="식사 취향과 건강 목표를 바탕으로 식사, 디저트, 산책 코스를 추천하는 API",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    meal_type: str
    health_goal: str
    dessert_type: str
    hunger_level: str
    companion: str
    mood: str
    walk_time: str


def get_restaurant_recommendation(
    meal_type: str,
    health_goal: str,
    hunger_level: str,
    companion: str,
    mood: str,
) -> dict:
    if health_goal == "다이어트 중":
        if meal_type in ["샐러드/건강식", "한식"]:
            title = "가벼운 건강식 식당"
            menu = "샐러드볼, 닭가슴살 덮밥, 현미 비빔밥"
        else:
            title = f"부담 적은 {meal_type} 식당"
            menu = "저칼로리 메뉴, 구운 단백질 메뉴, 채소 중심 메뉴"

    elif health_goal == "단백질 중심":
        title = "단백질 충전 식당"
        if meal_type == "한식":
            menu = "제육 없는 백반, 닭갈비, 생선구이 정식"
        elif meal_type == "일식":
            menu = "연어덮밥, 초밥, 사케동"
        elif meal_type == "양식":
            menu = "스테이크 샐러드, 그릴드 치킨, 포케"
        else:
            menu = "고기·계란·두부가 포함된 든든한 메뉴"

    elif hunger_level == "매우 배고픔":
        title = "든든한 한 끼 식당"
        menu = "덮밥, 국밥, 파스타, 볶음밥처럼 포만감 있는 메뉴"

    elif companion == "연인" or mood == "사진 찍기 좋은 곳":
        title = "분위기 좋은 식당"
        menu = "플레이팅이 예쁜 메뉴, 파스타, 스테이크, 정갈한 정식"

    elif companion == "가족":
        title = "편안한 가족 식사 식당"
        menu = "한식 정식, 샤브샤브, 중식 요리, 나눠 먹기 좋은 메뉴"

    elif mood == "가성비 좋은 곳":
        title = "가성비 좋은 식당"
        menu = "덮밥, 분식 세트, 백반, 면 요리"

    else:
        title = f"균형 잡힌 {meal_type} 식당"
        menu = "탄수화물, 단백질, 채소가 함께 있는 균형식 메뉴"

    reason = (
        f"선호 식사 유형은 '{meal_type}', 건강 목표는 '{health_goal}', "
        f"허기짐 정도는 '{hunger_level}'입니다. "
        f"동행 유형 '{companion}'과 원하는 분위기 '{mood}'까지 고려해 "
        f"식사 만족도와 상황 적합성이 높은 코스를 추천했습니다."
    )

    return {
        "title": title,
        "menu": menu,
        "reason": reason,
    }


def get_cafe_recommendation(dessert_type: str, health_goal: str, mood: str) -> dict:
    if health_goal == "다이어트 중":
        if dessert_type == "저당 음료":
            title = "저당 음료 카페"
            menu = "아메리카노, 무가당 라떼, 저당 티"
        elif dessert_type == "과일/요거트":
            title = "가벼운 요거트 카페"
            menu = "그릭요거트, 과일컵, 무가당 요거트"
        else:
            title = "부담 적은 디저트 카페"
            menu = "작은 사이즈 디저트, 티, 아메리카노"

    elif mood == "사진 찍기 좋은 곳":
        title = "감성 디저트 카페"
        menu = "시그니처 음료, 케이크, 크림 라떼"

    elif mood == "조용한 곳":
        title = "조용히 쉬기 좋은 카페"
        menu = "따뜻한 차, 아메리카노, 라떼"

    elif dessert_type == "베이커리":
        title = "베이커리 카페"
        menu = "크루아상, 소금빵, 샌드위치"

    elif dessert_type == "아이스크림":
        title = "달콤한 디저트 카페"
        menu = "아이스크림, 젤라또, 와플"

    elif dessert_type == "과일/요거트":
        title = "산뜻한 디저트 카페"
        menu = "요거트볼, 과일주스, 스무디"

    else:
        title = "깔끔한 커피 카페"
        menu = "아메리카노, 라떼, 콜드브루"

    reason = (
        f"선택한 디저트 유형은 '{dessert_type}'입니다. "
        f"건강 목표 '{health_goal}'과 원하는 분위기 '{mood}'을 함께 반영해 "
        f"식사 후 부담 없이 이어갈 수 있는 디저트 코스를 추천했습니다."
    )

    return {
        "title": title,
        "menu": menu,
        "reason": reason,
    }


def get_walk_recommendation(walk_time: str, health_goal: str, mood: str) -> dict:
    if walk_time == "0분":
        title = "휴식 중심 마무리 코스"
        activity = "산책 대신 카페나 실내 공간에서 짧게 쉬기"

    elif walk_time == "10분":
        title = "가벼운 소화 산책 코스"
        activity = "식당 주변을 천천히 걷는 10분 산책"

    elif walk_time == "20분":
        title = "균형 잡힌 식후 산책 코스"
        activity = "공원이나 조용한 길을 따라 걷는 20분 산책"

    else:
        title = "여유로운 리프레시 산책 코스"
        activity = "식사 후 기분 전환까지 할 수 있는 30분 이상 산책"

    reason = (
        f"식사 후 산책 가능시간은 '{walk_time}'입니다. "
        f"건강 목표 '{health_goal}'과 원하는 분위기 '{mood}'을 반영해 "
        f"식후 부담을 줄이고 자연스럽게 마무리할 수 있는 활동을 추천했습니다."
    )

    return {
        "title": title,
        "activity": activity,
        "reason": reason,
    }


def calculate_score(
    health_goal: str,
    hunger_level: str,
    companion: str,
    mood: str,
    walk_time: str,
) -> int:
    score = 76

    if health_goal in ["단백질 중심", "다이어트 중", "균형 잡힌 식사"]:
        score += 7

    if hunger_level in ["보통", "매우 배고픔"]:
        score += 4

    if companion in ["친구", "연인", "가족"]:
        score += 4

    if mood in ["건강한 느낌", "든든한 한 끼", "조용한 곳"]:
        score += 4

    if walk_time != "0분":
        score += 6

    return min(score, 98)


def get_badge(score: int) -> str:
    if score >= 92:
        return "오늘의 베스트 식후 코스"
    if score >= 86:
        return "균형 잡힌 추천 코스"
    return "가볍게 즐기기 좋은 코스"


@app.get("/")
def root():
    return {
        "message": "Meal Course Recommendation API is running.",
        "docs": "/docs",
    }


@app.post("/recommend")
def recommend(data: RecommendationRequest):
    restaurant = get_restaurant_recommendation(
        data.meal_type,
        data.health_goal,
        data.hunger_level,
        data.companion,
        data.mood,
    )

    cafe = get_cafe_recommendation(
        data.dessert_type,
        data.health_goal,
        data.mood,
    )

    walk = get_walk_recommendation(
        data.walk_time,
        data.health_goal,
        data.mood,
    )

    score = calculate_score(
        data.health_goal,
        data.hunger_level,
        data.companion,
        data.mood,
        data.walk_time,
    )

    result = {
        "message": "추천 결과가 FastAPI에서 JSON 형태로 생성되었습니다.",
        "course_title": f"{data.health_goal} 식사 + {data.dessert_type} 디저트 + {data.walk_time} 식후 루틴",
        "course_badge": get_badge(score),
        "recommendation_score": score,
        "course_summary": (
            f"'{data.meal_type}' 식사 취향을 바탕으로 "
            f"'{data.health_goal}' 목표, '{data.dessert_type}' 디저트, "
            f"'{data.walk_time}' 식후 루틴을 조합한 맞춤형 식후 코스입니다."
        ),
        "input_summary": {
            "meal_type": data.meal_type,
            "health_goal": data.health_goal,
            "dessert_type": data.dessert_type,
            "hunger_level": data.hunger_level,
            "companion": data.companion,
            "mood": data.mood,
            "walk_time": data.walk_time,
        },
        "restaurant": {
            "emoji": "🍚",
            "title": restaurant["title"],
            "menu": restaurant["menu"],
            "reason": restaurant["reason"],
        },
        "cafe": {
            "emoji": "☕",
            "title": cafe["title"],
            "menu": cafe["menu"],
            "reason": cafe["reason"],
        },
        "walk": {
            "emoji": "🌿",
            "title": walk["title"],
            "activity": walk["activity"],
            "reason": walk["reason"],
        },
    }

    return result