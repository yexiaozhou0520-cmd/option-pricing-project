import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

"""
欧式期权定价模型
实现方法：
1. Black-Scholes 解析解（闭式解）
2. 蒙特卡洛模拟法（数值解）
项目目的：验证衍生品定价方法一致性，展示量化建模与数值分析能力
"""

# ==============================
# 1. Black-Scholes 期权定价公式
# ==============================
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Black-Scholes 欧式期权定价公式
    :param S: 标的资产当前价格
    :param K: 期权执行价格
    :param T: 到期时间（年）
    :param r: 无风险利率
    :param sigma: 标的资产波动率
    :param option_type: 期权类型（call/put）
    :return: 期权价格
    """
    # 计算 d1 和 d2（BS 公式核心参数）
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 计算看涨期权价格
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # 计算看跌期权价格
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    else:
        raise ValueError("option_type 必须为 'call' 或 'put'")
    
    return price

# ==============================
# 2. 蒙特卡洛模拟期权定价
# ==============================
def monte_carlo_option(S, K, T, r, sigma, n_simulations=100000, option_type='call'):
    """
    蒙特卡洛模拟欧式期权定价（风险中性测度下）
    :param n_simulations: 模拟路径数量
    :return: 期权价格与标准误差
    """
    np.random.seed(666)  # 固定随机种子，保证结果可复现
    
    # 风险中性下的资产价格动态（几何布朗运动）
    ST = S * np.exp(
        (r - 0.5 * sigma ** 2) * T
        + sigma * np.sqrt(T) * np.random.normal(size=n_simulations)
    )
    
    # 计算期权到期收益
    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)
    
    # 折现求期望
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    # 计算标准误差（用于结果稳健性分析）
    std_error = np.std(payoffs) / np.sqrt(n_simulations)
    
    return option_price, std_error

# ==============================
# 3. 主程序：参数设置 + 定价对比
# ==============================
if __name__ == '__main__':
    # 期权基础参数
    S = 50        # 标的价格
    K = 50        # 执行价
    T = 1         # 到期时间（1年）
    r = 0.05      # 无风险利率
    sigma = 0.2   # 波动率

    # 计算 BS 解析解
    bs_call = black_scholes(S, K, T, r, sigma, 'call')
    print(f"Black-Scholes 看涨期权价格: {bs_call:.4f}")

    # 计算蒙特卡洛模拟解
    mc_call, mc_err = monte_carlo_option(S, K, T, r, sigma, n_simulations=100000)
    print(f"蒙特卡洛模拟看涨期权价格: {mc_call:.4f}")
    print(f"蒙特卡洛标准误差: {mc_err:.4f}")

    # ==============================
    # 4. 波动率敏感性分析（可视化）
    # ==============================
    sigma_range = np.linspace(0.05, 0.5, 50)  # 波动率从 5% 到 50%
    call_prices = [black_scholes(S, K, T, r, sig, 'call') for sig in sigma_range]

    plt.figure(figsize=(10, 6))
    plt.plot(sigma_range, call_prices, label='Call Option Price', linewidth=2)
    plt.title('Option Price vs Volatility (Sensitivity Analysis)', fontsize=12)
    plt.xlabel('Volatility (σ)', fontsize=11)
    plt.ylabel('Option Price', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
