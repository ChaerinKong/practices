import numpy as np
import matplotlib.pyplot as plt

#### Logistic Sigmoid Function ####
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

#### back-propagation on w11 ####
def back_prop_w11(g, y, x1, w3):
    return -2*(g-y)*y*(1-y)*w3*x1

#### back-propagation on w12 ####
def back_prop_w12(g, y, x1, w4):
    return -2*(g-y)*y*(1-y)*w4*x1

#### back-propagation on w21 ####
def back_prop_w21(g, y, x2, w3):
    return -2*(g-y)*y*(1-y)*w3*x2

#### back-propagation on w22 ####
def back_prop_w22(g, y, x2, w4):
    return -2*(g-y)*y*(1-y)*w4*x2

def back_prop_w3(g, y, x1, x2, w11, w21):
    return -2*(g-y)*y*(1-y)*(w11*x1+w21*x2)

def back_prop_w4(g, y, x1, x2, w12, w22):
    return -2*(g-y)*y*(1-y)*(w12*x1+w22*x2)

#### Input forward-feeding ####
def feedforward(x1, x2, w11, w12, w21, w22, w3, w4, theta):
    return sigmoid(w3*(w11*x1+w21*x2)+w4*(w12*x1+w22*x2)-theta)

#### Initial Values Assignment ####
w11 = 0.1
w12 = -0.1
w21 = -0.1
w22 = 0.1
w3 = 0.1
w4 = -0.1
theta = 0.5
lr = 0.25
epoch = 500

wb11 = list()
wb12 = list()
wb21 = list()
wb22 = list()
wb3 = list()
wb4 = list()

for i in range(epoch):
    if i % 4 == 0:
        x1 = 0
        x2 = 0
        g = 0

    elif i % 4 == 1:
        x1 = 1
        x2 = 0
        g = 1

    elif i % 4 == 2:
        x1 = 0
        x2 = 1
        g = 1

    else:
        x1 = 1
        x2 = 1
        g = 0

    y = feedforward(x1, x2, w11, w12, w21, w22, w3, w4, theta)
    w11 = w11 - lr*back_prop_w11(g, y, x1, w3)
    w12 = w12 - lr*back_prop_w12(g, y, x1, w4)
    w21 = w21 - lr*back_prop_w21(g, y, x2, w3)
    w22 = w22 - lr*back_prop_w22(g, y, x2, w4)
    w3 = w3 - lr*back_prop_w3(g, y, x1, x2, w11, w21)
    w4 = w4 - lr*back_prop_w4(g, y, x1, x2, w12, w22)

    y = feedforward(x1, x2, w11, w12, w21, w22, w3, w4, theta)
    w11 = w11 - lr*back_prop_w11(g, y, x1, w3)
    w12 = w12 - lr*back_prop_w12(g, y, x1, w4)
    w21 = w21 - lr*back_prop_w21(g, y, x2, w3)
    w22 = w22 - lr*back_prop_w22(g, y, x2, w4)
    w3 = w3 - lr*back_prop_w3(g, y, x1, x2, w11, w21)
    w4 = w4 - lr*back_prop_w4(g, y, x1, x2, w12, w22)

    print("y\t:", y, "g\t", g, "g-y\t", g-y, "x1\t", x1, "x2\t", x2)
    print("w11\t", w11, "w12\t", w12, "w21\t", w21, "w22\t", w22, "w3\t", w3, "w4\t", w4)
    print('-'*120)

    wb11.append(w11)
    wb12.append(w12)
    wb21.append(w21)
    wb22.append(w22)
    wb3.append(w3)
    wb4.append(w4)

x = np.arange(1, 500, 1)

plt.figure(1)
plt.plot(x, wb11[1:500], 'k')

plt.figure(2)
plt.plot(x, wb12[1:500], 'k')

plt.figure(3)
plt.plot(x, wb21[1:500], 'k')

plt.figure(4)
plt.plot(x, wb22[1:500], 'k')

plt.figure(5)
plt.plot(x, wb3[1:500], 'k')

plt.figure(6)
plt.plot(x, wb4[1:500], 'k')

plt.show()
