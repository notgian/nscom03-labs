import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before pyplot

import matplotlib.pyplot as plt
import numpy as np
import os


C_THZ_NM = 299_792.458

# Create directory for generated plots
os.makedirs('rainbow_plots', exist_ok=True)

# Base color definitions
# range is wavelength in nm
COLOR_DATA = {
    "Red": {"hex": "#FF0000", "range": (620, 750)},
    "Orange": {"hex": "#FF7F00", "range": (590, 620)},
    "Yellow": {"hex": "#EAEA0E", "range": (570, 590)},
    "Green": {"hex": "#0EED0E", "range": (495, 570)},
    "Blue": {"hex": "#0000FF", "range": (450, 495)},
    "Indigo": {"hex": "#4B0082", "range": (425, 450)},
    "Violet": {"hex": "#9400D3", "range": (380, 425)},
}

# Calculate color info from the base color data as above
# wavelength used is the midpoint of the range
# NOTE: Amplitude and Phase Shift are dynamically set to 1.0 and 0.
colors_info = []
for name, data in COLOR_DATA.items():
    avg_wavelength = sum(data["range"]) / 2
    freq_thz = round(C_THZ_NM / avg_wavelength, 2)
    colors_info.append({
        "name": name,
        "hex": data["hex"],
        "wavelength_nm": avg_wavelength,
        "freq_thz": freq_thz,  # Frequency in THz
        "T_fs": 1000.0 / freq_thz  # Period in femtoseconds
        # Explanation:
        # 1 THz = 10^12 hz; 1s = 10^15 fs
        # Perod in s: T = 1 / f
        # T_fs  = (1 / (f * 10^12)) * 10^15 <--- convert to fs
        #       = 10^15 / 10^12 / f = 1000 / f_thz
    })

# Simple helper to get the color info by its name
def get_color_info(name: str):
    for c in colors_info:
        if c["name"] == name:
            return c
    return None

# =====================================================
# ----- Part I: Generating Individual Color Plots -----
# =====================================================
# Looping through each color in the color info
for c in colors_info:
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    freq_thz = c["freq_thz"]
    T_fs = c["T_fs"]
    color_code = c.get("hex")

    # Amplitude and phase shift are always set to these values
    amplitude = 1.0
    phase_shift = 0
    
    # plotting the sinusodial wave
    # formuala: s(t) = A sin(2πft + ϕ)
    # A - ampliture
    # f - frequency
    # t - time

    # we generate our x values (the linspace) then
    # get each corresponding y, and plot this
    t_fs = np.linspace(0, T_fs, 1000)
    y = amplitude * np.sin(2 * np.pi * freq_thz * (t_fs / 1000.0) + phase_shift)
    ax.plot(
        t_fs, 
        y, 
        color=color_code, 
        linewidth=2, 
        label=f'{c["name"]} Light Signal ({c["freq_thz"]} THz)'
    )
    
    # --- AMPLITUDE ANNOTATION ---
    # Finding the peak in the graph and then the x and y of the point
    peak_idx = np.argmax(y)
    t_peak = t_fs[peak_idx]
    y_peak = y[peak_idx]

    ax.vlines(
        x=t_peak,
        ymin=0,
        ymax=y_peak,
        colors="black",
        linestyles="--",
        linewidth=1.2,
        alpha=0.8,
    )

    ax.plot(t_peak, y_peak, marker="o", markersize=5, color="black")

    # Add text next to the vertical line
    ax.text(
        x=t_peak + (T_fs * 0.03),  
        y=amplitude / 2,
        s="Peak Amplitude (A = 1.0)",
        fontsize=8,
        fontweight="bold",
        verticalalignment="center",
        bbox=dict(
            boxstyle="round,pad=0.3", fc="#FFFFE0", ec="gray", lw=0.5
        ),
        ha='left',
    )
    
    # --- PERIOD ANNOTATION ---
    y_period = -1.2

    # Double-headed arrow spanning the period
    ax.annotate(
        "",
        xy=(0, y_period),
        xytext=(T_fs, y_period),
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=1.5,
            color="black",
        ),
    )

    # Label text over the arrow line
    ax.text(
        x=T_fs / 2.0,
        y=y_period,
        s=f"Period = {T_fs:.2f} fs",
        fontsize=8,
        fontweight="bold",
        horizontalalignment="center",
        verticalalignment="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.8),
    )
    
    # The rest of the labels
    ax.set_title(f'Sinusoidal Waveform - {c["name"]} Light Signal\n(Frequency: {freq_thz} THz | Wavelength: {c["wavelength_nm"]} nm)', fontsize=10, fontweight='bold', pad=10)
    ax.set_xlabel('Time (fs)', fontsize=8.5)
    ax.set_ylabel('Amplitude (V)', fontsize=8.5)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlim(0, T_fs)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'rainbow_plots/{c["name"].lower()}.png', dpi=300)
    plt.close(fig)

