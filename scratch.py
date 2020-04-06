import numpy as np
from matplotlib import pyplot as plt

def pop(N, z, width):
	if z > width:
		u = 0
	elif z < 0:
		u = 0
	else:
		u = 1
	return N * u


def delI(N, z, I0, sig, width):
	if z < 0.0:
		dI = 0
	elif z > width:
		dI = 0
	else:
		dI = N * sig * I0
	return dI


def trap(z0, z1, N0, N1):
	return (z1 - z0) * (N0 + N1) / 2


def atten(N, z, I0, sig, width):
	if z < 0:
		v = I0
	elif z > width:
		v = I0 * np.exp(-sig * width)
	else:
		v = I0 * np.exp(-sig * N * z)  # Remember to change line above!!
	return v


def I0_rate(ED):
	return ED * 100 / 4.42e-16  # *10e-3 #Intensity per cm2 per s



ED=0.0001
width = 1.0
N0 = 1.20e15  # sample per cm-2
sig = 1.47e-16  # cross section per cm-2
phi = 0.3  # quantum yeidld of converstion
tstep = 1e-3  # In Seconds
tmax = 20e-3  # in seconds
residual = 0.1#0.5

z = np.linspace(-0.1, 1.1, 1000)
Ni = np.empty_like(z)
I = np.empty_like(z)
N = np.empty_like(z)
I0 = ED * 100 / 4.42e-16 * tstep
t = np.empty(int(tmax / tstep))

for i in enumerate(t):
	t[i[0]] = tstep

for i in enumerate(z):
	Ni[i[0]] = pop(N0*(1), i[1], width)
plt.plot(Ni, label='N0')

for i in enumerate(z):
	Ni[i[0]] = pop(N0*(1-residual), i[1], width)
plt.plot(Ni, label='N0')

for k in enumerate(t):
	Intergral = 0
	for i in enumerate(z):
		if i[0] == 0:
			# print('This is ',I0)
			I[i[0]] = I0
			N[i[0]] = 0
		# Intergral=0
		else:
			N[i[0]] = Ni[i[0]] - phi * delI(Ni[i[0]], i[1], I[i[0] - 1], sig, width)
			I[i[0]] = I[i[0] - 1] - (z[i[0]] - z[i[0] - 1]) * delI(Ni[i[0]], i[1], I[i[0] - 1], sig, width)
			Intergral = Intergral + trap(z[i[0] - 1], z[i[0]], N[i[0] - 1], N[i[0]])
	Ni = N
plt.plot(Ni,label='Ni')
plt.legend()
plt.show()
print(Intergral / N0)