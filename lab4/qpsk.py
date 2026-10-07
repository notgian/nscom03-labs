import numpy as np
import matplotlib.pyplot as plt
import sys

# generate quadrature carrier signal
Tb = 1
t = np.arange(0, Tb + Tb/100, Tb/100)
fc = 1

c1 = np.sqrt(2/Tb) * np.cos(2*np.pi*fc*t)
c2 = np.sqrt(2/Tb) * np.sin(2*np.pi*fc*t)

# generate message signal
N = 8
m = np.random.rand(N)

if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        m = [0, 1, 0, 1, 0, 0, 1, 1]

t1 = 0
t2 = Tb

# Arrays for storing the signals
odd_sig = np.zeros((N, len(t)))
even_sig = np.zeros((N, len(t)))

qpsk_plot = plt.figure(figsize=(10, 8))

for i in range(0, N-1, 2):
    t = np.arange(t1, t2 + Tb/100, Tb/100)

    if m[i] > 0.5:
        m[i] = 1
        m_s = np.ones(len(t))
    else:
        m[i] = 0
        m_s = -1 * np.ones(len(t))

    # odd bits modulated signal
    odd_sig[i, :] = c1 * m_s

    if m[i+1] > 0.518:
        m[i+1] = 1
        m_s = np.ones(len(t))
    else:
        m[i+1] = 0
        m_s = -1 * np.ones(len(t))

    # even bits modulated signal
    even_sig[i, :] = c2 * m_s

    # qpsk signal
    qpsk = odd_sig + even_sig

    # plot the QPSK modulated signal
    plt.subplot(2, 2, 4)
    plt.plot(t, qpsk[i, :])
    plt.title('QPSK signal')
    plt.xlabel('t---->')
    plt.ylabel('s(t)')
    plt.grid(True)

    t1 = t1 + (Tb + 0.01)
    t2 = t2 + (Tb + 0.01)

# plot the binary data bits and carrier signal
plt.subplot(2, 2, 1)
plt.stem(np.arange(0, N), m, basefmt=" ")
plt.title('binary data bits')
plt.xlabel('n---->')
plt.ylabel('b(n)')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(np.arange(0, Tb + Tb/100, Tb/100), c1)
plt.title('carrier signal-1')
plt.xlabel('t---->')
plt.ylabel('c1(t)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(np.arange(0, Tb + Tb/100, Tb/100), c2)
plt.title('carrier signal-2')
plt.xlabel('t---->')
plt.ylabel('c2(t)')
plt.grid(True)

plt.tight_layout()
plt.show()