# =====================================================
# ----- Part II: Generating Composite Signal Plots-----
# =====================================================
end_lim = 20

# ----- Combination 1: Red + Blue (2 Signals) -----
t_fs = np.linspace(0, end_lim, 1000)
fig, axs = plt.subplots(3, 1, figsize=(7, 7.5), dpi=250)

# Frequencies in THz
f_red_thz = get_color_info("Red")["freq_thz"]
f_blue_thz = get_color_info("Blue")["freq_thz"]

# Amplitude and phase shift are always set to these values
amplitude = 1.0
phase_shift = 0

# Red and blue sine waves
y_red = amplitude * np.sin(2 * np.pi * f_red_thz * (t_fs / 1000) + phase_shift)
y_blue = amplitude * np.sin(2 * np.pi * f_blue_thz * (t_fs / 1000) + phase_shift)
y_comp1 = y_red + y_blue

# Plot the composite signal
axs[0].plot(t_fs, y_comp1, color='#8E44AD', linewidth=1.8, label=f'Composite: Red ({f_red_thz:.2f} THz) + Blue ({f_blue_thz:.2f} THz)')
axs[0].set_title('Composite Signal 1: Combination of 2 Waveforms (Red + Blue)', fontsize=9.5, fontweight='bold')
axs[0].set_xlabel('Time (fs)', fontsize=8)
axs[0].set_ylabel('Amplitude (V)', fontsize=8)
axs[0].set_xlim(0, end_lim)
axs[0].grid(True, linestyle=':', alpha=0.6)
axs[0].legend(loc='upper right', fontsize=8)

# ----- Combination 2: Red + Green + Blue (RGB - 3 Signals) -----

# Green sine wave
f_green_thz = get_color_info("Green")["freq_thz"]
y_green = amplitude * np.sin(2 * np.pi * f_green_thz * (t_fs / 1000) + phase_shift)
y_comp2 = y_red + y_green + y_blue

axs[1].plot(t_fs, y_comp2, color='#2C3E50', linewidth=1.8, label='Composite: Red + Green + Blue (RGB Primary Light)')
axs[1].set_title('Composite Signal 2: Combination of 3 Waveforms (Red + Green + Blue)', fontsize=9.5, fontweight='bold')
axs[1].set_xlabel('Time (fs)', fontsize=8)
axs[1].set_ylabel('Amplitude (V)', fontsize=8)
axs[1].set_xlim(0, end_lim)
axs[1].grid(True, linestyle=':', alpha=0.6)
axs[1].legend(loc='upper right', fontsize=8)

# ----- Combination 3: All 7 Rainbow Colors Combined (Full Spectrum) -----
y_all = np.zeros_like(t_fs)
for c in colors_info:
    f_thz = c["freq_thz"]
    amplitude = 1.0
    phase_shift = 0
    y_all += amplitude * np.sin(2 * np.pi * f_thz * (t_fs / 1000) + phase_shift)

axs[2].plot(t_fs, y_all, color='#117A65', linewidth=1.5, label='Composite: All 7 ROYGBIV Spectral Signals')
axs[2].set_title('Composite Signal 3: Full ROYGBIV Spectrum Waveform Superposition', fontsize=9.5, fontweight='bold')
axs[2].set_xlabel('Time (fs)', fontsize=8.5)
axs[2].set_ylabel('Amplitude (V)', fontsize=8)
axs[2].set_xlim(0, end_lim)
axs[2].grid(True, linestyle=':', alpha=0.6)
axs[2].legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig('rainbow_plots/composite_signals.png', dpi=300)
plt.close(fig)

