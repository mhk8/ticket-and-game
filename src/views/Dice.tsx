import React, { useState } from 'react';
import './Dice.css';
import {
  Box,
  Button,
  FormControl,
  Input,
  Paper,
  Typography,
  Select,
  MenuItem,
} from '@material-ui/core';
import DiceImage from '../assets/image/dice1.gif';

import { useStyles } from '../styles';

function Dice() {
  const [bet, setBet] = useState(1);
  const [goal, setGoal] = useState(4);
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState('');
  const [open, setOpen] = React.useState(false);
  const onChange = (event) => {
    setMessage('');
    if (event.target.name === 'quantity') {
      let current = 0;
      if (event.target.value !== '') {
        current = parseInt(event.target.value, 10);
        setQuantity(current);
        setGoal(current * 4);
      } else {
        setQuantity(1);
        setGoal(4);
      }
    } else {
      setBet(parseInt(event.target.value, 10));
    }
  };

  const play = () => {
    const data = { bet, quantity };
    fetch('/api/dice', {
      method: 'POST',
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.status === 200) {
          response.json()
            .then((dataResponse) => {
              const { amount, won, value } = dataResponse;
              const winText = won ? 'won' : 'lost';
              setMessage(`The side drawn is ${value} and you have ${winText} ${amount} tickets because you selected ${bet}`);
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

  function onBet() {
    play();
  }
  // send over data with the head/tail, bet amount
  const handleChange = (event) => {
    setBet(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const classes = useStyles();
  return (
    <div className="Dice">
      <Paper className={classes.root}>
        <Typography variant="h3">
          Dice
        </Typography>
        <br />
        <Typography variant="h5"> Enter the amount of Ticket and the side you want. </Typography>
        <Typography variant="h5">
          If you win you will take&nbsp;
          <span className="golden">{goal}</span>
          s Tickets.
        </Typography>
        <img src={DiceImage} alt="Dice Game" className="dicegif" style={{ height: '200px' }} />
        <br />
        <Typography variant="h6">Entry number of tickets and select a side of dice:</Typography>
        <br />
        <FormControl fullWidth>
          <Input
            id="standard-adornment-amount"
            className={classes.textField}
            value={quantity}
            onChange={onChange}
            name="quantity"
          />
        </FormControl>
        <Select
          labelId="demo-controlled-open-select-label"
          id="demo-controlled-open-select"
          open={open}
          onClose={handleClose}
          onOpen={handleOpen}
          value={bet}
          onChange={handleChange}
        >
          <MenuItem value="1">Face1</MenuItem>
          <MenuItem value="2">Face2</MenuItem>
          <MenuItem value="3">Face3</MenuItem>
          <MenuItem value="4">Face4</MenuItem>
          <MenuItem value="5">Face5</MenuItem>
          <MenuItem value="6">Face6</MenuItem>
        </Select>
        <br />
        <Box>
          <Button variant="contained" color="primary" type="button" onClick={onBet} className={classes.betNowButton}>Bet Now</Button>
        </Box>
        <br />
        <br />
        <p>{message}</p>
      </Paper>
    </div>
  );
}
export default Dice;
