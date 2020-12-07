import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Paper, Typography, Button,
} from '@material-ui/core';
import 'fontsource-roboto';

import { useStyles } from '../styles';

interface Props {
  setLoggedIn: (isLoggedIn: boolean) => void;
}

function Signup(props: Props) {
  const { setLoggedIn } = props;
  const history = useHistory();
  const [params, setParams] = useState({
    name: '',
    username: '',
    email: '',
    password1: '',
    password2: '',
  });
  const [eMessage, setEMessage] = useState('');
  function SigningUp() {
    const tname = params.name.trim();
    const tusername = params.username.trim();
    const temail = params.email.trim();
    const tpassword1 = params.password1.trim();
    const tpassword2 = params.password2.trim();

    if (tname === '' || tusername === '' || temail === ''
      || tpassword1 === '' || tpassword2 === '') setEMessage('Please fill in all fields.');
    else if (tpassword1 !== tpassword2) setEMessage('Passwords do not match. Please try again.');
    else {
      fetch('/api/signup/password', {
        method: 'POST',
        headers: new Headers({ 'content-type': 'application/json' }),
        mode: 'no-cors',
        body: JSON.stringify({
          name: tname,
          username: tusername,
          email: temail,
          password: tpassword1,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            setLoggedIn(true);
            history.push('/profile');
          } else setEMessage(data.message);
        })
        .catch((error) => {
          <div className="signup-error-box">
            Malformed message was recieved:
            {error}
          </div>;
        });
    }
  }
  function handleParams(event) {
    const { value: NewValue } = event.target;
    setParams({
      ...params,
      [event.target.name]: NewValue,
    });
  }
  const classes = useStyles();
  return (
    <div className="sign-form-box">
      <Paper className={classes.root}>
        <form className="signup-form">
          <div className="form-label">Name</div>
          <input
            type="text"
            name="name"
            className="signup-name"
            defaultValue={params.name}
            onChange={handleParams}
            autoComplete="off"
          />
          <div className="form-label">
            <Typography variant="h6">
              Username
            </Typography>
          </div>
          <input
            type="text"
            name="username"
            className="signup-username"
            defaultValue={params.username}
            onChange={handleParams}
            autoComplete="off"
          />
          <div className="form-label">
            <Typography variant="h6">
              Email
            </Typography>
          </div>
          <input
            type="text"
            name="email"
            className="signup-email"
            defaultValue={params.email}
            onChange={handleParams}
            autoComplete="off"
          />
          <div className="form-label">
            <Typography variant="h6">
              Password
            </Typography>
          </div>
          <input
            type="password"
            name="password1"
            className="signup-password"
            defaultValue={params.password1}
            onChange={handleParams}
            autoComplete="off"
          />
          <div className="form-label">
            <Typography variant="h6">
              Enter Password Again
            </Typography>
          </div>
          <input
            type="password"
            name="password2"
            className="signup-password"
            defaultValue={params.password2}
            onChange={handleParams}
            autoComplete="off"
          />
        </form>
        <Button variant="contained" value="Submit" onClick={SigningUp}>Submit</Button>
        <div className="signup-error-box">{eMessage}</div>
      </Paper>
    </div>
  );
}

export default Signup;
