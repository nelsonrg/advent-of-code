from functools import reduce
from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# https://stackoverflow.com/a/72223195
def compose(*funcs):
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def read_input(fname):
    result = {}
    name = ""
    value_list = []
    with open(fname) as file:
        for line in file.readlines():
            if "seeds:" in line:
                result["seeds"] = [int(x) for x in line.split(":")[-1].split()]
            elif "map" in line:
                result[name] = value_list
                name = line.split()[0]
                value_list = []
            elif not line.strip():
                continue
            else:
                y = [int(x) for x in line.split()]
                if len(y) > 0:
                    value_list.append([int(x) for x in line.split()])
    result[name] = value_list
    return result


def pw_linear_factory(x, inverse=False):
    segments, functions = generate_functions(x, inverse)
    return lambda y: pw_linear(y, segments, functions)


def pw_linear(x, segments, functions):
    for s, f in zip(segments, functions):
        if x in s:
            return f(x)
    return x


def generate_functions(x, inverse=False):
    if inverse:
        segments = tuple(range(y[0], y[0]+y[2]) for y in x)
    else:
        segments = tuple(range(y[1], y[1]+y[2]) for y in x)

    def make_func(src, dest, inverse):
        if inverse:
            return lambda x: x - (dest - src)
        else:
            return lambda x: x + (dest - src)

    functions = tuple(make_func(y[1], y[0], inverse) for y in x)
    return segments, functions


def part_1(x):
    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    functions = tuple(map(pw_linear_factory, map(x.get, order)))
    locations = map(compose(*functions[::-1]), seeds)

    return min(locations)


def pw_linear_factory_ranges(x):
    segments, functions = generate_functions(x)
    return lambda y: pw_linear_ranges(y, segments, functions)


def pw_linear_ranges(x, segments, functions):
    def f(y):
        return pw_linear_range(y, segments, functions)[1]
    return list(chain(*[f(r) for r in x]))


def pw_linear_factory_range(x):
    segments, functions = generate_functions(x)
    return lambda y: pw_linear_range(y, segments, functions)


def pw_linear_range(x, segments, functions):
    breakpoints = [s.start for s in segments] + [s.stop for s in segments]
    interior_breakpoints = [b for b in breakpoints if b in x]
    exterior_breakpoints = [x.start, x.stop]
    output_breakpoints = list(set(interior_breakpoints + exterior_breakpoints))
    output_breakpoints.sort()
    output_edges = tuple(
        (start, stop) for start, stop in
        zip(output_breakpoints[::], output_breakpoints[1::])
    )

    def f(y):
        return pw_linear(y, segments, functions)

    input_ranges = [range(start, stop) for start, stop in output_edges]
    output_ranges = [range(f(start), f(stop-1)+1) for start, stop in output_edges]
    return input_ranges, output_ranges


def part_2(x, plot=False, animate=False):
    if plot:
        plot_seeds(x)
        plot_seeds2(x)
    if animate:
        animate_seeds(x)

    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    initial_ranges = [range(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])]

    functions = tuple(map(pw_linear_factory_ranges, map(x.get, order)))
    output_ranges = compose(*functions[::-1])(initial_ranges)

    return min(r.start for r in output_ranges)


def plot_seeds(x):
    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    initial_ranges = [range(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])]

    functions = tuple(pw_linear_factory_range(x[step]) for step in order)
    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    plt.tight_layout()
    axs = axs.flatten()
    axs[-1].set_axis_off()
    axs[0].axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
    axs[0].set(xlabel="seed",
               ylabel="seed")
    for r in initial_ranges:
        axs[0].plot([r.start, r.stop], [r.start, r.stop], 'k-')
    input_ranges = initial_ranges
    for i, f in enumerate(functions):
        out_ranges = []
        axs[i+1].axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
        axs[i+1].set(xlabel=order[i].split("-")[0],
                     ylabel=order[i].split("-")[-1])
        for input_range in input_ranges:
            in_r, out_r = f(input_range)
            for in_rr, out_rr in zip(in_r, out_r):
                if in_rr == out_rr:
                    c = "black"
                else:
                    c = "red"
                axs[i+1].plot(
                    [in_rr.start, in_rr.stop],
                    [out_rr.start, out_rr.stop],
                    color=c, linestyle="solid"
                )
            out_ranges.append(out_r)
        input_ranges = list(chain(*out_ranges))


