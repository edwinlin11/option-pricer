from flask import Flask, request, jsonify
import math, numpy as np, yfinance as yf
import matplotlib.pyplot as plt
import io, base64
import scipy.stats as stats
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Option Pricer API is running!"

# Add stock data route
@app.route('/stock-data/<ticker>')
def stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            return jsonify({
                'success': False
            })
        
        # Get current price and historical volatility
        price = float(hist['Close'].iloc[-1])
        
        # Calculate 30-day volatility
        hist_30d = stock.history(period="30d")
        volatility = float(hist_30d['Close'].pct_change().std() * np.sqrt(252) * 100)
        
        return jsonify({
            'success': True,
            'price': price,
            'volatility': volatility
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Change route from /option-pricer to /option-pricing to match frontend
@app.route('/option-pricing', methods=['POST'])
def option_pricing():
    data = request.get_json()
    # Rest of your option pricing code remains the same...
    # Get ticker from the request.
    ticker = data.get('ticker', None)
    
    # Use yfinance to get current stock price.
    if ticker:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if hist.empty:
                S = float(data.get('stockPrice', 100))
            else:
                S = float(hist['Close'].iloc[-1])
        except Exception as e:
            S = float(data.get('stockPrice', 100))
    else:
        S = float(data.get('stockPrice', 100))

    # Get remaining parameters.
    K = float(data.get('strikePrice', 100))
    timeToExpiry = float(data.get('timeToExpiry', 40))  # in days
    T = timeToExpiry / 365.0                          # in years
    vol = float(data.get('volatility', 20)) / 100.0     # convert percent to decimal
    r = float(data.get('riskFreeRate', 2.5)) / 100.0    # convert percent to decimal
    M = int(data.get('iterations', 1000))

    # One-step simulation using np.random.normal() for standard normal values.
    dt = T
    nudt = (r - 0.5 * vol**2) * dt
    volsdt = vol * math.sqrt(dt)
    lnS = math.log(S)

    sum_CT = 0.0
    sum_CT2 = 0.0
    sim_paths = []  # store first 100 terminal stock prices
    for i in range(M):
        # Use standard normal distribution.
        Z = np.random.normal()  # standard normal random variable
        lnST = lnS + nudt + volsdt * Z
        ST = math.exp(lnST)
        CT = max(0, ST - K)  # European call payoff
        sum_CT += CT
        sum_CT2 += CT * CT
        if i < 100:
            sim_paths.append(ST)

    # Calculate option price and standard error.
    optionPrice = math.exp(-r * T) * (sum_CT / M)
    sigma = math.sqrt(((sum_CT2 - (sum_CT**2)/M) * math.exp(-2*r*T)) / (M - 1))
    standardError = sigma / math.sqrt(M)

    # Create two plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Terminal stock prices for the first 100 simulations.
    axes[0].plot(range(len(sim_paths)), sim_paths, marker='o', linestyle='-')
    axes[0].set_title('Simulated Terminal Stock Prices (First 100 Paths)')
    axes[0].set_xlabel('Simulation Number')
    axes[0].set_ylabel('Stock Price')

    # Plot 2: Convergence Visualization.
    C0 = optionPrice
    SE = standardError
    x1 = np.linspace(C0 - 3*SE, C0 - SE, 100)
    x2 = np.linspace(C0 - SE, C0 + SE, 100)
    x3 = np.linspace(C0 + SE, C0 + 3*SE, 100)
    s1 = stats.norm.pdf(x1, C0, SE)
    s2 = stats.norm.pdf(x2, C0, SE)
    s3 = stats.norm.pdf(x3, C0, SE)
    axes[1].fill_between(x1, s1, color='tab:blue', label='> StDev')
    axes[1].fill_between(x2, s2, color='cornflowerblue', label='1 StDev')
    axes[1].fill_between(x3, s3, color='tab:blue')
    axes[1].plot([C0, C0], [0, max(s2)*1.1], 'k', label='Theoretical Value')
    market_value = optionPrice  
    axes[1].plot([market_value, market_value], [0, max(s2)*1.1], 'r', label='Market Value')
    axes[1].set_xlabel('Option Price')
    axes[1].set_ylabel('Probability')
    axes[1].set_title('Convergence Visualization')
    axes[1].legend()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return jsonify({
        'optionPrice': round(optionPrice, 2),
        'standardError': round(standardError, 2),
        'plot': img_base64
    })

if __name__ == '__main__':
    app.run(debug=True)