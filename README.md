# Monte Carlo Option Pricer

A web-based options pricing calculator that uses the Monte Carlo simulation method to estimate European call option prices. The application features real-time stock data fetching, interactive inputs, and visualization of the simulation results.

https://edwinlin11.github.io/option-pricer/

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
