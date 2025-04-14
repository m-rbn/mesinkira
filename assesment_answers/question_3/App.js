import ReactDOM from 'react-dom';
import React, { useState } from 'react';

const App = () => {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendRequest = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('https://your-api-endpoint.com/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: 'test_user_input' })
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Prediction API Test</h1>
      <button onClick={sendRequest} disabled={loading}>
        {loading ? 'Loading...' : 'Send a request to endpoint'}
      </button>
      <div>
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        {response && (
          <pre>
            {JSON.stringify(response, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));