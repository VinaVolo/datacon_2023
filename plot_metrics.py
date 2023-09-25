import matplotlib.pyplot as plt
import numpy as np


def R2_plot(R2_train: list, R2_test: list, iter_lst: list, type_iter: str):
    """Function for plotting R2Score"""
    
    plt.plot(iter_lst, R2_train, label='train')
    plt.plot(iter_lst, R2_test, label='test')
    
    plt.xlabel(type_iter)
    plt.ylabel('R2Score')
    
    plt.grid()
    
    plt.legend()


def RMSE_plot(RMSE_train: list, RMSE_test: list, iter_lst: list, type_iter: str):
    """Function for plotting RMSE"""
    
    plt.plot(iter_lst, RMSE_train, label='train')
    plt.plot(iter_lst, RMSE_test, label='test')
    
    plt.xlabel(type_iter)
    plt.ylabel('RMSE')
    
    plt.grid()
    
    plt.legend()
    
    
def R2_RMSE_plot(errors: dict, iter_lst: list, type_iter: str):
    """Function for plotting two graphs of R2 and RMSE"""
    
    fig, axs = plt.subplots(1, 2, figsize=(20, 7))
    
    max_R2_train = np.round(max(errors.get('R2_train')), 4)
    max_R2_test = np.round(max(errors.get('R2_test')), 4)
    
    min_RMSE_train = np.round(min(errors.get('RMSE_train')), 4)
    min_RMSE_test = np.round(min(errors.get('RMSE_test')), 4)
    
    print(f'max R2_train = {max_R2_train}\nmax R2_test = {max_R2_test}')
    print('-' * 20)
    print(f'min RMSE_train = {min_RMSE_train}\nmin RMSE_test = {min_RMSE_test}')
    
    axs[0].plot(iter_lst, errors.get('R2_train'), label='train')
    axs[0].plot(iter_lst, errors.get('R2_test'), label='test')
    axs[0].set_xlabel(type_iter)
    axs[0].set_ylabel('R2Score')
    axs[0].legend()
    axs[0].set_title('R2Score')
    axs[0].grid()
    
    axs[1].plot(iter_lst, errors.get('RMSE_train'), label='train')
    axs[1].plot(iter_lst, errors.get('RMSE_test'), label='test')
    axs[1].set_xlabel(type_iter)
    axs[1].set_ylabel('RMSE')
    axs[1].legend()
    axs[1].set_title('RMSE')
    axs[1].grid()