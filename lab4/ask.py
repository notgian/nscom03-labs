import numpy as np
import matplotlib.pyplot as plt
import sys

# generate carrier signal
Tb = 1
fc = 10
t = np.arange(0, Tb + Tb/100, Tb/100)
c = np.sqrt(2/Tb) * np.sin(2*np.pi*fc*t)

# generate message signal
N = 8
m = np.random.rand(N)

if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        m = [0, 1, 0, 1, 0, 0, 1, 1]

t1 = 0
t2 = Tb

message = np.zeros((N, len(t)))
ask_sig = np.zeros((N, len(t)))

ask_plot = plt.figure(figsize=(10, 10))

for i in range(N):
    t = np.arange(t1, t2 + 0.01, 0.01)

    if m[i] > 0.5:
        m[i] = 1
        m_s = np.ones(len(t))
    else:
        m[i] = 0
        m_s = np.zeros(len(t))

    message[i, :] = m_s

    # product of carrier and message
    ask_sig[i, :] = c * m_s

    # plot the message and ASK signal
    plt.subplot(5, 1, 2)
    plt.axis([0, N, -2, 2])
    plt.plot(t, message[i, :], 'r')
    plt.title('message signal')
    plt.xlabel('t--->')
    plt.ylabel('m(t)')
    plt.xticks(np.arange(0, N + 1))
    plt.grid(True)

    plt.subplot(5, 1, 4)
    plt.plot(t, ask_sig[i, :])
    plt.title('ASK signal')
    plt.xlabel('t--->')
    plt.ylabel('s(t)')
    plt.xlim(0, N)
    plt.xticks(np.arange(0, N + 1))
    plt.grid(True)

    t1 = t1 + Tb
    t2 = t2 + Tb

# plot the carrier signal
t = np.arange(0, N + Tb/100, Tb/100)
c = np.sqrt(2/Tb) * np.sin(2*np.pi*fc*t)

plt.subplot(5, 1, 3)
plt.plot(t, c)
plt.title('carrier signal')
plt.xlabel('t--->')
plt.ylabel('c(t)')
plt.xlim(0, N)
plt.xticks(np.arange(0, N + 1))
plt.grid(True)

# plot the input binary data
plt.subplot(5, 1, 1)
plt.stem(np.arange(0, N), m, basefmt=" ")
plt.title('binary data bits')
plt.xlabel('n--->')
plt.ylabel('b(n)')
plt.xlim(0, N)
plt.xticks(np.arange(0, N + 1))
plt.grid(True)

plt.tight_layout()
plt.show()
