from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Meal Menu Recommendation API",
    description="식사 취향과 건강 목표를 바탕으로 식사 메뉴를 추천하는 API",
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


def get_main_menu(meal_type: str, health_goal: str, hunger_level: str, companion: str, mood: str) -> dict:
    if health_goal == "다이어트 중":
        if meal_type == "한식":
            name = "현미 닭가슴살 비빔밥"
            description = "현미밥, 닭가슴살, 채소를 함께 먹을 수 있어 포만감은 유지하면서 부담은 줄인 메뉴입니다."
        elif meal_type == "일식":
            name = "연어 포케 bowl"
            description = "연어와 채소가 중심이 되어 단백질과 신선한 재료를 함께 섭취할 수 있는 메뉴입니다."
        elif meal_type == "양식":
            name = "그릴드 치킨 샐러드"
            description = "구운 닭고기와 채소 중심의 메뉴로 가볍게 먹고 싶을 때 적합합니다."
        else:
            name = "저칼로리 샐러드볼"
            description = "채소와 단백질을 중심으로 구성해 식사량을 조절하기 좋은 메뉴입니다."

    elif health_goal == "단백질 중심":
        if meal_type == "한식":
            name = "생선구이 정식"
            description = "생선 단백질과 밥, 반찬을 함께 먹을 수 있어 균형 잡힌 단백질 식사로 적합합니다."
        elif meal_type == "일식":
            name = "연어덮밥"
            description = "연어를 중심으로 단백질과 탄수화물을 함께 섭취할 수 있는 메뉴입니다."
        elif meal_type == "양식":
            name = "스테이크 샐러드"
            description = "고기 단백질과 채소를 함께 먹을 수 있어 단백질 중심 목표에 잘 맞습니다."
        elif meal_type == "중식":
            name = "마파두부 덮밥"
            description = "두부 단백질과 밥을 함께 먹을 수 있어 든든한 단백질 메뉴입니다."
        else:
            name = "닭가슴살 덮밥"
            description = "단백질 섭취를 우선으로 하면서 한 끼 식사로도 충분한 메뉴입니다."

    elif hunger_level == "매우 배고픔":
        if meal_type == "한식":
            name = "돼지국밥"
            description = "허기짐이 큰 상태에서 든든하게 먹을 수 있는 한식 메뉴입니다."
        elif meal_type == "중식":
            name = "볶음밥과 탕수육 세트"
            description = "포만감이 높고 여러 명이 함께 먹기에도 좋은 메뉴입니다."
        elif meal_type == "분식":
            name = "김밥과 떡볶이 세트"
            description = "빠르고 든든하게 먹기 좋은 조합입니다."
        else:
            name = f"든든한 {meal_type} 한 끼"
            description = "현재 허기짐 정도가 높기 때문에 포만감 있는 메뉴를 추천했습니다."

    elif companion == "연인" or mood == "사진 찍기 좋은 곳":
        if meal_type == "양식":
            name = "크림 파스타와 샐러드"
            description = "분위기 있는 식사에 어울리고 함께 나눠 먹기 좋은 메뉴입니다."
        elif meal_type == "일식":
            name = "초밥 세트"
            description = "깔끔하고 보기 좋은 메뉴로 데이트나 특별한 식사에 잘 맞습니다."
        else:
            name = f"정갈한 {meal_type} 세트 메뉴"
            description = "플레이팅과 분위기를 함께 고려한 메뉴입니다."

    elif companion == "가족":
        name = "나눠 먹기 좋은 정식 메뉴"
        description = "여러 사람이 함께 먹기 편하고 호불호가 적은 메뉴를 추천했습니다."

    elif mood == "가성비 좋은 곳":
        name = "가성비 덮밥 메뉴"
        description = "가격 부담이 적고 한 끼 식사로 충분한 메뉴입니다."

    else:
        name = f"균형 잡힌 {meal_type} 메뉴"
        description = "식사 유형과 건강 목표를 무난하게 반영한 균형형 메뉴입니다."

    reason = (
        f"선호 식사 유형은 '{meal_type}', 건강 목표는 '{health_goal}', "
        f"허기짐 정도는 '{hunger_level}'입니다. "
        f"동행 유형 '{companion}'과 원하는 분위기 '{mood}'까지 고려해 "
        f"가장 적합한 메인 메뉴를 추천했습니다."
    )

    return {
        "name": name,
        "description": description,
        "reason": reason,
    }


def get_alternative_menu(meal_type: str, health_goal: str, hunger_level: str) -> dict:
    if health_goal == "다이어트 중":
        name = "포케 또는 샐러드볼"
        description = "가볍지만 한 끼로 충분하고, 재료 구성을 조절하기 쉬운 대체 메뉴입니다."

    elif health_goal == "단백질 중심":
        name = "닭가슴살 덮밥 또는 연어덮밥"
        description = "단백질 섭취를 보완하기 좋은 대체 메뉴입니다."

    elif hunger_level == "매우 배고픔":
        name = "덮밥 또는 국밥류"
        description = "포만감이 높아 허기짐을 빠르게 해결하기 좋은 대체 메뉴입니다."

    elif meal_type == "분식":
        name = "김밥과 우동 조합"
        description = "분식 중에서도 식사 구성이 비교적 안정적인 대체 메뉴입니다."

    else:
        name = "정식 또는 덮밥 메뉴"
        description = "실패 확률이 낮고 한 끼 식사로 무난한 대체 메뉴입니다."

    return {
        "name": name,
        "description": description,
    }


