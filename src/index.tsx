import React from 'react';
import ReactDOM from 'react-dom';

import { createStore } from 'redux';
import { Provider } from 'react-redux';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';

import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import rootReducer from './reducers';

import App from './App';
import reportWebVitals from './reportWebVitals';

const darkTheme = createMuiTheme({
  palette: {
    type: 'dark',
  },
});

const store = createStore(rootReducer);
const rootElement = document.getElementById('root');

const stripePromise = loadStripe('pk_test_51HseN4AEuYim4mUyZxsKMzK8vBtG8gB91HjoAi09qb6OHfqEz6WARLYu8MA1I5ywcNOs2txEVwy8g2SmpRl2f3Nm00RPwSNMz7');

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <Provider store={store}>
        <Elements stripe={stripePromise}>
          <App />
        </Elements>
      </Provider>
    </ThemeProvider>
  </React.StrictMode>,
  rootElement,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
