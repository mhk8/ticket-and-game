import React from 'react';
import { render } from '@testing-library/react';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import rootReducer from './reducers';

import App from './App';

const store = createStore(rootReducer);

test('renders without error', () => {
  render(<Provider store={store}><App /></Provider>);
});
