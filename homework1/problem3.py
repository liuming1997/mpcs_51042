"""
MPCS 51042 Assignment 1
Problem 3
Ming Liu
"""

def newton(f, f_pr, x_0, tol, max_iter):
    # try:
        # calculate x(n+1)
    approx = x_0 - f(x_0)/f_pr(x_0)
    # if it's getting that small, just stop it somehow
    # except ZeroDivisionError:
        # approx = x_0
    if abs(approx - x_0) < tol:
        return approx
    elif max_iter == 0:
        return approx
    else:
        return newton(f, f_pr, approx, tol, (max_iter - 1))

def f(x):
    return (x) ** 2 - 4
    
def f_pr(x):
    return 2*(x)

def main():
    print(newton(f, f_pr, -1, 1e-16, 2))
    print(newton(f, f_pr, -1, 1e-16, 1000))
    print(newton(f, f_pr, 1, 1e-16, 1000))
    print(newton(f, f_pr, 3, 1e-16, 1000))


if __name__ == "__main__":
    main()