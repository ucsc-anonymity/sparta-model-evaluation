import argparse
import os
import json
import matplotlib.pyplot as plt
import numpy as np

import src.stats

FONT_SIZE = 24
LINE_WIDTH = 4
MSG_SIZE = 128
MSG_TO_MB = MSG_SIZE / 1000000

ESTIMATE = 0
SYS_BANDWIDTH = 2
USR_BANDWIDTH = 3

# plt.rcParams['text.usetex'] = True


def system_round_bandwidth_fig(
    dataset, out_path,
    b_data, b_label,
    # one_in_data, one_in_label,
    kin_data, kin_label,
    ksin_data, ksin_label,
    # one_out_data, one_out_label,
    kout_data, kout_label,
    ksout_data, ksout_label
):
    fig, ax = plt.subplots()

    b = np.array(src.stats.broadcast_round_bandwidth(
        b_data["num_users"],
        np.array(b_data["round_messages"]),
    )) * MSG_TO_MB
    ax.plot(list(range(len(b))), b, label=b_label)

    kin = np.array(src.stats.system_round_bandwidth(
        kin_data["num_rounds"],
        np.array(kin_data["user_bandwidth"]),
    )) * MSG_TO_MB
    ax.plot(list(range(len(kin))), kin, label=kin_label)

    ksin = np.array(src.stats.system_round_bandwidth(
        ksin_data["num_rounds"],
        np.array(ksin_data["user_bandwidth"]),
    )) * MSG_TO_MB
    ax.plot(list(range(len(ksin))), ksin, label=ksin_label)

    kout = np.array(src.stats.system_round_bandwidth(
        kout_data["num_rounds"],
        np.array(kout_data["user_bandwidth"]),
    )) * MSG_TO_MB
    ax.plot(list(range(len(kout))), kout, label=kout_label)

    ksout = np.array(src.stats.system_round_bandwidth(
        ksout_data["num_rounds"],
        np.array(ksout_data["user_bandwidth"]),
    )) * MSG_TO_MB
    ax.plot(list(range(len(ksout))), ksout, label=ksout_label)

    ax.set_yscale("log")
    ax.set_ylabel("Traffic Rate (MB/min.)")
    ax.set_xlabel("Rounds")
    ax.legend(loc="upper left")

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(out_path, format="pdf")


def latency_fig(
    dataset, out_path,
    b_data, b_label,
    # one_in_data, one_in_label,
    kin_data, kin_label,
    ksin_data, ksin_label,
    # one_out_data, one_out_label,
    kout_data, kout_label,
    ksout_data, ksout_label
):
    fig, ax = plt.subplots()

    b = np.array(sorted(b_data["latencies"]))
    ax.plot(list(range(len(b))), b, label=b_label)

    kin = np.array(sorted(kin_data["latencies"]))
    ax.plot(list(range(len(kin))), kin, label=kin_label)

    ksin = np.array(sorted(ksin_data["latencies"]))
    ax.plot(list(range(len(ksin))), ksin, label=ksin_label)

    kout = np.array(sorted(kout_data["latencies"]))
    ax.plot(list(range(len(kout))), kout, label=kout_label)

    ksout = np.array(sorted(ksout_data["latencies"]))
    ax.plot(list(range(len(ksout))), ksout, label=ksout_label)

    ax.set_yscale("log")
    ax.set_ylabel("Latency (sec.)")
    ax.set_xlabel("Users")
    ax.legend(loc="upper left")

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(out_path, format="pdf")


def user_peak_latency_fig(
    dataset, out_path,
    b_data, b_label,
    # one_in_data, one_in_label,
    kin_data, kin_label,
    ksin_data, ksin_label,
    # one_out_data, one_out_label,
    kout_data, kout_label,
    ksout_data, ksout_label
):
    fig, ax = plt.subplots()

    b = np.array(sorted(src.stats.avg_user_latency(
        b_data["latencies"],
        b_data["users"],
        b_data["num_users"],
    )))
    ax.plot(list(range(len(b))), b, label=b_label)

    kin = np.array(sorted(src.stats.avg_user_latency(
        kin_data["latencies"],
        kin_data["users"],
        kin_data["num_users"]
    )))
    ax.plot(list(range(len(kin))), kin, label=kin_label)

    ksin = np.array(sorted(src.stats.avg_user_latency(
        ksin_data["latencies"],
        ksin_data["users"],
        ksin_data["num_users"],
    )))
    ax.plot(list(range(len(ksin))), ksin, label=ksin_label)

    kout = np.array(sorted(src.stats.avg_user_latency(
        kout_data["latencies"],
        kout_data["users"],
        kout_data["num_users"],
    )))
    ax.plot(list(range(len(kout))), kout, label=kout_label)

    ksout = np.array(sorted(src.stats.peak_user_latency(
        ksout_data["latencies"],
        ksout_data["users"],
        ksout_data["num_users"],
    )))
    ax.plot(list(range(len(ksout))), ksout, label=ksout_label)

    ax.set_yscale("log")
    ax.set_ylabel("Latency (sec.)")
    ax.set_xlabel("Users")
    ax.legend(loc="upper left")

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(out_path, format="pdf")


