import numpy as np
import matplotlib.pyplot as plt

CONST_MULT = 165
CONST_STEP_1 = 1.4 / 12
CONST_STEP_2 = 1 / 12
CST_SQRT = 10.7
CONST_STEP_NORM = 4 / 39
CONST_MULT_NORM = 195
CST = 1.5
CST_F3 = 2885

if __name__ == "__main__":

    def function(step):
        if step <= 18:
            return CONST_MULT * (1 / (np.sqrt(2 * np.pi))) * (
                np.exp((-1 / 2) * (16.6 + (step - 6) * CONST_STEP_1 - 18) * (16.6 + (step - 6) * CONST_STEP_1 - 18)))
        elif step <= 27:
            return CONST_MULT * (1 / (np.sqrt(2 * np.pi))) * (
                np.exp((-1 / 2) * (18 + (step - 18) * CONST_STEP_2 - 18) * (18 + (step - 18) * CONST_STEP_2 - 18)))
        elif step <= 40:
            return 45

    def function_sqrt(x):
        return CST_SQRT * np.sqrt(x)


    def function_norm(x):
        return CONST_MULT_NORM * (1 / (np.sqrt(2 * np.pi))) * (
            np.exp((-1 / 2) * (x * CONST_STEP_NORM - 2) * (x * CONST_STEP_NORM - 2)))

    def function2(step):
        return CST*(20 + 170*(1 / (2*(np.sqrt(15 * np.pi)))) * (np.exp((-1 / 2) * (step-20) * (step-20)/(15*15))))

    def function3(step):
        if step <= 28:
            return CST_F3*(1 / (16*(np.sqrt(2 * np.pi)))) * (np.exp((-1 / 2) * (step-15) * (step-15)/(16*16)))
        elif step == 29:
            return 20
        elif step == 30 or step == 31:
            return 4
        elif step >= 32:
            return 1


    somme_t_J1 = 0
    somme_t_J2 = 0
    sum_t_tab_J1 = []
    sum_t_tab_J2 = []
    step_tab_J1 = []
    step_tab_J2 = []
    for k in range(2, 38):
        if k % 2 == 0:
            result = function3(k)
            step_tab_J2.append(k)
            somme_t_J2 += result
            sum_t_tab_J2.append(result)

        else:
            result = function3(k)
            step_tab_J1.append(k)
            somme_t_J1 += result
            sum_t_tab_J1.append(result)

    plt.plot(step_tab_J2, sum_t_tab_J2, "-b", label="J2 (time allocated : " + str(somme_t_J2) + "sec)")
    plt.plot(step_tab_J1, sum_t_tab_J1, "-r", label="J1 (time allocated : " + str(somme_t_J1) + "sec)")
    plt.legend(loc="lower left")
    plt.xlabel("Step")
    plt.ylabel("Time allocated per step")
    plt.savefig("Time_function_normal.png")
    plt.show()

