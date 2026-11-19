# Mini NPU 시뮬레이터 (Codyssey 미션 E1-3)


def read_matrix(name, n):
    """n x n 행렬을 한 줄씩 입력받아 2차원 list로 돌려준다."""
    print(f"\n[{name}] {n}x{n} 행렬을 한 줄씩 입력하세요.")
    matrix = []
    for i in range(n):
        text = input(f"  {i + 1}행: ")
        row = []
        for part in text.split():
            row.append(float(part))
        matrix.append(row)
    return matrix


def print_matrix(matrix):
    """행렬을 한 줄에 한 행씩 출력한다."""
    for row in matrix:
        print("  ", row)


# A-2: 필터 A, 필터 B, 패턴을 같은 함수로 입력받기
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
