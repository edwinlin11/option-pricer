import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Alert } from '../components/ui/alert';
import { Search } from 'lucide-react';


const OptionPricer = () => {
  const [inputs, setInputs] = useState({
    ticker: '',
    stockPrice: 100,      // fallback if no ticker data is found
    strikePrice: 100,
    timeToExpiry: 40,     // in days
    volatility: 20,       // in percent
    riskFreeRate: 2.5,    // in percent
    iterations: 1000
  });
  const [results, setResults] = useState(null);
  const [plotImg, setPlotImg] = useState('');
  const [error, setError] = useState(null);

  // (Optional) Function to fetch ticker data manually if desired.
  const fetchStockData = async (ticker) => {
    try {
      setError(null);
      const response = await fetch(`https://edwinlin.pythonanywhere.com/stock-data/${ticker}`);
      const data = await response.json();
      if (data.success) {
        setInputs(prev => ({
          ...prev,
          stockPrice: data.price,
          volatility: data.volatility
        }));
      } else {
        setError('Failed to fetch stock data');
      }
    } catch (err) {
      setError('Error fetching stock data');
      console.error(err);
    }
  };

  // Calls the Python backend which performs the simulation and returns results/plots.
  const calculateOptionPrice = async () => {
    const payload = {
    ticker: inputs.ticker,
    stockPrice: Number(inputs.stockPrice),
    strikePrice: Number(inputs.strikePrice),
    timeToExpiry: Number(inputs.timeToExpiry),
    volatility: Number(inputs.volatility),
    riskFreeRate: Number(inputs.riskFreeRate),
    iterations: Number(inputs.iterations),
    };

    try {
      setError(null);
      const response = await fetch('https://edwinlin.pythonanywhere.com/option-pricing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (data) {
        setResults({
          optionPrice: data.optionPrice,
          standardError: data.standardError
        });
        // data.plot is a base64-encoded PNG image generated by Python.
        setPlotImg(data.plot);
      }
    } catch (err) {
      setError('Error calculating option price');
      console.error(err);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Monte Carlo Option Pricer</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4 mb-4">
            <div className="flex-grow">
              <label className="block mb-1">Stock Ticker:</label>
              <div className="flex gap-2">
                <Input
                  type="text"
                  value={inputs.ticker}
                  onChange={(e) =>
                    setInputs({ ...inputs, ticker: e.target.value.toUpperCase() })
                  }
                  placeholder="Enter ticker (e.g., AAPL)"
                />
                <Button onClick={() => fetchStockData(inputs.ticker)}>
                  <Search className="w-4 h-4 mr-2" />
                  Fetch
                </Button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block mb-1">Stock Price:</label>
              <Input
                type="number"
                value={inputs.stockPrice}
                onChange={(e) =>
                  setInputs({ ...inputs, stockPrice: e.target.value })
                }
              />
            </div>
            <div>
              <label className="block mb-1">Strike Price:</label>
              <Input
                type="number"
                value={inputs.strikePrice}
                onChange={(e) =>
                  setInputs({ ...inputs, strikePrice: e.target.value })
                }
              />
            </div>
            <div>
              <label className="block mb-1">Time to Expiry (Days):</label>
              <Input
                type="number"
                value={inputs.timeToExpiry}
                onChange={(e) =>
                  setInputs({ ...inputs, timeToExpiry: e.target.value })
                }
              />
            </div>
            <div>
              <label className="block mb-1">Volatility (%):</label>
              <Input
                type="number"
                value={inputs.volatility}
                onChange={(e) =>
                  setInputs({ ...inputs, volatility: e.target.value })
                }
              />
            </div>
            <div>
              <label className="block mb-1">Risk-Free Rate (%):</label>
              <Input
                type="number"
                value={inputs.riskFreeRate}
                onChange={(e) =>
                  setInputs({ ...inputs, riskFreeRate: e.target.value })
                }
              />
            </div>
            <div>
              <label className="block mb-1">Number of Iterations:</label>
              <Input
                type="number"
                value={inputs.iterations}
                onChange={(e) =>
                  setInputs({ ...inputs, iterations: e.target.value })
                }
              />
            </div>
          </div>

          {error && (
            <Alert className="mb-4" variant="destructive">
              {error}
            </Alert>
          )}

          <Button className="w-full mb-4" onClick={calculateOptionPrice}>
            Calculate Option Price
          </Button>

          {results && (
            <Alert className="mb-4">
              <p>Option Price: ${results.optionPrice}</p>
              <p>Standard Error: ±${results.standardError}</p>
            </Alert>
          )}

          {plotImg && (
            <div className="mb-4">
              <img src={`data:image/png;base64,${plotImg}`} alt="Simulation Plot" />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default OptionPricer;