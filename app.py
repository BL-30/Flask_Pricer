from flask import Flask, flash, render_template, request
import math
from scipy.stats import norm

app = Flask(__name__)

def black_scholes_call(S, K, T, r, sigma):
    """
    :param S: Current stock price
    :param K: Option strike price
    :param T: Time to expiration (in years)
    :param r: Risk-free rate (annualized)
    :param sigma: Volatility (annualized)
    :return: Call option price
    """
    d1 = (math.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r*T) * norm.cdf(d2)

def black_scholes_put(S, K, T, r, sigma):
    d1 = (math.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

@app.route('/', methods=['POST', 'GET'])
def index():
    price = None
    if request.method == 'POST':
        S = float(request.form.get('S', 0))
        if S <= 0:
            flash('Stock price should be greater than 0')
            return render_template('index.html')
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        
        option_type = request.form.get('option_type', 'call')
        if option_type == 'call':
            price = black_scholes_call(S, K, T, r, sigma)
        else:
            price = black_scholes_put(S, K, T, r, sigma)
        #price = black_scholes_call(S, K, T, r, sigma)
        
    return render_template('index.html', price=price)


if __name__ == '__main__':
    app.run(debug=True)
