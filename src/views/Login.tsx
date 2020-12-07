import React, { useState } from 'react';
import { GoogleLogin } from 'react-google-login';
import { useHistory } from 'react-router-dom';
import {
  Paper, Typography, Button,
} from '@material-ui/core';
import 'fontsource-roboto';

import { useStyles } from '../styles';

interface Props {
  setUserId: (isLoggedIn: string) => void;
}

export default function Login(props: Props) {
  const { setUserId } = props;
  const history = useHistory();
  const [loginMessage, setLoginMessage] = useState('');
  const [login, setLogin] = useState({
    username: '',
    password: '',
  });

  function GoToSignUp() {
    history.push('/signup');
  }

  function PerformLogin() {
    const tusername = login.username.trim();
    const tpassword = login.password.trim();

    if (tusername === '' || tpassword === '') {
      setLoginMessage('Please fill in both fields.');
    } else {
      fetch('/api/login/password', {
        method: 'POST',
        headers: new Headers({ 'content-type': 'application/json' }),
        mode: 'no-cors',
        body: JSON.stringify({
          username: tusername,
          password: tpassword,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            setUserId(data.user_id);
            history.push('/');
          } else setLoginMessage(data.message);
        })
        .catch((error) => {
          <div className="login-error-box">
            Malformed message was recieved:
            {error}
          </div>;
        });
    }
  }

  function handleLogin(event) {
    const { value: NewValue } = event.target;
    setLogin({
      ...login,
      [event.target.name]: NewValue,
    });
  }

  function googleLogin(googleUser: any) {
    fetch('/api/login/oauth', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({ token: googleUser?.tokenId }),
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          if (data.new_user) {
            history.push('/newuser');
          } else {
            setUserId(data.user_id);
            history.push('/');
          }
        });
      }
    });
  }
  const classes = useStyles();
  return (
    <div className="LoginBox">
      <Paper className={classes.root}>
        <div className="Login">
          <div className="login-password">
            <form>
              <div className="form-label">
                <Typography variant="h6">
                  Username
                </Typography>
              </div>
              <input
                type="text"
                name="username"
                className="login-username"
                defaultValue={login.username}
                onChange={handleLogin}
                autoComplete="off"
              />
              <div className="form-label">
                <Typography variant="h6">
                  Password
                </Typography>
              </div>
              <input
                type="password"
                name="password"
                className="login-password"
                defaultValue={login.password}
                onChange={handleLogin}
                autoComplete="off"
              />
            </form>
          </div>
          <br />
          <Button variant="contained" style={{ position: 'relative', right: '1vh' }} value="Login" onClick={PerformLogin}>Login</Button>
          <Button variant="contained" value="Signup" onClick={GoToSignUp}>Sign Up</Button>
          <div>{loginMessage}</div>
          <br />
          <hr />
          <br />
          <Typography variant="h6">
            Google Login
          </Typography>
          <br />
          <GoogleLogin
            clientId="154638215001-5tdj4ttljsh2c3m5uojmq7nrruock21s.apps.googleusercontent.com"
            buttonText="Login"
            onSuccess={googleLogin}
            cookiePolicy="single_host_origin"
            isSignedIn
          />
        </div>
        <br />
      </Paper>
    </div>
  );
}
