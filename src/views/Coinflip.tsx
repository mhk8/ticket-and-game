import React, { useState } from 'react';
import './Coinflip.css';
import {
  Box,
  Button,
  ButtonGroup,
  Paper,
  Typography,
  Input,
  FormControl,
} from '@material-ui/core';
import { useStyles } from '../styles';
import CoinflipImage from '../assets/image/coin.gif';

function Coinflip() {
  const classes = useStyles();
  const [bet, setBet] = useState(0);
  const [value, setValue] = useState(0);
  const [message, setMessage] = useState('');

  const onChange = (event) => {
    let goal = 0;
    if (event.target.value !== '') {
      goal = parseInt(event.target.value, 10);
      setBet(goal);
      setValue(goal * 2);
    } else {
      setBet(0);
      setValue(0);
    }
  };

  const play = (side: 'Tails' | 'Heads') => {
    const data = { side, bet };
    fetch('/api/coinflip', {
      method: 'POST',
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.status === 200) {
          response.json()
            .then((dataResponse) => {
              const { amount, won } = dataResponse;
              const winText = won ? 'won' : 'lost';
              setMessage(`You ${winText} ${amount} tickets`);
            });
        } else {
          response.json().then((error) => {
            setMessage(`An error occured: ${error.error}`);
          });
        }
      })
      .catch((error) => {
        setMessage(`An error occured: ${error}`);
      });
  };

  function onHeads() {
    play('Heads');
  }

  function onTails() {
    play('Tails');
  }
  // send over data with the head/tail, bet amount

  return (
    <div className="Coinflip">
      <Paper style={{ background: 'none', color: 'white', boxShadow: 'none' }}>
        <br />
        <Typography variant="h3">
          Coinflip
        </Typography>
        <br />
        <Typography variant="h5"> Enter an amount you would like to wager. </Typography>
        <Typography variant="h5">
          If you win, you win&nbsp;
          <span className="golden">{value}</span>
          tickets. If you lose, you lose&nbsp;
          <span className="golden">{bet}</span>
          tickets you bet.
        </Typography>
        <img src={CoinflipImage} alt="Coin Flip" className="coinflipgif" />
        <br />
        <Typography variant="h6">Place a Bet in Number of Tickets:</Typography>
        <br />
        <FormControl fullWidth>
          <Input
            id="standard-adornment-amount"
            className={classes.textField}
            value={bet}
            onChange={onChange}
          />
        </FormControl>
        <br />
        <br />
        <Typography variant="h6">Choose heads or tails:</Typography>
        <br />
        <Box>
          <ButtonGroup variant="text" color="primary" aria-label="text primary button group">
            <Button variant="contained" type="button" className={classes.headButton} style={{ right: '10px' }} onClick={onHeads}>Heads</Button>
            <Button variant="contained" type="button" className={classes.tailButton} onClick={onTails}>Tails</Button>
          </ButtonGroup>
        </Box>
        <br />
        <br />
        <p>{message}</p>
      </Paper>
    </div>
  );
}
export default Coinflip;
