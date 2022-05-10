def caller(c, j):
    def _caller(function):
        def wrapper(x, y):
            return function(c + x, j + y)

        return wrapper

    return _caller


@caller(c="100", j="200")
def a(x, y):
    print(f"{x} - {y}")


def a_old(x, y):
    print(f"{x} - {y}")


def caller_old(func, c, j):
    return lambda a, b: func(c + a, j + b)


if __name__ == "__main__":
    # no decorator
    f = caller_old(a_old, "100", "200")
    f("h", "z")

    # with decorator
    a("h", "z")
