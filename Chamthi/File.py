import os
import random

problem_name = "CAU3"
num_tests = 10

for i in range(1, num_tests + 1):
    folder = f"test{i:02}"
    os.makedirs(folder, exist_ok=True)

    a = random.randint(1, 10**5)
    b = random.randint(1, 10**5)

    with open(os.path.join(folder, f"{problem_name}.inp"), "w") as f_inp:
        f_inp.write(f"{a} {b}\n")

    with open(os.path.join(folder, f"{problem_name}.out"), "w") as f_out:
        f_out.write(str(a + b))