def get_light_menu(health_goal: str, dessert_type: str) -> dict:
    if health_goal == "다이어트 중":
        name = "샐러드와 단백질 토핑"
        description = "식사량을 조절하면서도 단백질을 챙길 수 있는 가벼운 메뉴입니다."

    elif dessert_type in ["베이커리", "아이스크림"]:
        name = "가벼운 샌드위치"
        description = "디저트를 먹을 예정이라면 메인 식사는 너무 무겁지 않은 메뉴가 적합합니다."

    elif health_goal == "가볍게 먹기":
        name = "오픈 샌드위치 또는 샐러드랩"
        description = "부담 없이 먹기 좋고 식후 활동에도 무리가 적은 메뉴입니다."

    else:
        name = "미니 덮밥 또는 샐러드랩"
        description = "과하지 않게 식사하고 싶을 때 선택하기 좋은 가벼운 메뉴입니다."

    return {
        "name": name,
        "description": description,
    }


def get_dessert_tip(dessert_type: str, health_goal: str) -> dict:
    if health_goal == "다이어트 중":
        if dessert_type == "저당 음료":
            recommendation = "무가당 라떼 또는 아메리카노"
        elif dessert_type == "과일/요거트":
            recommendation = "그릭요거트와 과일"
        else:
            recommendation = "작은 사이즈 디저트와 아메리카노"
    else:
        if dessert_type == "커피":
            recommendation = "아메리카노 또는 라떼"
        elif dessert_type == "베이커리":
            recommendation = "소금빵 또는 크루아상"
        elif dessert_type == "아이스크림":
            recommendation = "젤라또 또는 아이스크림"
        elif dessert_type == "과일/요거트":
            recommendation = "요거트볼 또는 과일컵"
        else:
            recommendation = "저당 음료"

    return {
        "title": "식후 디저트 추천",
        "recommendation": recommendation,
        "reason": f"선택한 디저트 유형 '{dessert_type}'과 건강 목표 '{health_goal}'을 함께 고려했습니다.",
    }


def get_after_meal_tip(walk_time: str, health_goal: str) -> dict:
    if walk_time == "0분":
        activity = "식사 후 바로 앉기보다는 5분 정도 가볍게 움직이기"
    elif walk_time == "10분":
        activity = "식사 후 10분 정도 천천히 걷기"
    elif walk_time == "20분":
        activity = "식사 후 20분 정도 가볍게 산책하기"
    else:
        activity = "식사 후 30분 이상 여유롭게 걷기"

    return {
        "title": "식후 활동 팁",
        "activity": activity,
        "reason": f"건강 목표 '{health_goal}'과 산책 가능시간 '{walk_time}'을 반영했습니다.",
    }


def calculate_score(health_goal: str, hunger_level: str, companion: str, mood: str, walk_time: str) -> int:
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
        score += 5

    return min(score, 98)


def get_badge(score: int) -> str:
    if score >= 92:
        return "오늘의 강력 추천 메뉴"
    if score >= 86:
        return "상황 맞춤 추천 메뉴"
    return "가볍게 즐기기 좋은 메뉴"


@app.get("/")
def root():
    return {
        "message": "Meal Menu Recommendation API is running.",
        "docs": "/docs",
    }


@app.post("/recommend")
def recommend(data: RecommendationRequest):
    main_menu = get_main_menu(
        data.meal_type,
        data.health_goal,
        data.hunger_level,
        data.companion,
        data.mood,
    )

    alternative_menu = get_alternative_menu(
        data.meal_type,
        data.health_goal,
        data.hunger_level,
    )

    light_menu = get_light_menu(
        data.health_goal,
        data.dessert_type,
    )

    dessert_tip = get_dessert_tip(
        data.dessert_type,
        data.health_goal,
    )

    after_meal_tip = get_after_meal_tip(
        data.walk_time,
        data.health_goal,
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
        "recommendation_title": f"{data.health_goal} 목표에 맞춘 {data.meal_type} 메뉴 추천",
        "recommendation_badge": get_badge(score),
        "recommendation_score": score,
        "recommendation_summary": (
            f"'{data.meal_type}' 식사 유형을 기준으로 "
            f"'{data.health_goal}' 목표, '{data.hunger_level}' 상태, "
            f"'{data.companion}' 동행 상황과 '{data.mood}' 분위기를 반영해 메뉴를 추천했습니다."
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
        "main_menu": {
            "emoji": "🍚",
            "title": "메인 추천 메뉴",
            "name": main_menu["name"],
            "description": main_menu["description"],
            "reason": main_menu["reason"],
        },
        "alternative_menu": {
            "emoji": "🥗",
            "title": "대체 추천 메뉴",
            "name": alternative_menu["name"],
            "description": alternative_menu["description"],
        },
        "light_menu": {
            "emoji": "🥪",
            "title": "가벼운 추천 메뉴",
            "name": light_menu["name"],
            "description": light_menu["description"],
        },
        "dessert_tip": dessert_tip,
        "after_meal_tip": after_meal_tip,
    }

    return result