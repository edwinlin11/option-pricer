# Monte Carlo Option Pricer

A web-based options pricing calculator that uses the Monte Carlo simulation method to estimate European call option prices. The application features real-time stock data fetching, interactive inputs, and visualization of the simulation results.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/b4fd472a-caa8-4f1c-848a-dd4102b297cf" />


## Features

- **Real-time Stock Data**: Fetch current stock prices and volatility data for any ticker symbol
- **Monte Carlo Simulation**: Price European call options using Monte Carlo methods
- **Interactive Visualization**: View the distribution of simulated terminal stock prices
- **Error Analysis**: Calculate and display standard error of the price estimate
- **User-Friendly Interface**: Clean, responsive design built with React and Tailwind CSS

## Technical Stack

### Frontend
- React.js
- Tailwind CSS
- shadcn/ui components
- Lucide React icons
- Hosted on GitHub Pages

### Backend
- Python/Flask
- NumPy for numerical computations
- yfinance for real-time market data
- Matplotlib for visualization
- Hosted on PythonAnywhere

## How It Works

1. **Stock Data Fetching**
   - Enter a stock ticker (e.g., AAPL)
   - Click "Fetch" to get current price and volatility data
   - Data is retrieved using the yfinance API

2. **Option Parameters**
   - Stock Price: Current or custom stock price
   - Strike Price: The option's strike price
   - Time to Expiry: Number of days until expiration
   - Volatility: Annualized volatility (%)
   - Risk-Free Rate: Annual risk-free interest rate (%)
   - Number of Iterations: Simulation sample size

3. **Monte Carlo Simulation**
   - Simulates multiple stock price paths
   - Calculates option payoffs at expiration
   - Averages discounted payoffs to estimate option price
   - Visualizes the distribution of terminal stock prices

## Installation and Setup

### Frontend
```bash
# Clone the repository
git clone https://github.com/yourusername/monte-carlo-option-pricer
cd monte-carlo-option-pricer

# Install dependencies
npm install

# Start development server
npm run dev

# Deploy to GitHub Pages
npm run deploy
```

### Backend
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install flask numpy yfinance matplotlib scipy flask-cors

# Start the Flask server
python app.py
```

## API Endpoints

### GET /stock-data/{ticker}
Fetches current stock price and volatility data.

Response:
```json
{
    "success": true,
    "price": 180.5,
    "volatility": 25.3
}
```

### POST /option-pricing
Calculates option price using Monte Carlo simulation.

Request body:
```json
{
    "ticker": "AAPL",
    "stockPrice": 180.5,
    "strikePrice": 185,
    "timeToExpiry": 40,
    "volatility": 25.3,
    "riskFreeRate": 2.5,
    "iterations": 1000
}
```

Response:
```json
{
    "optionPrice": 5.23,
    "standardError": 0.15,
    "plot": "base64_encoded_image"
}
```
