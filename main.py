# Mini NPU 시뮬레이터 (Codyssey 미션 E1-3)

import json
import math
import time

EPSILON = 1e-9  # 두 점수의 차이가 이보다 작으면 "같다"로 본다
DATA_PATH = "data.json"
REPEAT = 10     # 성능 측정 반복 횟수
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


def print_section(title):
    """단계 제목을 구분선과 함께 출력한다."""
    print("\n" + "-" * 40)
    print(title)
    print("-" * 40)


def make_test_matrix(n):
    """성능 측정용 n x n 행렬 (값은 계산 시간에 영향이 없으니 전부 1.0)."""
    return [[1.0] * n for _ in range(n)]


def measure_mac_time(pattern, filter_matrix):
    """MAC을 REPEAT번 반복해 1회 평균 시간(ms)을 돌려준다. 입력·출력은 측정 구간 밖."""
    start = time.perf_counter()
    for _ in range(REPEAT):
        mac(pattern, filter_matrix)
    elapsed = time.perf_counter() - start  # 초 단위
    return elapsed / REPEAT * 1000         # 1회 평균, ms 단위


def print_performance_table(sizes):
    """크기별 MAC 평균 시간과 연산 횟수(N²)를 표로 출력한다."""
    print("크기    | 평균 시간(ms) | 연산 횟수(N²)")
    for n in sizes:
        matrix = make_test_matrix(n)
        avg_ms = measure_mac_time(matrix, matrix)
        print(f"{n}x{n}".ljust(7) + f" | {avg_ms:13.4f} | {n * n:13}")


def run_mode1():
    """모드 1: 필터 A·B 입력 → 저장 확인 → 패턴 입력"""
    n = 3
    print_section("[1] 필터 입력")
    filter_a = read_matrix("필터 A", n)
    filter_b = read_matrix("필터 B", n)

    print("\n필터 저장 완료")
    print("필터 A:")
    print_matrix(filter_a)
    print("필터 B:")
    print_matrix(filter_b)

    print_section("[2] 패턴 입력")
    pattern = read_matrix("패턴", n)
    print("\n패턴 저장 완료")
    print_matrix(pattern)

    # MAC 점수 계산
    print_section("[3] MAC 결과")
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    result = judge(score_a, score_b)
    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {result}")

    print_section(f"[4] 성능 분석 (MAC {REPEAT}회 평균)")
    print_performance_table([n])  # 3x3 성능


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


def is_square_matrix(matrix, n):
    """matrix가 n x n 모양(길이 n인 list가 n개)이면 True."""
    if not isinstance(matrix, list) or len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
    return True


def normalize_label(label):
    """'+', 'cross' → 'Cross' / 'x' → 'X'. 규칙에 없는 라벨이면 None."""
    return LABEL_MAP.get(str(label).strip().lower())


