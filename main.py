# Mini NPU 시뮬레이터 (Codyssey 미션 E1-3)


def read_matrix(name, n):
    """n x n 행렬을 한 줄씩 입력받아 2차원 list로 돌려준다."""
    print(f"\n[{name}] {n}x{n} 행렬을 한 줄씩 입력하세요.")
    matrix = []
    while len(matrix) < n:  # n줄이 다 찰 때까지 반복
        text = input(f"  {len(matrix) + 1}행: ")
        row = []

        # 예외 ①: 숫자로 바꿀 수 없는 값 (예: abc)
        try:
            for part in text.split():
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


# 모드 1 흐름: 필터 A·B 입력 → 저장 확인 → 패턴 입력
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
