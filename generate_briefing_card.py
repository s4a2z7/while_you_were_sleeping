"""
당신이 잠든 사이 브리핑 카드 이미지 생성
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# 이미지 설정
WIDTH = 1200
HEIGHT = 630
BG_DARK = "#0a0e27"  # 짙은 네이비 배경
BG_ACCENT = "#1a2540"  # 보라색 계열 배경
ACCENT_GREEN = "#10b981"  # 초록색 (상승)
ACCENT_ORANGE = "#f59e0b"  # 주황색 (강조)

# 경로 설정
OUTPUT_DIR = "output/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "briefing_card_20251205.png")

# 이미지 생성
img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
draw = ImageDraw.Draw(img)

# 폰트 설정 (시스템 폰트 사용)
try:
    # Windows 기본 폰트
    title_font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 56)
    heading_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
    normal_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    small_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    label_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
except:
    # 폰트 없을 경우 기본 폰트
    title_font = ImageFont.load_default()
    heading_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()
    label_font = ImageFont.load_default()

# 배경 그라디언트 효과
for y in range(HEIGHT):
    ratio = y / HEIGHT
    # 위에서 아래로 진해지는 효과
    r = int(10 + (25 - 10) * ratio)
    g = int(14 + (32 - 14) * ratio)
    b = int(39 + (60 - 39) * ratio)
    color = (r, g, b)
    draw.line([(0, y), (WIDTH, y)], fill=color)

# 좌상단 라인 (강조)
draw.line([(0, 0), (300, 0)], fill=ACCENT_GREEN, width=6)
draw.line([(0, 0), (0, 100)], fill=ACCENT_GREEN, width=6)

# 상단 제목 영역 배경 (반투명 효과)
draw.rectangle([(0, 0), (WIDTH, 130)], fill="#0f1829", outline="#2a3f5f", width=2)

# 제목
title_text = "당신이 잠든 사이"
date_text = "2025.12.05"

# 제목과 날짜 배치
draw.text((50, 25), title_text, fill="white", font=title_font)
draw.text((50, 85), date_text, fill=ACCENT_ORANGE, font=normal_font)

# 구분선
draw.line([(50, 135), (1150, 135)], fill=ACCENT_GREEN, width=2)

# 왼쪽 섹션 - 종목 정보
left_x = 60
top_y = 160

# 종목 카드 배경
card_height = 300
draw.rectangle([(left_x-10, top_y-10), (560, top_y + card_height)], 
               fill="#1a2540", outline="#3a5f8f", width=2)

# "오늘의 화제 종목" 라벨
draw.text((left_x + 20, top_y + 15), "오늘의 화제 종목", fill="#888888", font=label_font)

# 종목명과 코드
ticker = "TESLA"
code = "(TSLA)"
draw.text((left_x + 20, top_y + 55), ticker, fill="white", font=heading_font)
draw.text((left_x + 20, top_y + 105), code, fill="#aaaaaa", font=normal_font)

# 등락률 (상승이므로 초록색)
change_text = "+8.7%"
change_label = "상승"
draw.text((left_x + 20, top_y + 155), change_text, fill=ACCENT_GREEN, font=heading_font)
draw.text((left_x + 20 + 140, top_y + 165), change_label, fill=ACCENT_GREEN, font=normal_font)

# 선정 기준
criteria_text = "거래량 1위"
criteria_label = "선정 기준"
draw.text((left_x + 20, top_y + 230), criteria_label, fill="#888888", font=label_font)
draw.text((left_x + 20, top_y + 260), criteria_text, fill="#ffffff", font=normal_font)

# 우측 섹션 - 핵심 뉴스
right_x = 600
news_y = 160

# 뉴스 카드 배경
draw.rectangle([(right_x-10, news_y-10), (1150, news_y + card_height)], 
               fill="#1a2540", outline="#3a5f8f", width=2)

# "핵심 뉴스" 라벨
draw.text((right_x + 20, news_y + 15), "핵심 뉴스", fill="#888888", font=label_font)

# 뉴스 제목 (텍스트 랩핑)
news_title = "사이버트럭 판매량 급증"
draw.text((right_x + 20, news_y + 55), news_title, fill="white", font=heading_font)

# 뉴스 아이콘
draw.text((right_x + 20, news_y + 130), "📰", font=heading_font)
draw.text((right_x + 80, news_y + 130), "시장 영향도 높음", fill=ACCENT_ORANGE, font=normal_font)

# 핵심 포인트
draw.text((right_x + 20, news_y + 200), "• 4분기 판매량 목표 달성", fill="#cccccc", font=small_font)
draw.text((right_x + 20, news_y + 240), "• 시가총액 사상 최고 경신", fill="#cccccc", font=small_font)

# 하단 영역
info_y = 480

# 하단 배경 바
draw.rectangle([(0, info_y - 20), (WIDTH, HEIGHT)], fill="#0f1829", outline=ACCENT_GREEN, width=2)

# "생성 시간" 정보
generated_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
draw.text((60, info_y), f"생성 시간: {generated_time}", fill="#666666", font=small_font)

# 로고/브랜드
logo_text = "While You Were Sleeping"
draw.text((1120, info_y), logo_text, fill="#666666", font=small_font, anchor="rm")

# 하단 메시지
message = "당신이 잠든 사이, 세상은 움직였습니다"
message_bbox = draw.textbbox((0, 0), message, font=normal_font)
message_width = message_bbox[2] - message_bbox[0]
message_x = (WIDTH - message_width) // 2
draw.text((message_x, info_y + 50), message, fill=ACCENT_GREEN, font=normal_font)

# 이미지 저장
img.save(OUTPUT_PATH)
print(f"✅ 이미지 생성 완료: {OUTPUT_PATH}")
print(f"📐 크기: {WIDTH}x{HEIGHT}px")
print(f"📊 제목: 당신이 잠든 사이 | 2025.12.05")
print(f"🚀 종목: TESLA (TSLA) | +8.7% 상승")
print(f"📰 뉴스: 사이버트럭 판매량 급증")
