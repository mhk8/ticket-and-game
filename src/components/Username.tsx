import React, { useState } from 'react';
import {
  Button, Typography, TextField,
} from '@material-ui/core';

interface Props {
  valid: boolean,
}

function Username(props: Props) {
  const { valid } = props;
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');

  function HandleUsername(event) {
    setUsername(event.target.value);
  }

  function SubmitUsername() {
    const tusername = username;
    fetch('/api/settings/username', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        username: tusername,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message);
      });
  }

  if (valid) {
    return (
      <div style={{ textAlign: 'center' }}>
        <Typography variant="h6">Change Username</Typography>
        <TextField
          color="primary"
          variant="outlined"
          size="small"
          defaultValue={username}
          onChange={HandleUsername}
        />
        <Button color="primary" variant="contained" onClick={SubmitUsername}>Confirm</Button>
        <div>{message}</div>
      </div>
    );
  }
  return <div />;
}

export default Username;
