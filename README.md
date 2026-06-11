# 오늘 뭐 먹지?

Streamlit + FastAPI + Docker + AWS EC2 기반 메뉴 추천 웹 애플리케이션입니다.

## 프로젝트 개요

사용자가 식사 시간, 선호 식사 유형, 건강 목표, 허기짐 정도, 매운맛 선호, 식사 방식, 피하고 싶은 재료를 입력하면 FastAPI 백엔드가 메뉴 추천 결과를 JSON 형태로 생성하고, Streamlit 프론트엔드가 그 결과를 화면에 출력합니다.

## 주요 기능

- Streamlit 사용자 입력 화면
- FastAPI 메뉴 추천 API
- Streamlit에서 FastAPI로 HTTP 요청
- FastAPI JSON 응답 반환
- 건강 목표 기반 메뉴 추천
- 허기짐 정도에 따른 메뉴 양 조정
- 매운맛 선호와 피하고 싶은 재료를 반영한 선택 팁 제공
- Docker Compose 기반 실행
- AWS EC2 배포 가능

## 프로젝트 구조

```text
meal-course-recommender/
├── front/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── back/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md