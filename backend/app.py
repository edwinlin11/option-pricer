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

    dt = T
    nudt = (r - 0.5 * vol**2) * dt
    volsdt = vol * math.sqrt(dt)
    lnS = math.log(S)

    sum_CT = 0.0
    sum_CT2 = 0.0
    sim_paths = []  # store all terminal stock prices

    for i in range(M):
        Z = np.random.normal()  # standard normal random variable
        lnST = lnS + nudt + volsdt * Z
        ST = math.exp(lnST)
        CT = max(0, ST - K)  # European call payoff
        sum_CT += CT
        sum_CT2 += CT * CT
        sim_paths.append(ST)  # store every simulated terminal stock price

    # Calculate option price and standard error.
    optionPrice = math.exp(-r * T) * (sum_CT / M)
    sigma = math.sqrt(((sum_CT2 - (sum_CT**2)/M) * math.exp(-2*r*T)) / (M - 1))
    standardError = sigma / math.sqrt(M)

    # Create a histogram of simulated terminal stock prices.
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(sim_paths, bins=30, edgecolor='black', alpha=0.7)
    ax.set_title("Histogram of Simulated Terminal Stock Prices")
    ax.set_xlabel("Terminal Stock Price")
    ax.set_ylabel("Frequency")

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