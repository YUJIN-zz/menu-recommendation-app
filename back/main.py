from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import quote


app = FastAPI(
    title="Meal Course Recommendation API",
    description="식사, 디저트, 산책 코스를 추천하는 FastAPI 백엔드",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    location_text: str
    latitude: float | None = None
    longitude: float | None = None
    meal_type: str
    health_goal: str
    dessert_type: str
    hunger_level: str
    companion: str
    mood: str
    walk_time: str


def make_naver_map_url(keyword: str) -> str:
    encoded_keyword = quote(keyword)
    return f"https://map.naver.com/p/search/{encoded_keyword}"


def get_restaurant_keyword(meal_type: str, health_goal: str, hunger_level: str, companion: str, mood: str) -> str:
    if health_goal == "다이어트 중":
        if meal_type in ["한식", "샐러드/건강식"]:
            return "샐러드 건강식 맛집"
        return f"{meal_type} 저칼로리 맛집"

    if health_goal == "단백질 중심":
        if meal_type == "한식":
            return "단백질 한식 맛집"
        if meal_type == "일식":
            return "연어덮밥 초밥 맛집"
        if meal_type == "양식":
            return "스테이크 샐러드 맛집"
        return f"{meal_type} 단백질 맛집"

    if hunger_level == "매우 배고픔":
        if meal_type == "한식":
            return "든든한 한식 맛집"
        if meal_type == "중식":
            return "중식 맛집"
        if meal_type == "분식":
            return "분식 맛집"
        return f"{meal_type} 든든한 맛집"

    if companion == "연인" or mood == "사진 찍기 좋은 곳":
        return f"{meal_type} 데이트 맛집"

    if companion == "가족":
        return f"{meal_type} 가족식사 맛집"

    if mood == "가성비 좋은 곳":
        return f"{meal_type} 가성비 맛집"

    if mood == "조용한 곳":
        return f"조용한 {meal_type} 맛집"

    return f"{meal_type} 맛집"


def get_cafe_keyword(dessert_type: str, health_goal: str, mood: str) -> str:
    if health_goal == "다이어트 중":
        if dessert_type == "저당 음료":
            return "저당 음료 카페"
        if dessert_type == "과일/요거트":
            return "그릭요거트 카페"
        return "건강 디저트 카페"

    if mood == "사진 찍기 좋은 곳":
        return "감성 카페"

    if mood == "조용한 곳":
        return "조용한 카페"

    if dessert_type == "커피":
        return "분위기 좋은 카페"
    if dessert_type == "베이커리":
        return "베이커리 카페"
    if dessert_type == "아이스크림":
        return "아이스크림 디저트 카페"
    if dessert_type == "과일/요거트":
        return "요거트 디저트 카페"

    return f"{dessert_type} 카페"


def get_walk_keyword(walk_time: str, location_text: str) -> str:
    if walk_time == "0분":
        return f"{location_text} 근처"

    if walk_time == "10분":
        return "가벼운 산책로"

    if walk_time == "20분":
        return "공원 산책로"

    return "걷기 좋은 산책 코스"


def calculate_score(health_goal: str, hunger_level: str, companion: str, mood: str, walk_time: str) -> int:
    score = 78

    if health_goal in ["단백질 중심", "다이어트 중", "균형 잡힌 식사"]:
        score += 6

    if hunger_level in ["보통", "매우 배고픔"]:
        score += 4

    if companion in ["친구", "연인", "가족"]:
        score += 4

    if mood in ["건강한 느낌", "든든한 한 끼", "사진 찍기 좋은 곳"]:
        score += 4

    if walk_time != "0분":
        score += 5

    return min(score, 98)


def get_course_badge(score: int) -> str:
    if score >= 92:
        return "오늘의 강력 추천 코스"
    if score >= 86:
        return "균형 잡힌 추천 코스"
    return "가볍게 즐기기 좋은 코스"


def make_restaurant_reason(meal_type: str, health_goal: str, hunger_level: str, companion: str, mood: str) -> str:
    return (
        f"'{health_goal}' 목표와 '{hunger_level}' 상태를 반영했습니다. "
        f"또한 동행 유형은 '{companion}', 원하는 분위기는 '{mood}'이므로 "
        f"식사 만족도와 상황 적합성을 함께 고려해 {meal_type} 계열의 식당을 추천했습니다."
    )


def make_cafe_reason(dessert_type: str, health_goal: str, mood: str) -> str:
    return (
        f"식사 후 디저트는 '{dessert_type}' 유형을 기준으로 추천했습니다. "
        f"건강 목표 '{health_goal}'과 원하는 분위기 '{mood}'을 함께 반영해 "
        f"식후 부담이 적고 코스 흐름이 자연스러운 카페를 추천했습니다."
    )


def make_walk_reason(walk_time: str) -> str:
    if walk_time == "0분":
        return "산책 시간이 없기 때문에 멀리 이동하지 않고 주변에서 마무리할 수 있는 코스를 추천했습니다."

    return (
        f"식사 후 소화를 돕고 부담 없이 움직일 수 있도록 "
        f"'{walk_time}' 산책 가능시간에 맞는 코스를 추천했습니다."
    )


@app.get("/")
def root():
    return {
        "message": "Meal Course Recommendation API is running.",
        "docs": "/docs"
    }


@app.post("/recommend")
def recommend(data: RecommendationRequest):
    location = data.location_text.strip()

    if not location:
        location = "현재 위치"

    restaurant_keyword = get_restaurant_keyword(
        data.meal_type,
        data.health_goal,
        data.hunger_level,
        data.companion,
        data.mood,
    )

    cafe_keyword = get_cafe_keyword(
        data.dessert_type,
        data.health_goal,
        data.mood,
    )

    walk_keyword = get_walk_keyword(
        data.walk_time,
        location,
    )

    restaurant_search = f"{location} {restaurant_keyword}"
    cafe_search = f"{location} {cafe_keyword}"
    walk_search = f"{location} {walk_keyword}"

    recommendation_score = calculate_score(
        data.health_goal,
        data.hunger_level,
        data.companion,
        data.mood,
        data.walk_time,
    )

    course_title = f"{location} {data.health_goal} + {data.dessert_type} + {data.walk_time} 산책 코스"
    course_badge = get_course_badge(recommendation_score)

    course_summary = (
        f"{location}에서 {data.meal_type} 식사로 시작해 "
        f"{data.dessert_type} 디저트와 {data.walk_time} 산책으로 마무리하는 맞춤형 식후 코스입니다."
    )

    result = {
        "message": "추천 결과가 FastAPI에서 JSON 형태로 생성되었습니다.",
        "course_title": course_title,
        "course_badge": course_badge,
        "course_summary": course_summary,
        "recommendation_score": recommendation_score,
        "course_flow": "식사 → 디저트 → 산책",
        "input_summary": {
            "location": location,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "meal_type": data.meal_type,
            "health_goal": data.health_goal,
            "dessert_type": data.dessert_type,
            "hunger_level": data.hunger_level,
            "companion": data.companion,
            "mood": data.mood,
            "walk_time": data.walk_time,
        },
        "restaurant": {
            "step": "STEP 1",
            "emoji": "🍚",
            "title": "식사 코스",
            "search_keyword": restaurant_search,
            "category": data.meal_type,
            "reason": make_restaurant_reason(
                data.meal_type,
                data.health_goal,
                data.hunger_level,
                data.companion,
                data.mood,
            ),
            "map_url": make_naver_map_url(restaurant_search),
        },
        "cafe": {
            "step": "STEP 2",
            "emoji": "☕",
            "title": "디저트 코스",
            "search_keyword": cafe_search,
            "category": data.dessert_type,
            "reason": make_cafe_reason(
                data.dessert_type,
                data.health_goal,
                data.mood,
            ),
            "map_url": make_naver_map_url(cafe_search),
        },
        "walk": {
            "step": "STEP 3",
            "emoji": "🚶",
            "title": "식후 산책 코스",
            "search_keyword": walk_search,
            "walk_time": data.walk_time,
            "reason": make_walk_reason(data.walk_time),
            "map_url": make_naver_map_url(walk_search),
        },
    }

    return result