def run_mode2():
    """모드 2: data.json 분석"""
    print("\n=== 모드 2: data.json 분석 ===")
    data = load_data(DATA_PATH)
    if data is None:
        return

    # 예외 ⑩: 파일 전체 구조(스키마) 오류 — 최상위가 dict가 아니거나 patterns가 없음
    if not isinstance(data, dict) or not isinstance(data.get("patterns"), dict):
        print("data.json 구조 오류: 최상위에 patterns 항목(dict)이 필요합니다.")
        return
    patterns = data["patterns"]
    all_filters = data.get("filters")
    if not isinstance(all_filters, dict):
        print("주의: filters 항목이 없거나 형식이 잘못되어 모든 케이스가 FAIL 처리됩니다.")
        all_filters = {}

    # [1] 필터 로드: 크기별로 Cross·X가 제대로 있는지 미리 보여 주기
    print_section("[1] 필터 로드")
    for filter_key, pair in all_filters.items():
        if isinstance(pair, dict):
            labels = [str(normalize_label(label)) for label in pair]
            print(f"  {filter_key} 필터 로드 ({', '.join(labels)})")
        else:
            print(f"  {filter_key} 필터 형식 오류 (dict가 아님)")

    # [2] 패턴 분석
    print_section("[2] 패턴 분석 (라벨 정규화 적용)")
    passed = 0
    failures = []  # 실패한 케이스의 "이름: 사유" 문자열 모음

    for case_id, case in patterns.items():
        # 예외 ⑪: 케이스 하나가 dict가 아님 (예: "size_5_3": [1, 2])
        if not isinstance(case, dict):
            print(f"[{case_id}] FAIL - 케이스 형식 오류")
            failures.append(f"{case_id}: 케이스 형식 오류(input/expected를 가진 dict가 아님)")
            continue

        # 예외 ⑤: 키 형식 오류 (예: "abc" → [1] 칸 없음 / "size_x_1" → int 실패)
        try:
            n = int(case_id.split("_")[1])      # "size_13_2" → ["size", "13", "2"] → 13
        except (IndexError, ValueError):
            print(f"[{case_id}] FAIL - 키 형식 오류")
            failures.append(f"{case_id}: 키 형식 오류(size_N_idx 형식이 아님)")
            continue

        # 예외 ⑥: 그 크기의 필터가 없음 (예: size_7_1인데 size_7 필터가 없음)
        filter_key = f"size_{n}"
        if not isinstance(all_filters.get(filter_key), dict):
            print(f"[{case_id}] FAIL - {n}x{n} 필터 없음")
            failures.append(f"{case_id}: {n}x{n} 필터 없음")
            continue

        # 필터 키 이름 통일: {"cross": 행렬, "x": 행렬} → {"Cross": 행렬, "X": 행렬}
        filters = {}
        for label, matrix in all_filters[filter_key].items():
            filters[normalize_label(label)] = matrix

        # 예외 ⑦: 크기 불일치 (패턴이나 필터가 n x n이 아님, 빠져 있어도 여기서 걸림)
        pattern = case.get("input")
        if not is_square_matrix(pattern, n):
            print(f"[{case_id}] FAIL - 크기 불일치(패턴이 {n}x{n}이 아님)")
            failures.append(f"{case_id}: 크기 불일치(패턴이 {n}x{n}이 아님)")
            continue
        if not (is_square_matrix(filters.get("Cross"), n) and is_square_matrix(filters.get("X"), n)):
            print(f"[{case_id}] FAIL - {n}x{n} 필터가 없거나 크기 불일치")
            failures.append(f"{case_id}: {n}x{n} 필터가 없거나 크기 불일치")
            continue

        # 예외 ⑧: 규칙에 없는 정답 라벨 (예: "o")
        expected = normalize_label(case.get("expected"))
        if expected is None:
            print(f"[{case_id}] FAIL - 알 수 없는 정답 라벨: {case.get('expected')}")
            failures.append(f"{case_id}: 알 수 없는 정답 라벨({case.get('expected')})")
            continue

        # 예외 ⑨: 행렬 안에 숫자가 아닌 값 (예: "a" * 1.0 → TypeError)
        try:
            score_cross = mac(pattern, filters["Cross"])
            score_x = mac(pattern, filters["X"])
        except TypeError:
            print(f"[{case_id}] FAIL - 행렬에 숫자가 아닌 값이 있음")
            failures.append(f"{case_id}: 행렬에 숫자가 아닌 값이 있음")
            continue

        # 예외 ⑫: 데이터에 NaN·Infinity가 섞여 점수가 망가짐 (비교가 전부 False가 됨)
        if not (math.isfinite(score_cross) and math.isfinite(score_x)):
            print(f"[{case_id}] FAIL - 점수가 nan 또는 inf")
            failures.append(f"{case_id}: 행렬에 nan/inf 값이 있어 점수 계산 불가")
            continue

        result = judge(score_cross, score_x)    # A = Cross 쪽, B = X 쪽

        # 판정 이름 통일: A/B → Cross/X
        if result == "A":
            decision = "Cross"
        elif result == "B":
            decision = "X"
        else:
            decision = "UNDECIDED"

        if decision == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            if decision == "UNDECIDED":
                reason = "두 점수가 epsilon 이내로 같아 판정 불가(UNDECIDED)"
            else:
                reason = f"판정 {decision}, 정답 {expected}"
            failures.append(f"{case_id}: {reason}")

        print(f"[{case_id}] Cross: {score_cross} | X: {score_x} "
              f"| 판정: {decision} | expected: {expected} | {status}")

    print_section(f"[3] 성능 분석 (MAC {REPEAT}회 평균)")
    print_performance_table([3, 5, 13, 25])

    print_section("[4] 결과 요약")
    print(f"전체 {len(patterns)}개 / 통과 {passed}개 / 실패 {len(failures)}개")
    for failure in failures:
        print(f"  - {failure}")


# 이 파일을 직접 실행했을 때의 시작점
if __name__ == "__main__":
    # 예외 ④: Ctrl+C(KeyboardInterrupt), 입력 끝(EOFError) → 안내 후 종료
    try:
        print("=== Mini NPU Simulator ===")
        mode = read_mode()
        if mode == "1":
            run_mode1()
        else:
            run_mode2()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
