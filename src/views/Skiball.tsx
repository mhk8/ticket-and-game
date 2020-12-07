import React, { useState } from 'react';
import './Skiball.css';
import {
  Button, Typography,
} from '@material-ui/core';

function Skiball() {
  const [message, setMessage] = useState('');

  function play() {
    fetch('/api/skiball')
      .then((response) => {
        if (response.status === 200) {
          response.json()
            .then((dataResponse) => {
              const { amount } = dataResponse;
              setMessage(`You won ${amount} tickets!`);
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
  }

  return (
    <div className="Skiball">
      <div>
        <Typography variant="h3">
          Skiball
        </Typography>
        <br />
        <Typography variant="h5" style={{ margin: 'auto', textAlign: 'center' }}> Click on roll ball and see where it lands! You win as many tickets as the point amount on the hole. </Typography>
        <br />
        <Typography variant="h5">Takes 30 tickets to play!</Typography>
        <br />
        <img
          src="https://media0.giphy.com/media/26gsqnn8rZOSiVFfy/200.gif"
          alt="coinflip"
          className="coinflipgif"
          style={{
            height: '250px', width: '300px', borderStyle: 'solid', borderWidth: '2px',
          }}
        />
        <br />
        <br />
        <Typography variant="h6">Go ahead and roll:</Typography>
        <br />
        <Button variant="contained" type="button" onClick={play}>Roll!</Button>
        <br />
        <p>{message}</p>
        <br />
      </div>
    </div>
  );
}
export default Skiball;
