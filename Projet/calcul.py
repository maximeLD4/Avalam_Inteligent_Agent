import numpy as np
import matplotlib.pyplot as plt
CONST_MULT = 170
CONST_STEP_1 = 1.4/12
CONST_STEP_2 = 1/12

if __name__ == "__main__":

    def function(step):
        if step <= 18:
            return CONST_MULT*(1/(np.sqrt(2*np.pi)))*(np.exp((-1/2)*(16.6 + (step-6)*CONST_STEP_1 - 18)*(16.6 + (step-6)*CONST_STEP_1 - 18)))
        elif step <= 27:
            return CONST_MULT*(1/(np.sqrt(2*np.pi)))*(np.exp((-1/2)*(18 + (step-18)*CONST_STEP_2 - 18)*(18 + (step-18)*CONST_STEP_2 - 18)))
        elif step <= 36:
            return 50


    somme1 = 0
    somme2 = 0
    for i in range(0, 13):
        somme1 += CONST_MULT*(1/(np.sqrt(2*np.pi)))*(np.exp((-1/2)*(16.6 + i*CONST_STEP_1 - 18)*(16.6 + i*CONST_STEP_1 - 18)))
    print(somme1)
    for i in range(1, 13):
        somme2 += CONST_MULT*(1/(np.sqrt(2*np.pi)))*(np.exp((-1/2)*(18 + i*CONST_STEP_2 - 18)*(18 + i*CONST_STEP_2 - 18)))
    print(somme2)
    somme3 = 4 * 50
    print(somme3)
    print(somme1 + somme2 + somme3)
    print("------- START TEST : -----")
    somme_t_J1 = 0
    somme_t_J2 = 0
    sum_t_tab_J1 = []
    sum_t_tab_J2 = []
    step_tab_J1 = []
    step_tab_J2 = []
    for k in range(6, 37):
        if k % 2 == 0:
            result = function(k)
            step_tab_J2.append(k)
            somme_t_J2 += result
            print(result)
            sum_t_tab_J2.append(result)
        else:
            result = function(k)
            step_tab_J1.append(k)
            somme_t_J1 += result
            print(result)
            sum_t_tab_J1.append(result)
    print("test somme_t J1 : ", somme_t_J1)
    print("test somme_t J2 : ", somme_t_J2)
    plt.plot(step_tab_J2, sum_t_tab_J2)
    plt.plot(step_tab_J1, sum_t_tab_J1)
    plt.show()
