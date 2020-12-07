import React, { useEffect, useState } from 'react';
import './Blackjack.css';
import {
  Box, makeStyles, Typography, Button,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';
import BlackjackCard from './BlackjackCard';

const useStyles = makeStyles(() => ({
  dealer: {
    display: 'block',
    height: '30vh',
    width: '100%',
    textAlign: 'center',
  },
  player: {
    display: 'block',
    height: '30vh',
    width: '100%',
    textAlign: 'center',
    bottom: '20px',
  },
  clientUI: {
    display: 'block',
    position: 'relative',
    height: '100%',
    width: '100%',
  },
  playerUI: {
    display: 'block',
    height: '60%',
    width: '100%',
  },
}));

interface Props {
  pool: string;
}

function BlackjackGame(props: Props) {
  const { pool } = props;
  const [playerHand, setPlayerHand] = useState<Array<number|String>>([]);
  const [dealerHand, setDealerHand] = useState<Array<number|String>>([]);
  const [endScreen, setEndScreen] = useState<Boolean>(false);
  const [newPool, setNewPool] = useState<string>('500');
  const [errorMessage, setErrorMessage] = useState<String>('');
  const [effect, seteffect] = useState<String>('');
  const [result, setResult] = useState<string>('');
  const [tie, setTie] = useState<Boolean>(false);
  const history = useHistory();

  function HandleLeave() {
    history.push('/');
  }
  function HandleResult(bust, blackjack, winner) {
    if (bust) {
      seteffect('bust!');
      setResult('Dealer!');
    } else if (blackjack) {
      seteffect('Blackjack!');
      if (winner === 'player') {
        setResult('Player!');
      } else {
        setResult('Tied!');
        setTie(true);
      }
    } else if (winner === 'none') {
      seteffect('Tied!');
      setTie(true);
    } else {
      seteffect('');
      setResult(winner);
    }
    setEndScreen(true);
  }
  function HandleStand(bust, blackjack) {
    fetch('/api/blackjack/stand')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setDealerHand(data.dealer);
          setPlayerHand(data.player);
          HandleResult(bust, blackjack, data.winner);
          setEndScreen(true);
        }
      });
  }
  function HandleNewPool(event) {
    const { value: NewValue } = event.target;
    setNewPool(NewValue);
  }
  function HandlePlayAgain() {
    const num = Number(newPool);
    if (/^\d*$/.test(newPool) === false || Number.isNaN(num)) {
      setErrorMessage('Invalid Input');
    } else if (num < 500) {
      setNewPool('500');
      setErrorMessage('Minimum pool required is 500 tickets');
    } else {
      fetch('/api/blackjack/checkfunds', {
        method: 'POST',
        body: JSON.stringify({
          amount: Number(newPool),
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            fetch('/api/blackjack/playagain', {
              method: 'POST',
              body: JSON.stringify({
                amount: Number(newPool),
              }),
            })
              .then((response) => response.json())
              .then((ndata) => {
                if (ndata.success) {
                  setDealerHand(ndata.dealer);
                  setPlayerHand(ndata.player);
                  if (ndata.blackjack) {
                    HandleStand(false, ndata.blackjack);
                  }
                  setResult('');
                  setEndScreen(false);
                }
              });
          } else {
            setErrorMessage(data.message);
          }
        });
      seteffect('');
    }
  }
  function HandleHit() {
    fetch('/api/blackjack/hit')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          if (data.bust) {
            HandleResult(data.bust, data.blackjack, data.winner);
          } else if (data.blackjack) {
            HandleStand(false, data.blackjack);
          }
          setPlayerHand(data.player);
        }
      });
  }
  function HandleButtonStand() {
    HandleStand(false, false);
  }
  function HandleTie() {
    fetch('/api/blackjack/tiebreaker')
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setDealerHand(data.dealer);
          setPlayerHand(data.player);
          if (data.blackjack) {
            HandleStand(false, data.blackjack);
          }
        }
      });
    setResult('');
    seteffect('');
    setEndScreen(false);
    setTie(false);
  }
  useEffect(() => {
    fetch('/api/blackjack/start', {
      method: 'POST',
      body: JSON.stringify({
        amount: Number(pool),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setDealerHand(data.dealer);
          setPlayerHand(data.player);
          if (data.blackjack) {
            HandleStand(false, data.blackjack);
          }
        }
      });
  }, []);
  const classes = useStyles();
  return (
    <Box className={classes.playerUI}>
      <Box className={classes.dealer}><BlackjackCard hand={dealerHand} /></Box>
      { endScreen
        ? (
          <div className="blackjack-end">
            <Typography variant="h5">
              Winner:&nbsp;
              {result}
            </Typography>
            { tie
              ? (
                <div className="blackjack-tie">
                  <Button onClick={HandleTie} className="blackjack-button-hit">Another Round</Button>
                </div>
              )
              : (
                <div className="blackjack-playagain">
                  <input type="text" defaultValue={newPool} onChange={HandleNewPool} />
                  <div className="error-box">{errorMessage}</div>
                  <Button onClick={HandlePlayAgain} className="blackjack-button-hit">Play Again</Button>
                  <Button onClick={HandleLeave} className="blackjack-logout">Leave</Button>
                </div>
              )}
          </div>
        )
        : (
          <div className="blackjack-play">
            <Button onClick={HandleHit} style={{ right: '5px' }} className="blackjack-button-hit">Hit</Button>
            <Button onClick={HandleButtonStand} className="blackjack-button-hit">Hold</Button>
          </div>
        )}
      <Box className={classes.clientUI}>
        <Typography variant="h6">{effect}</Typography>
        <Box className={classes.player}><BlackjackCard hand={playerHand} /></Box>
      </Box>
    </Box>
  );
}

export default BlackjackGame;
