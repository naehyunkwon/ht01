"""
==========================================
  건강 트래커 (Health Tracker)
  버전: 1.0.0
  저장소: health_data.json
==========================================
"""

import json
import os
from datetime import date, datetime

DATA_FILE = "health_data.json"

# ──────────────────────────────────────────
# 데이터 저장 / 불러오기
# ──────────────────────────────────────────

def load_data() -> dict:
    """health_data.json 파일에서 기록을 불러옵니다."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("⚠️  데이터 파일을 읽는 중 오류가 발생했습니다. 새 파일을 시작합니다.")
        return {}


def save_data(data: dict) -> None:
    """기록을 health_data.json 파일에 저장합니다."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 데이터가 '{DATA_FILE}'에 저장되었습니다.")
    except IOError as e:
        print(f"⚠️  파일 저장 중 오류가 발생했습니다: {e}")

# ──────────────────────────────────────────
# 입력 헬퍼 함수
# ──────────────────────────────────────────

def input_float(prompt: str, min_val: float = 0, max_val: float = 9999) -> float:
    """유효한 범위의 실수를 입력받습니다."""
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            print(f"  ❌ {min_val} ~ {max_val} 사이의 값을 입력하세요.")
        except ValueError:
            print("  ❌ 숫자를 입력하세요.")


def input_choice(prompt: str, valid: list) -> str:
    """지정된 선택지 중 하나를 입력받습니다."""
    while True:
        val = input(prompt).strip().lower()
        if val in valid:
            return val
        print(f"  ❌ 다음 중 하나를 입력하세요: {', '.join(valid)}")

# ──────────────────────────────────────────
# 기능 1 : 오늘 기록 추가
# ──────────────────────────────────────────