def user_peak_bandwidth_fig(
    dataset, out_path,
    b_data, b_label,
    # one_in_data, one_in_label,
    kin_data, kin_label,
    ksin_data, ksin_label,
    # one_out_data, one_out_label,
    kout_data, kout_label,
    ksout_data, ksout_label
):
    fig, ax = plt.subplots()

    b = np.array(sorted(src.stats.broadcast_peak_user_bandwidth(
        b_data["round_messages"],
        b_data["num_users"],
    ))) * MSG_SIZE
    ax.plot(list(range(len(b))), b, label=b_label)

    kin = np.array(sorted(src.stats.system_peak_user_bandwidth(
        kin_data["user_bandwidth"]
    ))) * MSG_SIZE
    ax.plot(list(range(len(kin))), kin, label=kin_label)

    ksin = np.array(sorted(src.stats.system_peak_user_bandwidth(
        ksin_data["user_bandwidth"]
    ))) * MSG_SIZE
    ax.plot(list(range(len(ksin))), ksin, label=ksin_label)

    kout = np.array(sorted(src.stats.system_peak_user_bandwidth(
        kout_data["user_bandwidth"]
    ))) * MSG_SIZE
    ax.plot(list(range(len(kout))), kout, label=kout_label)

    ksout = np.array(sorted(src.stats.system_peak_user_bandwidth(
        ksout_data["user_bandwidth"]
    ))) * MSG_SIZE
    ax.plot(list(range(len(ksout))), ksout, label=ksout_label)

    ax.set_yscale("log")
    ax.set_ylabel("Traffic Rate per User (b / min)")
    ax.set_xlabel("Users")
    ax.legend(loc="upper right")

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.savefig(out_path, format="pdf")


def avg_fig(
    dataset, out_path,
    b_data, b_label,
    # one_in_data, one_in_label,
    kin_data, kin_label,
    ksin_data, ksin_label,
    # one_out_data, one_out_label,
    kout_data, kout_label,
    ksout_data, ksout_label
):
    s = ""
    s += f"{b_label}\n"
    s += f"\tavg latency: {src.stats.avg_latency(b_data['latencies'])}\n"
    s += f"\tmed latency: {src.stats.med_latency(b_data['latencies'])}\n"
    s += f"\tavg overhead: {src.stats.broadcast_avg_overhead(b_data['num_users'])}\n"

    s += f"{kin_label}\n"
    s += f"\tavg latency: {src.stats.avg_latency(kin_data['latencies'])}\n"
    s += f"\tmed latency: {src.stats.med_latency(kin_data['latencies'])}\n"
    o = src.stats.system_avg_overhead(
        kin_data['user_bandwidth'],
        kin_data['num_rounds'],
        kin_data['num_real'],
    )
    s += f"\tavg overhead: {o}\n"

    s += f"{ksin_label}\n"
    s += f"\tavg latency: {src.stats.avg_latency(ksin_data['latencies'])}\n"
    s += f"\tmed latency: {src.stats.med_latency(ksin_data['latencies'])}\n"
    o = src.stats.system_avg_overhead(
        ksin_data['user_bandwidth'],
        ksin_data['num_rounds'],
        ksin_data['num_real'],
    )
    s += f"\tavg overhead: {o}\n"

    # print(kin_label)
    # print("\tavg latency:", src.stats.avg_latency(kin_data["latencies"]))
    # print("\tmed latency:", src.stats.med_latency(kin_data["latencies"]))
    # print("\tavg overhead:", src.stats.system_avg_overhead(
    #     kin_data["user_bandwidth"],
    #     kin_data["num_rounds"],
    #     kin_data["num_real"],
    # ))

    # print(ksin_label)
    # print("\tavg latency:", src.stats.avg_latency(ksin_data["latencies"]))
    # print("\tmed latency:", src.stats.med_latency(ksin_data["latencies"]))
    # print("\tavg overhead:", src.stats.system_avg_overhead(
    #     ksin_data["user_bandwidth"],
    #     ksin_data["num_rounds"],
    #     ksin_data["num_real"],
    # ))

    # print(one_out_label)
    # print("\tavg latency:", src.stats.avg_latency(one_out_data["latencies"]))
    # print("\tmed latency:", src.stats.med_latency(one_out_data["latencies"]))
    # print("\tavg overhead:", src.stats.system_avg_overhead(
    #     one_out_data["user_bandwidth"],
    #     one_out_data["num_rounds"],
    #     one_out_data["num_real"],
    # ))

    s += f"{kout_label}\n"
    s += f"\tavg latency: {src.stats.avg_latency(kout_data['latencies'])}\n"
    s += f"\tmed latency: {src.stats.med_latency(kout_data['latencies'])}\n"
    o = src.stats.system_avg_overhead(
        kout_data['user_bandwidth'],
        kout_data['num_rounds'],
        kout_data['num_real'],
    )
    s += f"\tavg overhead: {o}\n"

    # print(kout_label)
    # print("\tavg latency:", src.stats.avg_latency(kout_data["latencies"]))
    # print("\tmed latency:", src.stats.med_latency(kout_data["latencies"]))
    # print("\tavg overhead:", src.stats.system_avg_overhead(
    #     kout_data["user_bandwidth"],
    #     kout_data["num_rounds"],
    #     kout_data["num_real"],
    # ))

    s += f"{ksout_label}\n"
    s += f"\tavg latency: {src.stats.avg_latency(ksout_data['latencies'])}\n"
    s += f"\tmed latency: {src.stats.med_latency(ksout_data['latencies'])}\n"
    o = src.stats.system_avg_overhead(
        ksout_data['user_bandwidth'],
        ksout_data['num_rounds'],
        ksout_data['num_real'],
    )
    s += f"\tavg overhead: {o}\n"

  # print(ksout_label)
  # print("\tavg latency:", src.stats.avg_latency(ksout_data["latencies"]))
  # print("\tmed latency:", src.stats.med_latency(ksout_data["latencies"]))
  # print("\tavg overhead:", src.stats.system_avg_overhead(
  #     ksout_data["user_bandwidth"],
  #     ksout_data["num_rounds"],
  #     ksout_data["num_real"],
  # ))

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(out_path, "w") as f:
        f.write(s)