# ============================================================
# ----- 3. Generate Frequency-Domain Light Spectrum Plot -----
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), dpi=300)

# Extract frequency data
freqs = [c["freq_thz"] for c in colors_info]
bar_colors = [c.get("hex") for c in colors_info]
base_amplitude = 1.0
stagger = 0.20

# Stagger line heights for readability
staggered_amps = [
    base_amplitude if i % 2 == 0 else (base_amplitude - stagger)
    for i in range(len(freqs))
]

ax1.vlines(x=freqs, ymin=0, ymax=staggered_amps, colors=bar_colors, linewidth=2.5)
ax1.plot(freqs, staggered_amps, "o", color="black", markersize=4)

for i, c in enumerate(colors_info):
    ax1.text(
        c["freq_thz"],
        staggered_amps[i] + 0.02,
        f'{c["name"]}\n{c["freq_thz"]} THz',
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color=c.get("hex"),
    )

ax1.set_title('Frequency-Domain Representation: Discrete Spectral Lines (ROYGBIV)', fontsize=10, fontweight='bold')
ax1.set_xlabel('Frequency (THz)', fontsize=8.5)
ax1.set_ylabel('Peak Amplitude (V)\nNOTE: Staggered for Visibility', fontsize=8.5)
ax1.set_xlim(380, 800)
ax1.set_ylim(0, 1.3)
ax1.grid(True, linestyle=':', alpha=0.6)

# --- CONTINUOUS LIGHT SPECTRUM BAND) ---

# Helper to convert wavelength to rgb colors
def wavelength_to_rgb(wl):
    """Calculates continuous RGB values for wavelengths from 380nm to 750nm. 
        Normalizes the values and performs linear interpolation to map the values
        for each color respectively."""
    # 1. Violet -> Blue (380–440 nm): Red decays linearly 1.0 -> 0.0
    if 380 <= wl < 440:
        r = -(wl - 440) / (440 - 380)
        g = 0.0
        b = 1.0

    # 2. Blue -> Cyan (440–490 nm): Green grows linearly 0.0 -> 1.0
    elif 440 <= wl < 490:
        r = 0.0
        g = (wl - 440) / (490 - 440)
        b = 1.0

    # 3. Cyan -> Green (490–510 nm): Blue decays linearly 1.0 -> 0.0
    elif 490 <= wl < 510:
        r = 0.0
        g = 1.0
        b = -(wl - 510) / (510 - 490)

    # 4. Green -> Yellow (510–580 nm): Red grows linearly 0.0 -> 1.0
    elif 510 <= wl < 580:
        r = (wl - 510) / (580 - 510)
        g = 1.0
        b = 0.0

    # 5. Yellow -> Red (580–645 nm): Green decays linearly 1.0 -> 0.0
    elif 580 <= wl < 645:
        r = 1.0
        g = -(wl - 645) / (645 - 580)
        b = 0.0

    # 6. Deep Red (645–750 nm): Constant maximal Red intensity
    elif 645 <= wl <= 750:
        r = 1.0
        g = 0.0
        b = 0.0

    # Non-visible spectrum (UV < 380 nm or IR > 750 nm): Constant black
    else:
        r, g, b = 0.0, 0.0, 0.0

    return (r , g, b)


# Define THz frequency domain (380 THz - 800 THz)
freq_domain = np.linspace(380, 800, 1000)
spectrum_img = np.zeros((50, 1000, 3))

for i, f_thz in enumerate(freq_domain):
    wl = C_THZ_NM / f_thz
    spectrum_img[:, i] = wavelength_to_rgb(wl)

# Generate and render the light spectrum
ax2.imshow(spectrum_img, extent=[380, 800, 0, 1], aspect='auto')
ax2.set_yticks([])
ax2.set_xlim(380, 800)
ax2.set_xlabel('Frequency (THz) / Visible Spectrum Band', fontsize=8.5)
ax2.set_title('Visible Light Spectrum Map in Frequency Domain', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('rainbow_plots/light_spectrum.png', dpi=300)
plt.close(fig)
