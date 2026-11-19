# Mini NPU 시뮬레이터 (Codyssey 미션 E1-3)


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


def run_mode2():
    """모드 2: data.json 분석 (블록 C에서 구현)"""
    print("\n[모드 2] 아직 준비 중입니다.")


# 이 파일을 직접 실행했을 때의 시작점
if __name__ == "__main__":
    # 예외 ③: Ctrl+C(KeyboardInterrupt), 입력 끝(EOFError) → 안내 후 종료
    try:
        mode = read_mode()
        if mode == "1":
            run_mode1()
        else:
            run_mode2()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
