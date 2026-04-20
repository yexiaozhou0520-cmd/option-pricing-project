import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# ====================== 1. Black-Scholes 模型 ======================
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * stats.norm.cdf(d1) - K * np.exp(-r*T) * stats.norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r*T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return price, d1, d2

# ====================== 2. 蒙特卡洛模拟 ======================
def monte_carlo_option(S, K, T, r, sigma, n_simulations=100000):
    np.random.seed(666)
    Z = np.random.normal(0, 1, n_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoffs = np.maximum(ST - K, 0)
    price = np.exp(-r * T) * np.mean(payoffs)
    return price

# ====================== 参数（可自己改） ======================
S = 100    # 标的价格
K = 100    # 行权价
T = 1      # 到期时间 1年
r = 0.05   # 无风险利率
sigma = 0.2# 波动率

# ====================== 计算 ======================
bs_price, d1, d2 = black_scholes(S, K, T, r, sigma, 'call')
mc_price = monte_carlo_option(S, K, T, r, sigma, 100000)

# ====================== 输出结果 ======================
print("="*60)
print("Black-Scholes 欧式看涨期权价格：", round(bs_price, 4))
print("蒙特卡洛模拟 欧式看涨期权价格：", round(mc_price, 4))
print("两者误差：", round(abs(bs_price - mc_price), 4))
print("="*60)

# ====================== 波动率敏感性分析 ======================
sigmas = np.linspace(0.1, 0.5, 20)
prices = [black_scholes(S, K, T, r, s, 'call')[0] for s in sigmas]

plt.figure(figsize=(10,4))
plt.plot(sigmas, prices, marker='o')
plt.title('Option Price vs Volatility')
plt.xlabel('Volatility (σ)')
plt.ylabel('Call Price')
plt.grid(True)
plt.show()