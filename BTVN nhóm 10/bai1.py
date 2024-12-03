import math
import concurrent.futures
import time

# Thuật toán kiểm tra số nguyên tố tuần tự
def is_prime_sequential(x):
    if x <= 1:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

# Thuật toán kiểm tra số nguyên tố song song
def is_prime_parallel(x):
    if x <= 1:
        return False

    def check_range(start, end):
        for i in range(start, end):
            if x % i == 0:
                return False
        return True

    num_threads = 4
    step = (int(math.sqrt(x)) + 1) // num_threads
    ranges = [(2 + i * step, 2 + (i + 1) * step) for i in range(num_threads)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_range, start, end) for start, end in ranges]
        for future in concurrent.futures.as_completed(futures):
            if not future.result():
                return False
    return True

# Nhập giá trị X từ người dùng
def get_input():
    try:
        x = int(input("Nhập số nguyên X để kiểm tra: "))
        return x
    except ValueError:
        print("Vui lòng nhập một số nguyên hợp lệ!")
        return None

# Kiểm tra thời gian với thuật toán tuần tự
def test_sequential(x):
    start_time = time.time()
    result = is_prime_sequential(x)
    end_time = time.time()
    print(f"X = {x} (Sequential) - Result: {result}, Time: {end_time - start_time:.5f} seconds")

# Kiểm tra thời gian với thuật toán song song
def test_parallel(x):
    start_time = time.time()
    result = is_prime_parallel(x)
    end_time = time.time()
    print(f"X = {x} (Parallel) - Result: {result}, Time: {end_time - start_time:.5f} seconds")

# Hàm chính
def main():
    x = get_input()
    if x is not None:
        # Chạy thử cả hai phương pháp
        test_sequential(x)
        test_parallel(x)

# Chạy chương trình
if __name__ == "__main__":
    main()
