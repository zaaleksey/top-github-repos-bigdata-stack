import time


def calc_exec_time(min=False):
    def _calc_exec_time(f):
        def wrapper(*args, **kwargs):
            print(f"Function name: {f.__name__}")
            start = time.time()
            result = f(*args, **kwargs)
            end = time.time()
            total = (end - start) / 60 if min else end - start
            units_of_time = "min." if min else "sec."
            print(f"Function execution time: {total} {units_of_time}\n")
            return result

        return wrapper

    return _calc_exec_time


@calc_exec_time()
def a(x, y):
    print(f"{x} - {y}")


@calc_exec_time(min=False)
def sequence_square(limit):
    return [x ** 10 for x in range(limit)]


@calc_exec_time(min=True)
def fibonacci(n):
    n -= 2
    fib1 = fib2 = 1
    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1
    return fib2


@calc_exec_time(min=True)
def fibonacci_rec(n):
    return _fibonacci_rec(n)


def _fibonacci_rec(n):
    if n in (1, 2):
        return 1
    return _fibonacci_rec(n - 1) + _fibonacci_rec(n - 2)


if __name__ == "__main__":
    a(10, 10)
    sequence_square(1_000_000)

    number = 5_000_000
    print(f"(loop) The {number} fibonacci number")
    fibonacci(number)

    print()

    number = 50
    print(f"(recursion) The {number} fibonacci number")
    fibonacci_rec(number)
