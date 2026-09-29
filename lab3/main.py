# import matplotlib
# matplotlib.use('Agg')  # Set non-interactive backend before pyplot

import matplotlib.pyplot as plt
import numpy as np
import os

MESSAGE_STR = "You're all I ever needed, yeah"

def ascii_char_to_bin(char: str) -> str:
    """Converts a single ASCII character to an 8-bit binary string. 
    Assumes all valid ascii characters."""
    return format(ord(char), "08b")

def generate_x(length: int, step=1):
    x = list()
    if length < 0:
        return x
    x.append(0)

    curr_x=0
    while curr_x < length:
        curr_x += step;
        x.append(curr_x)
        x.append(curr_x)
    return x

MESSAGE_BIN = "".join(ascii_char_to_bin(char) for char in MESSAGE_STR)

# TODO: USE FULL MESSAGE. ONLY FOR TESTING
MESSAGE = MESSAGE_BIN

V_GLOBAL = 1;

# Unipolar NRZ
def gen_unipolar_scheme(message: str, V=1) -> tuple[list[int], list[int]]:
    """ Generates the x and y values for the plot of a
    Unipolar NRZ line encoding scheme. """
    if len(message) == 0:
        return [], []
    x = generate_x(len(message))[:-1]
    y = []
    for i in message:
        if i == "0":
            y.append(0)
            y.append(0)
        elif i == "1":
            y.append(V)
            y.append(V)

    return x, y

def generate_plots(plot_func, message: str, V=1, trun_len:int = 32):
    # --- I. First trunc_len bits with labels  ---
    message_trunc = message[:trun_len]
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    x, y = plot_func(message_trunc, V=V_GLOBAL)
    ax.plot(x, y, label="Unipolar NRZ", color="tab:blue")

    # Draw boundary lines for each bit
    for bit_boundary in range(0, len(message_trunc) + 1):
        ax.axvline(
            x=bit_boundary,
            linestyle="--",
            linewidth=0.6,
            color="gray",
            alpha=0.7,
        )

    # Set custom x-ticks at bit centers for clear labeling
    ax.set_xticks([i + 0.5 for i in range(len(message_trunc))])
    ax.set_xticklabels([str(b) for b in message_trunc])
    ax.set_xlabel("Bits")

    ax.set_ylabel("Voltage (V)")

    # Keep y-limits clean with slight padding
    ax.set_ylim(min(y) - 0.5, max(y) + 0.5)
    plt.tight_layout()

    # --- II. Full message with reduced layout ---
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    x, y = plot_func(MESSAGE, V=V_GLOBAL)
    ax.plot(x, y, label="Unipolar NRZ", color="tab:blue")

    # Draw boundary lines matched to actual voltage range
    for byte_boundary in range(0, len(message) + 1, 8):
        ax.axvline(
            x=byte_boundary,
            linestyle="--",
            linewidth=0.6,
            color="gray",
            alpha=0.7,
        )

    
    # --- Centered Byte Ticks ---
    BYTE_SIZE = 8

    # Group message into 8-bit chunks
    byte_chunks = [
        message[i : i + BYTE_SIZE]
        for i in range(0, len(message), BYTE_SIZE)
        ]

    # Calculate x-center for each byte chunk: 4.0, 12.0, 20.0, ...
    byte_tick_positions = [
        i * BYTE_SIZE + (len(chunk) / 2) for i, chunk in enumerate(byte_chunks)
        ]

    # Format labels as binary strings (e.g., "10110010")
    # byte_tick_labels = ["".join(map(str, chunk)) for chunk in byte_chunks]
    byte_tick_labels = [
    chr(int("".join(map(str, chunk)), 2)) for chunk in byte_chunks
    ]

    # Apply ticks and labels
    ax.set_xticks(byte_tick_positions)
    ax.set_xticklabels(byte_tick_labels, fontsize=8)  # Reduced font size to avoid overlap
    ax.set_xlabel("Bytes (8-bit blocks)")

    ax.set_ylabel("Voltage (V)")

    # Keep y-limits clean with slight padding
    ax.set_ylim(min(y) - 0.5, max(y) + 0.5)
    plt.tight_layout()

    plt.show()

generate_plots(gen_unipolar_scheme, MESSAGE, V=1)
