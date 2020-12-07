import React, { Dispatch, useState } from 'react';
import { Button, TextField, Typography } from '@material-ui/core';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

import { useDispatch } from 'react-redux';
import { MessageActions, ADD_MESSAGE } from '../actions/messageActions';

const useStyles = makeStyles((theme: Theme) => createStyles({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    },
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
}));

function TicketTransfer() {
  const classes = useStyles();

  const [amount, setAmount] = useState<number>();
  const [recipientId, setRecipientId] = useState<number>();
  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();

  const transferTicket = () => {
    fetch('/api/ticket/transfer', {
      headers: {
        'Content-Type': 'application/json',
      },
      method: 'POST',
      body: JSON.stringify({ to: recipientId, amount }),
    }).then((response) => {
      response.json().then((data) => {
        if (response.status === 200) {
          messagesDispatch({
            type: ADD_MESSAGE,
            payload: {
              message: `Sent ${data.amount} to user id ${data.user_id}`,
              type: 'success',
            },
          });
        } else {
          messagesDispatch({
            type: ADD_MESSAGE,
            payload: {
              message: data.error,
              type: 'error',
            },
          });
        }
      });
    });
  };

  const amountOnChange = (e) => {
    setAmount(Number(e.target.value));
  };

  const recipientOnChange = (e) => {
    setRecipientId(Number(e.target.value));
  };

  return (
    <div>
      <Typography variant="h4" component="h4">
        Transfer points
      </Typography>
      <form className={classes.root} autoComplete="off">
        <TextField id="transfer-recipient" label="Recipient ID" type="number" onChange={recipientOnChange} variant="filled" />
        <TextField
          id="transfer-amount"
          label="Amount"
          type="number"
          value={amount}
          onChange={amountOnChange}
          variant="filled"
        />
        <Button size="large" variant="contained" onClick={transferTicket}>
          Transfer
        </Button>
      </form>
    </div>
  );
}

export default TicketTransfer;
