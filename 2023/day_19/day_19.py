from functools import reduce
import operator
import copy


def read_input(fname):
    workflows = {}
    ratings = []
    is_workflow = True
    is_rating = False
    with open(fname) as file:
        for line in file.readlines():
            x = line.strip()
            if len(x) == 0:
                is_workflow = False
                is_rating = True
                continue
            if is_workflow:
                name, body = x.split("{")
                body = body.strip("{}")  # remove trailing }
                body = [b.split(":") for b in body.split(",")]
                workflows[name] = body
            if is_rating:
                rating = x.strip("{}").split(",")
                rating = [r.split("=") for r in rating]
                rating = {r[0]: int(r[1]) for r in rating}
                ratings.append(rating)
    return workflows, ratings


def run_workflow(workflows, workflow, rating):
    if workflow == "R":
        return 0
    elif workflow == "A":
        return 1

    for w in workflows[workflow]:
        if len(w) == 2:
            category = w[0][0]
            cond = str(rating[category]) + w[0][1:]
            next_workflow = w[1]
            if eval(cond):
                return run_workflow(workflows, next_workflow, rating)
        else:
            return run_workflow(workflows, w[0], rating)


def split_range(r, relation, point):
    left, right = None, None
    true_branch, false_branch = None, None
    if point < r.start:
        right = r
    elif point >= r.stop:
        left = r
    else:
        if relation == "<":
            left = range(r.start, point)
            right = range(point, r.stop)
        elif relation == ">":
            left = range(r.start, point+1)
            right = range(point+1, r.stop)
    if relation == "<":
        true_branch = left
        false_branch = right
    elif relation == ">":
        true_branch = right
        false_branch = left
    else:
        raise ValueError(f"Unknown condition {relation}")
    return true_branch, false_branch


def run_workflow2(workflows, workflow, rating, total):
    if workflow == "A":
        total.append(reduce(operator.mul, [len(r) for r in rating.values()]))
        return 0
    elif workflow == "R":
        return 0

    for w in workflows[workflow]:
        if len(w) == 2:
            category = w[0][0]
            cond = w[0]
            if "<" in cond:
                relation = "<"
            elif ">" in cond:
                relation = ">"
            point = int(cond.split(relation)[1])
            r = rating[category]
            true_range, false_range = split_range(r, relation, point)
            next_workflow = w[1]
            next_rating = copy.deepcopy(rating)
            next_rating[category] = true_range
            rating[category] = false_range
            run_workflow2(workflows, next_workflow, next_rating, total)
        else:
            return run_workflow2(workflows, w[0], rating, total)


def part_1(workflows, ratings):
    accumulator = 0
    for r in ratings:
        accumulator += run_workflow(workflows, "in", r)*sum(r.values())
    return accumulator


def part_2(workflows, ratings):
    accumulator = []
    ratings = {
        "x": range(1, 4001),
        "m": range(1, 4001),
        "a": range(1, 4001),
        "s": range(1, 4001)
    }
    run_workflow2(workflows, "in", ratings, accumulator)
    return sum(accumulator)


if __name__ == "__main__":
    print("Part 1 test:", part_1(*read_input("test.txt")))
    print("Part 1:", part_1(*read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(*read_input("test.txt")))
    print("Part 2:", part_2(*read_input("input.txt")))
