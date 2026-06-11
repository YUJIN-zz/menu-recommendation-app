from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Menu Recommendation API",
    description="사용자의 식사 상황과 건강 목표를 바탕으로 메뉴를 추천하는 FastAPI 백엔드",
    version="1.0.0",
)


class MenuRequest(BaseModel):
    meal_time: str
    food_type: str
    health_goal: str
    hunger_level: str
    spicy_preference: str
    eating_style: str
    avoid_ingredient: str


def recommend_main_menu(data: MenuRequest) -> str:
    # 1. 건강 목표 우선 추천
    if data.health_goal == "다이어트":
        if data.food_type == "한식":
            return "닭가슴살 비빔밥"
        if data.food_type == "일식":
            return "연어 포케"
        if data.food_type == "양식":
            return "그릴드 치킨 샐러드"
        if data.food_type == "중식":
            return "청경채 닭고기 볶음"
        if data.food_type == "분식":
            return "곤약 김밥"
        return "단백질 샐러드볼"

    if data.health_goal == "단백질 보충":
        if data.food_type == "한식":
            return "제육덮밥과 계란찜"
        if data.food_type == "일식":
            return "연어덮밥"
        if data.food_type == "양식":
            return "스테이크 샐러드"
        if data.food_type == "중식":
            return "마라 닭고기 덮밥"
        if data.food_type == "분식":
            return "참치김밥과 삶은 계란"
        return "닭가슴살 샐러드"

    if data.health_goal == "든든한 한 끼":
        if data.food_type == "한식":
            return "김치찌개 백반"
        if data.food_type == "일식":
            return "돈카츠 정식"
        if data.food_type == "양식":
            return "토마토 파스타와 샐러드"
        if data.food_type == "중식":
            return "볶음밥과 짬뽕국물"
        if data.food_type == "분식":
            return "떡볶이와 김밥"
        return "고구마 닭가슴살 플레이트"

    if data.health_goal == "가볍게 먹기":
        if data.food_type == "한식":
            return "두부 샐러드 비빔밥"
        if data.food_type == "일식":
            return "유부초밥과 미소국"
        if data.food_type == "양식":
            return "리코타 샐러드"
        if data.food_type == "중식":
            return "계란 토마토 볶음"
        if data.food_type == "분식":
            return "꼬마김밥"
        return "그릭요거트 샐러드볼"

    # 균형 잡힌 식사
    if data.food_type == "한식":
        return "불고기 비빔밥"
    if data.food_type == "일식":
        return "사케동"
    if data.food_type == "양식":
        return "치킨 샌드위치와 샐러드"
    if data.food_type == "중식":
        return "잡채밥"
    if data.food_type == "분식":
        return "김밥과 어묵국"
    return "현미밥 샐러드 플레이트"


def adjust_menu_by_hunger(menu: str, hunger_level: str) -> str:
    if hunger_level == "매우 배고픔":
        return f"{menu} + 사이드 메뉴 추가"
    if hunger_level == "조금 출출함":
        return f"{menu} 소량"
    return menu


def recommend_side_menu(data: MenuRequest) -> str:
    if data.health_goal == "다이어트":
        return "삶은 계란 또는 미소국"

    if data.health_goal == "단백질 보충":
        return "계란찜 또는 닭가슴살 추가"

    if data.hunger_level == "매우 배고픔":
        return "밥 추가 또는 작은 국물 메뉴"

    if data.meal_time == "아침":
        return "과일 또는 요거트"

    if data.meal_time == "야식":
        return "따뜻한 차 또는 가벼운 국물"

    return "샐러드 또는 국물 메뉴"


def recommend_drink(data: MenuRequest) -> str:
    if data.health_goal == "다이어트":
        return "제로 음료 또는 아메리카노"

    if data.meal_time == "아침":
        return "아메리카노 또는 두유"

    if data.spicy_preference == "매운 음식":
        return "쿨피스 대신 물 또는 무가당 차"

    return "물 또는 무가당 차"


def make_reason(data: MenuRequest, main_menu: str) -> str:
    return (
        f"'{data.health_goal}' 목표와 '{data.food_type}' 선호를 우선 반영했습니다. "
        f"현재 허기짐 정도가 '{data.hunger_level}'이고, 식사 방식이 '{data.eating_style}'이기 때문에 "
        f"실제로 선택하기 쉬운 메뉴인 '{main_menu}'을 추천했습니다."
    )


def make_nutrition_point(data: MenuRequest) -> str:
    if data.health_goal == "다이어트":
        return "칼로리를 과하게 높이지 않으면서 포만감을 줄 수 있는 구성을 추천했습니다."

    if data.health_goal == "단백질 보충":
        return "단백질 섭취량을 늘릴 수 있는 메뉴를 중심으로 추천했습니다."

    if data.health_goal == "든든한 한 끼":
        return "탄수화물, 단백질, 지방이 함께 들어가 포만감이 높은 구성을 추천했습니다."

    if data.health_goal == "가볍게 먹기":
        return "부담스럽지 않고 소화가 비교적 쉬운 메뉴를 추천했습니다."

    return "탄수화물, 단백질, 채소가 함께 포함되도록 균형을 고려했습니다."


def make_avoid_tip(data: MenuRequest) -> str:
    if data.avoid_ingredient == "없음":
        return "특별히 피해야 할 재료가 없으므로 선택 폭을 넓게 두었습니다."

    return f"'{data.avoid_ingredient}'을 피하고 싶다고 입력했기 때문에 해당 요소가 적은 메뉴를 선택하는 것이 좋습니다."


def make_spicy_tip(data: MenuRequest) -> str:
    if data.spicy_preference == "안 매운 음식":
        return "자극적인 양념보다는 담백한 소스나 간장 베이스를 선택하는 것이 좋습니다."

    if data.spicy_preference == "약간 매운 음식":
        return "약간의 매운맛은 괜찮지만 너무 자극적인 메뉴는 피하는 것이 좋습니다."

    return "매운 음식을 선택하되, 속이 불편하지 않도록 국물이나 음료를 함께 준비하는 것이 좋습니다."


@app.get("/")
def root():
    return {
        "message": "Menu Recommendation API is running.",
        "docs": "/docs",
    }


@app.post("/recommend")
def recommend_menu(data: MenuRequest):
    base_menu = recommend_main_menu(data)
    main_menu = adjust_menu_by_hunger(base_menu, data.hunger_level)
    side_menu = recommend_side_menu(data)
    drink = recommend_drink(data)

    result = {
        "input_summary": {
            "meal_time": data.meal_time,
            "food_type": data.food_type,
            "health_goal": data.health_goal,
            "hunger_level": data.hunger_level,
            "spicy_preference": data.spicy_preference,
            "eating_style": data.eating_style,
            "avoid_ingredient": data.avoid_ingredient,
        },
        "recommendation": {
            "main_menu": main_menu,
            "side_menu": side_menu,
            "drink": drink,
            "reason": make_reason(data, main_menu),
            "nutrition_point": make_nutrition_point(data),
            "avoid_tip": make_avoid_tip(data),
            "spicy_tip": make_spicy_tip(data),
        },
        "message": "추천 결과가 FastAPI에서 JSON 형태로 생성되었습니다.",
    }

    return result