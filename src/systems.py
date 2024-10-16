"""
Module responsible for simulating interesting system types. We support four
systems
- direct delivery with full participation,
- broadcast,
- k-broadcast with dropped messages, and
- k-broadcast with deferred messages.

For each, given a dataframe, interval, and other parameters, it computes
- overhead, which is the fraction of dummy messages to delivered messages,
- latency, which is the difference in rounds, between when a message is
submitted and when it is sent, and
- dropped, which is the fraction of dropped messages to submitted messages.
"""

import numpy as np

import src.rounds
import src.utils
import src.stats
import src.k_fns

LATENCY = 0
OVERHEAD = 1

SIG_FIGS = 2


def broadcast(interval, df):
    """
    Computes statistics for broadcast.

    Returns overhead, latency, median traffic, maximum traffic.
    """

    sort_idx = src.utils.sort_receiver(df)
    df = df[sort_idx]
    num_users = src.utils.num_users(df)

    # Latencies
    start = np.min(src.utils.submits(df))
    message_rounds = src.rounds.round_submitted(
        src.utils.submits(df),
        start,
        interval
    )
    message_delivers = src.rounds.round_end(message_rounds, start, interval)
    latencies = message_delivers - src.utils.submits(df)

    # Overheads
    round_messages = src.rounds.messages_per_round(
        message_rounds,
        np.unique(message_rounds)
    )

    return {
        "latencies": latencies.tolist(),
        "round_messages": round_messages.tolist(),
        "users": src.utils.receivers(df).tolist(),
        "num_users": num_users,
    }


def deferred(interval, users, start, submits, k):

    start = np.min(submits)

    send_rounds = src.rounds.round_deferred(users, submits, start, interval, k)
    sends = src.rounds.round_end(send_rounds, start, interval)
    latencies = sends - submits

    num_rounds = np.max(send_rounds) - np.min(send_rounds) + 1

    avg_latency = src.stats.avg_latency(latencies)

    system_bandwidth = np.sum(k)
    user_bandwidth = np.average(k)
    total_overhead = src.stats.system_avg_overhead(k, num_rounds, len(sends))
    overhead_per_user_round = total_overhead / (len(k) * num_rounds)
    return (avg_latency, system_bandwidth, user_bandwidth, total_overhead, overhead_per_user_round)


# def search_overhead(stats_fn, initial_k, target_overhead):
#     min_c = 0.0
#     max_c = 2.0
#     print(target_overhead)

#     prev_sum_k = -1
#     while True:
#         c = (min_c + max_c) / 2
#         k = np.ceil(c * initial_k)
#         sum_k = np.sum(k)
#         print(f"{c}: {sum_k}")

#         if sum_k <= target_overhead and sum_k - prev_sum_k == 0:
#             break
#         else:
#             prev_sum_k = sum_k
#             if sum_k > target_overhead:
#                 max_c = c
#             else:
#                 min_c = c

#     stats = stats_fn(k)
#     print(stats)

#     return stats


# def search_latency(stats_fn, initial_k, target_latency):

#     max_c = 1.0
#     min_c = 0.0

#     prev_overhead = -1
#     while True:
#         c = (min_c + max_c)/2
#         stats = stats_fn(np.ceil(c * initial_k))
#         latency = stats[LATENCY]
#         overhead = stats[OVERHEAD]

#         print(f"{c}: {overhead}, {latency}")
#         overhead = src.utils.round_sigfigs(overhead, 2)

#         if abs(prev_overhead - overhead) == 0 and abs(target_latency - src.utils.round_sigfigs(latency)):
#             break
#         else:
#             prev_overhead = overhead
#             if latency > target_latency:
#                 min_c = c
#             else:
#                 max_c = c

#     return stats


# def k_in(interval, df, k):
#     """
#     Computes statistics for direct delivery with full participation.

#     Input: interval, df
#     Output: overhead, latency, dropped.
#     """

#     # sort_idx = src.utils.sort_sender(df)
#     # df = df[sort_idx]
#     senders = src.utils.senders(df)
#     submits = src.utils.submits(df)
#     start = np.min(submits)

#     return deferred(interval, senders, start, submits, k)


# def k_out(interval, df, k):
#     """
#     Computes statistics for k-retrieval, where messages are deferred.

#     Returns overhead, latency, dropped.
#     """

#     # sort_idx = src.utils.sort_receiver(df)
#     # df = df[sort_idx]
#     receivers = src.utils.receivers(df)
#     submits = src.utils.submits(df)
#     start = np.min(submits)

#     return deferred(interval, receivers, start, submits, k)


def k_in_prep(df):
    sort_idx = src.utils.sort_sender(df)
    df = df[sort_idx]
    users = src.utils.senders(df)
    submits = src.utils.submits(df)
    start = np.min(submits)

    return (users, submits, start)


def k_out_prep(df):
    sort_idx = src.utils.sort_receiver(df)
    df = df[sort_idx]
    users = src.utils.receivers(df)
    submits = src.utils.submits(df)
    start = np.min(submits)

    return (users, submits, start)

#   user_num_messages = src.k_fns.user_num_messages(receivers, num_users)

#    if variable_k:
#         initial_k = user_num_messages
#     else:
#         initial_k = src.k_fns.k(np.max(user_num_messages), num_users)

#     def stats_fn(k):

#     if latency_or_overhead:
#         return search_latency(stats_fn, initial_k, target)
#     else:
#         return search_overhead(stats_fn, initial_k, target * num_users)


def one_per_round(interval, df, k):

    submits = np.sort(src.utils.submits(df))
    users = np.zeros(df.shape[0], dtype=int)

    return deferred(interval, users, submits, 1, int(k), False)
