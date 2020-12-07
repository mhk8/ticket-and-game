import React, { Dispatch } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

import { Box, Container } from '@material-ui/core';
import { Alert } from '@material-ui/lab';

import { AppState } from './reducers';
import { MessageActions, DELETE_MESSAGE } from './actions/messageActions';

import './App.css';
import AppHeader from './AppHeader';
import Leaderboard from './views/Leaderboard';
import Profileview from './views/Profileview';
import Login from './views/Login';
import Coinflip from './views/Coinflip';
import Signup from './views/Signup';
import Blackjack from './views/Blackjack';
import Home from './views/Home';
import Skiball from './views/Skiball';
import Store from './views/Store';
import TicketPurchase from './views/TicketPurchase';
import AuthRequired from './components/AuthRequired';
import NewUser from './views/NewUser';

import { useLocalStorage } from './utils/hooks';
import Settings from './views/Settings';
import Dice from './views/Dice';

function App() {
  const [userId, setUserId] = useLocalStorage('userId', '');
  const messages = useSelector((state: AppState) => state.messages);
  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();

  const loggedIn = Boolean(userId);

  return (
    <Router>
      <AppHeader loggedIn={loggedIn} setUserId={setUserId} />
      <link rel="preconnect" href="https://fonts.gstatic.com" />
      <link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Pathway+Gothic+One&display=swap" rel="stylesheet" />
      <Switch>
        {/* Private routes that do require login */}
        <Route path="/profile/:userId?" defaultParams={{ userId: '' }}>
          <AuthRequired loggedIn={loggedIn}>
            <Container>
              <Box>
                <Profileview />
              </Box>
            </Container>
          </AuthRequired>
        </Route>
        <Route path="/coinflip">
          <AuthRequired loggedIn={loggedIn}>
            <Coinflip />
          </AuthRequired>
        </Route>
        <Route path="/dice">
          <AuthRequired loggedIn={loggedIn}>
            <Dice />
          </AuthRequired>
        </Route>
        <Route path="/skiball">
          <AuthRequired loggedIn={loggedIn}>
            <Skiball />
          </AuthRequired>
        </Route>
        <Route path="/blackjack">
          <AuthRequired loggedIn={loggedIn}>
            <Blackjack />
          </AuthRequired>
        </Route>
        <Route path="/store">
          <AuthRequired loggedIn={loggedIn}>
            <Container>
              <Box>
                <Store />
              </Box>
            </Container>
          </AuthRequired>
        </Route>
        <Route path="/purchase">
          <AuthRequired loggedIn={loggedIn}>
            <Container>
              <Box>
                <TicketPurchase />
              </Box>
            </Container>
          </AuthRequired>
        </Route>
        <Route path="/settings">
          <AuthRequired loggedIn={loggedIn}>
            <Container>
              <Box>
                <Settings />
              </Box>
            </Container>
          </AuthRequired>
        </Route>

        {/* Public routes that don't require login */}
        <Route path="/leaderboard">
          <Container>
            <Box>
              <Leaderboard />
            </Box>
          </Container>
        </Route>
        <Route path="/login">
          <Container>
            <Box>
              <Login setUserId={setUserId} />
            </Box>
          </Container>
        </Route>
        <Route path="/signup">
          <Container>
            <Box>
              <Signup setLoggedIn={setUserId} />
            </Box>
          </Container>
        </Route>
        <Route path="/newuser">
          <Container>
            <Box>
              <NewUser setUserId={setUserId} />
            </Box>
          </Container>
        </Route>
        <Route path="/">
          <Container>
            <Box>
              <Home />
            </Box>
          </Container>
        </Route>
      </Switch>
      <Container>
        <Box>
          {messages.map((error) => (
            <Alert
              severity={error.type}
              onClose={() => messagesDispatch({
                type: DELETE_MESSAGE,
                payload: {
                  id: error.id,
                },
              })}
            >
              {error.message}
            </Alert>
          ))}
        </Box>
      </Container>
    </Router>
  );
}

export default App;
