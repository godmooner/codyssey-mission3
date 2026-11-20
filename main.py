# Mini NPU 시뮬레이터 (Codyssey 미션 E1-3)

import json
import math

EPSILON = 1e-9  # 두 점수의 차이가 이보다 작으면 "같다"로 본다
DATA_PATH = "data.json"
LABEL_MAP = {"+": "Cross", "cross": "Cross", "x": "X"}  # 라벨 통일 규칙


def read_matrix(name, n):
    """n x n 행렬을 한 줄씩 입력받아 2차원 list로 돌려준다."""
    print(f"\n[{name}] {n}x{n} 행렬을 한 줄씩 입력하세요.")
    matrix = []
    while len(matrix) < n:  # n줄이 다 찰 때까지 반복
        text = input(f"  {len(matrix) + 1}행: ")
        parts = text.split()

        # 예외 ②: 숫자 개수가 n개가 아님 (빈 줄이면 0개)
        if len(parts) != n:
            print(f"  숫자 {n}개가 필요한데 {len(parts)}개가 입력되었습니다. 이 행을 다시 입력하세요.")
            continue

        row = []
        # 예외 ①: 숫자로 바꿀 수 없는 값 (예: abc)
        try:
            for part in parts:
                row.append(float(part))
        except ValueError:
            print("  숫자가 아닌 값이 있습니다. 이 행을 다시 입력하세요.")
            continue

        # 예외 ③: nan, inf는 float()를 통과하지만 계산에 쓸 수 없음
        has_invalid = False
        for value in row:
            if not math.isfinite(value):
                has_invalid = True
        if has_invalid:
            print("  nan, inf는 사용할 수 없습니다. 이 행을 다시 입력하세요.")
            continue

        matrix.append(row)
    return matrix


def print_matrix(matrix):
    """행렬을 한 줄에 한 행씩 출력한다."""
    for row in matrix:
        print("  ", row)


def read_mode():
    """1 또는 2가 들어올 때까지 다시 묻는다."""
    while True:
        choice = input("모드를 선택하세요 (1: 직접 입력 3x3, 2: data.json 분석): ").strip()
        if choice in ("1", "2"):
            return choice
        print("잘못된 입력입니다. 1 또는 2를 입력하세요.")


def mac(pattern, filter_matrix):
    """같은 위치의 값끼리 곱해서 전부 더한 값(MAC 점수)을 돌려준다."""
    n = len(pattern)
    total = 0.0
    for i in range(n):          # 행
        for j in range(n):      # 열
            total += pattern[i][j] * filter_matrix[i][j]
    return total


def judge(score_a, score_b):
    """두 점수 중 큰 쪽을 판정한다. 차이가 EPSILON보다 작으면 UNDECIDED."""
    # 동점 검사를 가장 먼저: 부동소수점 오차 수준의 차이는 같은 점수로 본다
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"


def run_mode1():
    """모드 1: 필터 A·B 입력 → 저장 확인 → 패턴 입력"""
    n = 3
    filter_a = read_matrix("필터 A", n)
    filter_b = read_matrix("필터 B", n)

    print("\n필터 저장 완료")
    print("필터 A:")
    print_matrix(filter_a)
    print("필터 B:")
    print_matrix(filter_b)

    pattern = read_matrix("패턴", n)
    print("\n패턴 저장 완료")
    print_matrix(pattern)

    # MAC 점수 계산
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    print(f"\n필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    print(f"판정: {judge(score_a, score_b)}")


def load_data(path):
    """JSON 파일을 읽어 dict로 돌려준다. 실패하면 안내 후 None."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{path} 파일을 찾을 수 없습니다. mission03 폴더에서 실행하세요.")
        return None
    except json.JSONDecodeError:
        print(f"{path}의 JSON 형식이 올바르지 않습니다.")
        return None


def normalize_label(label):
    """'+', 'cross' → 'Cross' / 'x' → 'X'. 규칙에 없는 라벨이면 None."""
    return LABEL_MAP.get(label.strip().lower())


def run_mode2():
    """모드 2: data.json 분석"""
    print("\n=== 모드 2: data.json 분석 ===")
    data = load_data(DATA_PATH)
    if data is None:
        return

    for case_id, case in data["patterns"].items():
        n = int(case_id.split("_")[1])          # "size_13_2" → ["size", "13", "2"] → 13
        filters = data["filters"][f"size_{n}"]  # {"cross": 행렬, "x": 행렬}
        pattern = case["input"]

        score_cross = mac(pattern, filters["cross"])
        score_x = mac(pattern, filters["x"])
        result = judge(score_cross, score_x)    # A = cross 쪽, B = x 쪽

        # 판정 이름 통일: A/B → Cross/X
        if result == "A":
            decision = "Cross"
        elif result == "B":
            decision = "X"
        else:
            decision = "UNDECIDED"

        # 정답 이름 통일: +/x → Cross/X
        expected = normalize_label(case["expected"])

        if decision == expected:
            status = "PASS"
        else:
            status = "FAIL"

        print(f"[{case_id}] Cross: {score_cross} | X: {score_x} "
              f"| 판정: {decision} | expected: {expected} | {status}")


# 이 파일을 직접 실행했을 때의 시작점
if __name__ == "__main__":
    # 예외 ④: Ctrl+C(KeyboardInterrupt), 입력 끝(EOFError) → 안내 후 종료
    try:
        mode = read_mode()
        if mode == "1":
            run_mode1()
        else:
            run_mode2()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