def plot_seeds2(x):
    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    initial_ranges = [range(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])]
    functions = tuple(pw_linear_factory_ranges(x[step]) for step in order)
    inverse_functions = tuple(pw_linear_factory(x[step], inverse=True) for step in order)

    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    plt.tight_layout()
    axs = axs.flatten()
    axs[-1].set_axis_off()
    axs[0].axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
    axs[0].set(xlabel="seed",
               ylabel="seed")
    for r in initial_ranges:
        axs[0].plot([r.start, r.stop], [r.start, r.stop], 'k-')

    for j in range(len(functions)):
        if j == 0:
            output_ranges = functions[0](initial_ranges)
        else:
            output_ranges = compose(*(functions[:(j+1)][::-1]))(initial_ranges)
        axs[j+1].axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
        axs[j+1].set(xlabel="seed",
                     ylabel=order[j].split("-")[-1])
        print(j, output_ranges)
        for out_r in output_ranges:
            if j == 0:
                inp_start = inverse_functions[0](out_r.start)
                inp_end = inverse_functions[0](out_r.stop-1)+1
            else:
                inp_start = compose(*(inverse_functions[:(j+1)]))(out_r.start)
                inp_end = compose(*(inverse_functions[:(j+1)]))(out_r.stop-1)+1
            print((inp_start, inp_end), (out_r.start, out_r.stop))
            axs[j+1].plot(
                [inp_start, inp_end],
                [out_r.start, out_r.stop],
                color="red", linestyle="solid"
            )


def animate_seeds(x):
    seeds = x["seeds"]

    order = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water",
             "water-to-light", "light-to-temperature", "temperature-to-humidity",
             "humidity-to-location"]

    initial_ranges = [range(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])]
    functions = tuple(pw_linear_factory_ranges(x[step]) for step in order)
    inverse_functions = tuple(pw_linear_factory(x[step], inverse=True) for step in order)

    output_ranges = compose(*functions[::-1])(initial_ranges)
    max_value = max(r.stop for r in output_ranges)*1.2

    # now animate
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    plt.tight_layout()
    ax.axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
    ax.set(xlabel="seed",
           ylabel="seed",
           ylim=[0, max_value])
    for r in initial_ranges:
        ax.plot([r.start, r.stop], [r.start, r.stop], 'k.-')

    delta_steps = 3

    def update(k):
        i = k // (len(functions)*delta_steps)
        j = k % (len(functions)*delta_steps)

        # clear the axis each frame
        ax.clear()

        # replot things
        ax.axline((0, 0), slope=1, color="lightgray", linestyle="dashed")
        ax.set(xlabel="seeds",
               ylabel=order[i].split("-")[-1],
               ylim=[0, max_value])
        plt.tight_layout()

        if i == 0:
            last_output_ranges = initial_ranges
            output_ranges = functions[0](initial_ranges)
        else:
            last_output_ranges = compose(*(functions[:(i)][::-1]))(initial_ranges)
            output_ranges = compose(*(functions[:(i+1)][::-1]))(initial_ranges)

        # old lines
        if i > 0:
            for l_out_r in last_output_ranges:
                if i == 1:
                    inp_start = inverse_functions[0](l_out_r.start)
                    inp_stop = inverse_functions[0](l_out_r.stop-1)+1
                else:
                    inp_start = compose(*(inverse_functions[:(i)]))(l_out_r.start)
                    inp_stop = compose(*(inverse_functions[:(i)]))(l_out_r.stop-1)+1
                ax.plot(
                    [inp_start, inp_stop],
                    [l_out_r.start, l_out_r.stop],
                    color="gray", linestyle="solid",
                    alpha=1-j/(delta_steps*len(functions)-1)
                )

        # new lines
        for out_r in output_ranges:
            if i == 0:
                inp_start = inverse_functions[0](out_r.start)
                inp_stop = inverse_functions[0](out_r.stop-1)+1
                last_start = inp_start
                last_stop = inp_stop
            else:
                inp_start = compose(*(inverse_functions[:(i+1)]))(out_r.start)
                inp_stop = compose(*(inverse_functions[:(i+1)]))(out_r.stop-1)+1
                last_start = inverse_functions[i](out_r.start)
                last_stop = inverse_functions[i](out_r.stop-1)+1
            ax.plot(
                [inp_start, inp_stop],
                [last_start+(out_r.start-last_start)*j/(delta_steps*len(functions)-1),
                 last_stop+(out_r.stop-last_stop)*j/(delta_steps*len(functions)-1)],
                color="red", linestyle="solid"
            )

    ani = animation.FuncAnimation(
        fig, update,
        frames=len(order)**2*delta_steps, interval=100, repeat=False
    )
    ani.save("animation.mp4", writer="ffmpeg", dpi=300)
    plt.show()


if __name__ == "__main__":
    print("Part 1 test:", part_1(read_input("test.txt")))
    print("Part 1:", part_1(read_input("input.txt")))
    print()
    print("Part 2 test:", part_2(read_input("test.txt")))
    print("Part 2:", part_2(read_input("input.txt"), plot=False, animate=False))
    plt.show()
