import random
import time
from multiprocessing import Pool, cpu_count

# Hàm sinh ma trận ngẫu nhiên
def generate_matrix(rows, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]

# Hàm nhân ma trận tuần tự
def multiply_matrices_sequential(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Hàm tính toán một phần của ma trận (hỗ trợ song song)
def compute_chunk(args):
    A, B, start_row, end_row = args
    cols_B = len(B[0])
    cols_A = len(A[0])
    C_chunk = []
    for i in range(start_row, end_row):
        row = []
        for j in range(cols_B):
            value = sum(A[i][k] * B[k][j] for k in range(cols_A))
            row.append(value)
        C_chunk.append(row)
    return C_chunk

# Hàm nhân ma trận song song
def multiply_matrices_parallel(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    num_processes = cpu_count()
    chunk_size = rows_A // num_processes
    ranges = [(A, B, i, min(i + chunk_size, rows_A)) for i in range(0, rows_A, chunk_size)]

    with Pool(num_processes) as pool:
        results = pool.map(compute_chunk, ranges)

    # Ghép các kết quả lại thành ma trận cuối
    return [row for chunk in results for row in chunk]

# Hàm so sánh và đo thời gian
def main():
    # Sinh ma trận kích thước 400 × 400
    test_cases = [10, 30, 50, 100, 300, 500]
    for size in test_cases:
        A = generate_matrix(size, size)
        B = generate_matrix(size, size)

        print(f"Testing with {size} × {size} matrices")

        # Thực hiện tuần tự
        start_time = time.time()
        result_seq = multiply_matrices_sequential(A, B)
        seq_time = time.time() - start_time
        print(f"Tuan tu: Time = {seq_time:.6f}s")

        # Thực hiện song song
        start_time = time.time()
        result_par = multiply_matrices_parallel(A, B)
        par_time = time.time() - start_time
        print(f"Song song: Time = {par_time:.6f}s")

        print(f"Toi uu thoi gian: {seq_time / par_time:.2f}x")

if __name__ == "__main__":
    main()