def add_record(data: dict) -> dict:
    """오늘 날짜의 건강 기록을 입력받아 저장합니다."""
    today = str(date.today())          # "2026-03-17"
    print(f"\n📅 오늘 날짜: {today}")

    if today in data:
        overwrite = input_choice(
            "⚠️  오늘 기록이 이미 있습니다. 덮어쓰시겠습니까? (y/n): ",
            ["y", "n"]
        )
        if overwrite == "n":
            print("기록 추가를 취소했습니다.")
            return data

    print("\n─── 건강 정보를 입력하세요 ───")

    # 1. 체중
    weight = input_float("  ⚖️  체중 (kg): ", 20, 300)

    # 2. 수면 시간
    sleep = input_float("  🛌 수면 시간 (시간, 예: 7.5): ", 0, 24)

    # 3. 운동 여부 & 시간
    exercised_raw = input_choice("  🏃 오늘 운동하셨나요? (y/n): ", ["y", "n"])
    exercised = exercised_raw == "y"
    exercise_minutes = 0
    if exercised:
        exercise_minutes = int(input_float("  ⏱️  운동 시간 (분): ", 1, 1440))

    # 4. 식사 점수
    print("  🍽️  식사 점수")
    print("       1) 나쁨  2) 보통  3) 좋음")
    meal_map = {"1": "나쁨", "2": "보통", "3": "좋음"}
    meal_key = input_choice("  선택 (1/2/3): ", ["1", "2", "3"])
    meal_score = meal_map[meal_key]

    record = {
        "date": today,
        "weight_kg": weight,
        "sleep_hours": sleep,
        "exercised": exercised,
        "exercise_minutes": exercise_minutes,
        "meal_score": meal_score,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    data[today] = record

    print("\n─────────────── 입력 확인 ───────────────")
    print(f"  날짜      : {today}")
    print(f"  체중      : {weight} kg")
    print(f"  수면      : {sleep} 시간")
    print(f"  운동      : {'✔ ' + str(exercise_minutes) + '분' if exercised else '✘ 미운동'}")
    print(f"  식사 점수 : {meal_score}")
    print("─────────────────────────────────────────")

    save_data(data)
    return data

# ──────────────────────────────────────────
# 기능 2 : 과거 기록 보기
# ──────────────────────────────────────────

def view_records(data: dict) -> None:
    """저장된 모든 기록을 날짜 순으로 출력합니다."""
    if not data:
        print("\n📭 저장된 기록이 없습니다.")
        return

    print("\n══════════════ 📋 과거 기록 ══════════════")
    print(f"{'날짜':<12} {'체중(kg)':>8} {'수면(h)':>8} {'운동':>10} {'식사':>8}")
    print("─" * 52)

    for key in sorted(data.keys()):
        r = data[key]
        exercise_str = (
            f"✔ {r['exercise_minutes']}분" if r["exercised"] else "✘ 미운동"
        )
        print(
            f"{r['date']:<12}"
            f"{r['weight_kg']:>8.1f}"
            f"{r['sleep_hours']:>8.1f}"
            f"{exercise_str:>10}"
            f"  {r['meal_score']:>8}"
        )
    print("═" * 52)
    print(f"  총 기록 수: {len(data)}일\n")

# ──────────────────────────────────────────
# 기능 3 : 요약 통계
# ──────────────────────────────────────────

MEAL_SCORE_KO = {"나쁨": 1, "보통": 2, "좋음": 3}

def show_summary(data: dict) -> None:
    """평균 체중, 평균 수면, 총 운동 일수 등 요약 정보를 출력합니다."""
    if not data:
        print("\n📭 요약할 기록이 없습니다.")
        return

    records = list(data.values())
    count = len(records)

    avg_weight = sum(r["weight_kg"] for r in records) / count
    avg_sleep  = sum(r["sleep_hours"] for r in records) / count
    exercise_days = sum(1 for r in records if r["exercised"])
    total_exercise_min = sum(r["exercise_minutes"] for r in records)

    meal_counts = {"나쁨": 0, "보통": 0, "좋음": 0}
    for r in records:
        meal_counts[r["meal_score"]] = meal_counts.get(r["meal_score"], 0) + 1

    most_meal = max(meal_counts, key=lambda k: meal_counts[k])

    # 체중 변화 (초기 → 최신)
    sorted_keys = sorted(data.keys())
    first_weight = data[sorted_keys[0]]["weight_kg"]
    last_weight  = data[sorted_keys[-1]]["weight_kg"]
    weight_change = last_weight - first_weight
    change_icon = "📈" if weight_change > 0 else ("📉" if weight_change < 0 else "➡️")

    print("\n══════════════ 📊 건강 요약 ══════════════")
    print(f"  📅 기록 기간   : {sorted_keys[0]}  ~  {sorted_keys[-1]}")
    print(f"  📆 총 기록 수  : {count}일")
    print()
    print(f"  ⚖️  평균 체중   : {avg_weight:.1f} kg")
    print(f"  {change_icon}  체중 변화   : {weight_change:+.1f} kg  ({first_weight:.1f} → {last_weight:.1f})")
    print()
    print(f"  🛌 평균 수면   : {avg_sleep:.1f} 시간")
    print()
    print(f"  🏃 총 운동 일수 : {exercise_days}일 / {count}일")
    print(f"  ⏱️  총 운동 시간 : {total_exercise_min}분  ({total_exercise_min // 60}시간 {total_exercise_min % 60}분)")
    print()
    print(f"  🍽️  식사 점수 분포")
    for label in ["좋음", "보통", "나쁨"]:
        bar = "▓" * meal_counts[label] + "░" * (count - meal_counts[label])
        print(f"       {label:>4}: [{bar}] {meal_counts[label]}회")
    print(f"  🏆 가장 많은 식사 점수: {most_meal}")
    print("═" * 46)

# ──────────────────────────────────────────
# 메인 메뉴
# ──────────────────────────────────────────

MENU_BANNER = """
╔═══════════════════════════════════════╗
║       🌿 건강 트래커 (Health Tracker)        ║
╠═══════════════════════════════════════╣
║  1. 오늘 건강 기록 추가               ║
║  2. 과거 기록 보기                    ║
║  3. 요약 통계 보기                    ║
║  4. 종료                              ║
╚═══════════════════════════════════════╝"""


def main() -> None:
    print(MENU_BANNER)
    data = load_data()
    print(f"  📂 기존 기록 {len(data)}개를 불러왔습니다.\n")

    while True:
        print("\n──── 메뉴 선택 ────")
        print("  1) 오늘 기록 추가")
        print("  2) 과거 기록 보기")
        print("  3) 요약 통계")
        print("  4) 종료")
        choice = input("번호를 입력하세요: ").strip()

        if choice == "1":
            data = add_record(data)
        elif choice == "2":
            view_records(data)
        elif choice == "3":
            show_summary(data)
        elif choice == "4":
            print("\n👋 건강 트래커를 종료합니다. 건강하세요!\n")
            break
        else:
            print("❌ 1~4 중에서 선택하세요.")


if __name__ == "__main__":
    main()
