import React from 'react';

import { useHistory } from 'react-router-dom';

type Props = {
  loggedIn: boolean,
  children: React.ReactNode,
};

export default function AuthRequired(props: Props) {
  const { loggedIn, children } = props;
  const history = useHistory();

  if (!loggedIn) {
    history.push('/login');
  }

  return (
    <>{loggedIn ? children : null}</>
  );
}