def read_data(in_path, dataset, interval, name):
    path = os.path.join(in_path, dataset, interval, f"{name}.csv")
    data = np.genfromtxt(path, delimiter='\t', skip_header=1)
    print(data.shape)
    if len(data.shape) == 1:
        data = data.reshape(1, -1)
    return data[:, [ESTIMATE, SYS_BANDWIDTH, USR_BANDWIDTH]]


def system_bandwidth_fig(x, y, outmax, inmax):
    plt.plot(x, y, label="$k^*_{out}$")
    plt.plot(x, outmax, label="$k_{out}$")
    plt.plot(x, inmax, label="$k_{in}$")

    plt.yscale("log")
    plt.xscale("log")
    plt.xticks()
    plt.legend()
    plt.show()


def user_bandwidth_fig(x, y, outmax, inmax, interval):
    plt.plot(x, MSG_SIZE / interval * y,
             label="$k^*_{out}$", linewidth=LINE_WIDTH)
    plt.plot(x, MSG_SIZE / interval * outmax,
             label="$k_{out}$", linewidth=LINE_WIDTH)
    plt.plot(x, MSG_SIZE / interval * inmax,
             label="$k_{in}$", linewidth=LINE_WIDTH)

    ax = plt.gca()

    # Set the line width for the axes
    for spine in ax.spines.values():
        spine.set_linewidth(LINE_WIDTH)

    plt.yscale("log")
    plt.xscale("log")
    plt.yticks(fontsize=18)
    plt.xticks(x, labels=[f"${i}$" for i in x], fontsize=18)
    plt.xlabel("Estimate Factor (log)", fontweight="bold", fontsize=24)
    plt.ylabel("User Bandwidth (B/s)",
               fontweight="bold", fontsize=24)
    plt.tight_layout()
    plt.legend(fontsize="xx-large")
    plt.savefig("enron.pdf", format="pdf")
    plt.show()


def main(in_path, out_path, dataset, interval):
    k_out = "k-out*"
    k_out_100 = "k-out-100"
    k_in_100 = "k-in-100"

    k_out_data = read_data(in_path, dataset, interval, k_out)
    k_out_100_data = read_data(in_path, dataset, interval, k_out_100)
    k_in_100_data = read_data(in_path, dataset, interval, k_in_100)

    # x = k_out_data[:, 0].flatten()
    x = [2**i for i in range(0, 10)]
    sys_out_y = k_out_data[:, 1].flatten()
    sys_out_100_y = np.full(len(x), k_out_100_data[:, 1])
    sys_in_100_y = np.full(len(x), k_in_100_data[:, 1])

    usr_out_y = k_out_data[:, 2].flatten()
    print(usr_out_y)
    usr_out_100_y = np.full(usr_out_y.shape, k_out_100_data[:, 2].flatten())
    print(usr_out_100_y)
    usr_in_100_y = np.full(usr_out_y.shape, k_in_100_data[:, 2].flatten())
    print(usr_in_100_y)

    # system_bandwidth_fig(x, sys_out_y, sys_out_100_y, sys_in_100_y)
    user_bandwidth_fig(x, usr_out_y, usr_out_100_y,
                       usr_in_100_y, float(interval))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Simulator",
        description="""
                    This builds the figures.
                    """
    )

    parser.add_argument("inpath", type=str, help="Path to data.")
    parser.add_argument("outpath", type=str, help="Path to figs.")
    parser.add_argument("dataset", type=str, help="Dataset to use.")
    parser.add_argument("interval", type=str)

    args = parser.parse_args()
    in_path = os.path.abspath(args.inpath)
    out_path = os.path.abspath(args.outpath)

    main(in_path, out_path, args.dataset, args.interval)
