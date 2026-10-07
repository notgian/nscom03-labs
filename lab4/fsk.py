import numpy as np
import matplotlib.pyplot as plt
import sys

# generate carrier signal
Tb = 1
fc1 = 2
fc2 = 5

t = np.arange(0, Tb + Tb/100, Tb/100)
c1 = np.sqrt(2/Tb) * np.sin(2*np.pi*fc1*t)
c2 = np.sqrt(2/Tb) * np.sin(2*np.pi*fc2*t)

# generate message signal
N = 8
m = np.random.rand(N)

if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        m = [0, 1, 0, 1, 0, 0, 1, 1]

t1 = 0
t2 = Tb

message = np.zeros((N, len(t)))
fsk_sig1 = np.zeros((N, len(t)))
fsk_sig2 = np.zeros((N, len(t)))

fig, fsk_plot = plt.subplots(5, 1, figsize=(10, 10), sharex=True)

for i in range(N):
    t = np.arange(t1, t2 + Tb/100, Tb/100)

    if m[i] > 0.5:
        m[i] = 1
        m_s = np.ones(len(t))
        invm_s = np.zeros(len(t))
    else:
        m[i] = 0
        m_s = np.zeros(len(t))
        invm_s = np.ones(len(t))

    message[i, :] = m_s

    # multiplier
    fsk_sig1[i, :] = c1 * m_s
    fsk_sig2[i, :] = c2 * invm_s
    fsk = fsk_sig1 + fsk_sig2

    # plotting message signal
    fsk_plot[1].plot(t, message[i, :], 'r')

    # plotting FSK signal
    fsk_plot[4].plot(t, fsk[i, :])

    t1 = t1 + Tb
    t2 = t2 + Tb

# binary data
fsk_plot[0].stem(np.arange(0, N), m, basefmt=" ")
fsk_plot[0].set_title('Binary Data')
fsk_plot[0].set_ylabel('b(n)')
fsk_plot[0].set_yticks([0, 1])
fsk_plot[0].grid(True)

# message signal
fsk_plot[1].set_title('Message Signal')
fsk_plot[1].set_ylabel('m(t)')
fsk_plot[1].set_ylim(-0.5, 1.5)
fsk_plot[1].set_yticks([0, 1])
fsk_plot[1].grid(True)

# carrier signal 1
t_carrier = np.arange(0, N + Tb/100, Tb/100)
c1_full = np.sqrt(2/Tb) * np.sin(2*np.pi*fc1*t_carrier)
fsk_plot[2].plot(t_carrier, c1_full)
fsk_plot[2].set_title('Carrier Signal 1')
fsk_plot[2].set_ylabel('c1(t)')
fsk_plot[2].set_ylim(-2, 2)
fsk_plot[2].grid(True)

# carrier signal 2
c2_full = np.sqrt(2/Tb) * np.sin(2*np.pi*fc2*t_carrier)
fsk_plot[3].plot(t_carrier, c2_full)
fsk_plot[3].set_title('Carrier Signal 2')
fsk_plot[3].set_ylabel('c2(t)')
fsk_plot[3].set_ylim(-2, 2)
fsk_plot[3].grid(True)

# FSK signal
fsk_plot[4].set_title('FSK Signal')
fsk_plot[4].set_xlabel('t ---->')
fsk_plot[4].set_ylabel('s(t)')
fsk_plot[4].set_ylim(-2, 2)
fsk_plot[4].grid(True)

for a in fsk_plot:
    a.set_xlim(0, N)
    a.set_xticks(np.arange(0, N + 1))
    a.margins(x=0)

plt.tight_layout()
plt.show()
