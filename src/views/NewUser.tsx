import React, { useState } from 'react';
import { Typography, Button } from '@material-ui/core';
import { useHistory } from 'react-router-dom';

interface Props {
  setUserId: (isLoggedIn: string) => void
}

function NewUser(props: Props) {
  const { setUserId } = props;
  const history = useHistory();
  const [username, setUsername] = useState('');
  const [eMessage, setEMessage] = useState('');
  function handleUsername(event) {
    const { value: NewValue } = event.target;
    setUsername(NewValue);
  }
  function handleSubmit() {
    const tusername = username.trim();
    if (tusername === '') setEMessage('Username field must be filled');
    else {
      fetch('/api/login/newuser', {
        method: 'POST',
        headers: new Headers({ 'content-type': 'application/json' }),
        mode: 'no-cors',
        body: JSON.stringify({ user: tusername }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            setUserId(data.user_id);
            history.push('/');
          } else setEMessage(data.message);
        })
        .catch((error) => {
          <div className="new-user-error-box">
            Malformed message was recieved:
            {error}
          </div>;
        });
    }
  }
  return (
    <div>
      <Typography variant="h3">
        Welcome to Ticket and Games. Please enter an username.
      </Typography>
      <div className="form-label">
        <Typography variant="h6">
          Username
        </Typography>
      </div>
      <input
        type="text"
        name="username"
        className="new-user-username"
        defaultValue={username}
        onChange={handleUsername}
        autoComplete="off"
      />
      <Button variant="contained" value="Submit" onClick={handleSubmit}>Submit</Button>
      <div>{eMessage}</div>
    </div>
  );
}

export default NewUser;
