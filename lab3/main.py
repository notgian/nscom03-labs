import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before pyplot

import matplotlib.pyplot as plt
import shutil
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

V_GLOBAL = 1;

# Unipolar NRZ
def unipolar_scheme(message: str, V=1) -> tuple[list[int], list[int]]:
    """ Generates the x and y values for the plot of a
    Unipolar NRZ line encoding scheme. The Volatage V is
    the peak-to-peak voltage. """
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

def polar_nrz_l_scheme(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Polar NRZ-L line encoding scheme. The Volatage V is
    the peak-to-peak voltage. """
    peak_pos = V * 0.5
    peak_neg = -V * 0.5
    if len(message) == 0:
        return [], []
    x = generate_x(len(message))[:-1]
    y = []
    for i in message:
        if i == "0":
            y.append(peak_pos)
            y.append(peak_pos)
        elif i == "1":
            y.append(peak_neg)
            y.append(peak_neg)
    return x, y


def polar_nrz_i_scheme(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Polar NRZ-I line encoding scheme. The Volatage V is
    the peak-to-peak voltage. """

    if len(message) == 0:
        return [], []
    peak = V * 0.5
    x = [0] + generate_x(len(message))[:-1]

    y = [peak]
    current_level = y[-1]

    for i in message:
        # invert signal if bit is 1
        if i == "1":
            current_level = -current_level

        y.append(current_level)
        y.append(current_level)

    return x, y

def polar_rz_scheme(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Polar RZ line encoding scheme. The Volatage V is
    the peak-to-peak voltage. """
    if len(message) == 0:
        return [], []
    peak = V * 0.5
    x = generate_x(len(message), step=0.5)[:-1]
    y = []
    for i in message:
        if i == "0":
            y += [-peak, -peak, 0, 0]
        elif i == "1":
            y += [peak, peak, 0, 0]
    return x, y

def bipolar_manchester(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Bipolar Manchester line encoding scheme. The Volatage V 
    is the peak-to-peak voltage. """
    if len(message) == 0:
        return [], []
    peak = V * 0.5
    x = generate_x(len(message), step=0.5)[:-1]
    y = []
    for i in message:
        if i == "0":
            y += [peak, peak, -peak, -peak]
        elif i == "1":
            y += [-peak, -peak, peak, peak]
    return x, y

def bipolar_differential_manchester(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Bipolar Differential Manchester line encoding scheme. 
    The Volatage V is the peak-to-peak voltage. """

    if len(message) == 0:
        return [], []

    peak = V * 0.5
    x = [0] + generate_x(len(message), step = 0.5)[:-1]

    y = [peak]

    for i in message:
        current_level = y[-1]
        # invert signal if bit is 0
        if i == "0":
            current_level = -current_level

        y += [current_level, current_level, -current_level, -current_level]

    return x, y

def bipolar_ami(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Bipolar AMI line encoding scheme. The Volatage V is 
    the peak-to-peak voltage. """

    if len(message) == 0:
        return [], []

    x = generate_x(len(message))[:-1]

    peak = V * 0.5
    y = []

    for i in message:
        if i == "0":
            y += [0 ,0]
        elif i == "1":
            y += [peak, peak]
            peak = -peak

    return x, y

def bipolar_pseudoternary(message: str, V=1):
    """ Generates the x and y values for the plot of a
    Bipolar Pseudoternary line encoding scheme. The 
    Volatage V is the peak-to-peak voltage. """

    if len(message) == 0:
        return [], []

    x = generate_x(len(message))[:-1]

    peak = V * 0.5
    y = []

    for i in message:
        if i == "1":
            y += [0 ,0]
        elif i == "0":
            y += [peak, peak]
            peak = -peak

    return x, y

def generate_plots(plot_func, message: str, title: str, save_dir: str, V=1, trunc_len: int = 32):
    os.makedirs(save_dir, exist_ok=True)
    filename_base = title.lower().replace(" ", "_")

    # --------------------------------------------
    # --- I. First trunc_len bits with labels  ---
    # --------------------------------------------
    message_trunc = message[:trunc_len]
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    x, y = plot_func(message_trunc, V=V_GLOBAL)
    plot_title = f'{title} (Truncated to First {trunc_len} Bits)' 
    ax.plot(
        x, 
        y, 
        label=plot_title, 
        color="tab:blue",
        linewidth=2,
        drawstyle="steps-post"
    )

    # Draw boundary lines for each bit
    for bit_boundary in range(0, len(message_trunc) + 1):
        ax.axvline(
            x=bit_boundary,
            linestyle="--",
            linewidth=0.6,
            color="gray",
            alpha=0.7,
        )
    
    # Draw horizontal line at y=0
    ax.axhline(
        y=0,
        color="black",
        linestyle="--",
        linewidth=1,
        alpha=0.7,
        zorder=1,  # Keeps line behind data points if needed
    )

    # Set custom x-ticks at bit centers for clear labeling
    ax.set_title(plot_title, fontsize=10, fontweight='bold', pad=10)
    ax.set_xticks([i + 0.5 for i in range(len(message_trunc))])
    ax.set_xticklabels([str(b) for b in message_trunc])
    ax.set_xlabel("Time (Bit Intervals)")

    ax.set_ylabel("Voltage (V)")

    # Keep y-limits clean with slight padding
    ax.set_ylim(min(y) - V * 0.5, max(y) + V * 0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{filename_base}_truncated.png"))
    plt.close(fig)
    
    # --------------------------------------------
    # --- II. Full message with reduced layout ---
    # --------------------------------------------

    # Dynamically scale width for the full message (0.6 inches per byte / 8 bits)
    # full_width = max(12, (len(message) / 8) * 0.6)
    # fig, ax = plt.subplots(figsize=(full_width, 3.5), dpi=250)
    fig, ax = plt.subplots(figsize=(12, 3.5), dpi=250)

    x, y = plot_func(MESSAGE, V=V_GLOBAL)
    plot_title = f'{title} (Full Message)'
    ax.plot(
        x, 
        y, 
        label=plot_title, 
        color="tab:blue",
        linewidth=0.8,
        drawstyle="steps-post"
    )

    # Draw boundary lines matched to actual voltage range
    for byte_boundary in range(0, len(message) + 1, 8):
        ax.axvline(
            x=byte_boundary,
            linestyle="--",
            linewidth=0.6,
            color="gray",
            alpha=0.7,
        )

    # Draw horizontal line at y=-1
    ax.axhline(
        y=0,
        color="black",
        linestyle="-",
        linewidth=1,
        alpha=0.7,
        zorder=1,  # Keeps line behind data points if needed
    )
    
    BYTE_SIZE = 8

    # Group message into 8-bit chunks
    byte_chunks = [
        message[i : i + BYTE_SIZE]
        for i in range(0, len(message), BYTE_SIZE)
        ]

    # Calculate x-center for each byte chunk
    byte_tick_positions = [
        i * BYTE_SIZE + (len(chunk) / 2) for i, chunk in enumerate(byte_chunks)
        ]

    # Format labels as the char values of each byte
    byte_tick_labels = [
    chr(int("".join(map(str, chunk)), 2)) for chunk in byte_chunks
    ]

    # Apply ticks and labels
    ax.set_title(plot_title, fontsize=10, fontweight='bold', pad=10)
    ax.set_xticks(byte_tick_positions)
    ax.set_xticklabels(byte_tick_labels, fontsize=12)
    ax.set_xlabel("Time (Byte Intervals)")

    ax.set_ylabel("Voltage (V)")

    # Keep y-limits clean with slight padding
    ax.set_ylim(min(y) - 0.5, max(y) + 0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{filename_base}_full.png"))
    plt.close(fig)

if __name__ == "__main__":
# TODO: USE FULL MESSAGE. ONLY FOR TESTING
    MESSAGE = MESSAGE_BIN

    # Create/Clean directory for generated plots
    EXPORT_DIR = 'line_encoding_plots'
    if os.path.exists(EXPORT_DIR):
        print("Removing old plots...")
        shutil.rmtree(EXPORT_DIR)  # Delete old plots/directory
    os.makedirs(EXPORT_DIR, exist_ok=True)

    TRUNC_LENGTH = 16

    # Define schemes to generate
    schemes = [
        (unipolar_scheme, "Unipolar NRZ", TRUNC_LENGTH),
        (polar_nrz_l_scheme, "Polar NRZ-L", TRUNC_LENGTH),
        (polar_nrz_i_scheme, "Polar NRZ-I", TRUNC_LENGTH),
        (polar_rz_scheme, "Polar RZ", TRUNC_LENGTH),
        (bipolar_manchester, "Bipolar Manchester", TRUNC_LENGTH),
        (bipolar_differential_manchester, "Bipolar Differential Manchester", TRUNC_LENGTH),
        (bipolar_ami, "Bipolar AMI", TRUNC_LENGTH),
        (bipolar_pseudoternary, "Bipolar Pseudoternary", TRUNC_LENGTH),
    ]

    # Generate Each Plot
    for func, title, trun in schemes:
        print(f"Generating plot for: {title}...")
        generate_plots(func, MESSAGE, title, EXPORT_DIR, V=1, trunc_len=trun)

    print("All plots generated successfully!")
