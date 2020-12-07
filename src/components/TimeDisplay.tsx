import React from 'react';
import { Tooltip, Typography } from '@material-ui/core';
import { humanizeSeconds } from '../utils/time';

type Props = {
  time: string,
};

function TimeDisplay(props: Props) {
  const { time } = props;

  const datetime = new Date(time);

  return (
    <Tooltip title={datetime.toLocaleString()}>
      <Typography variant="inherit">
        { humanizeSeconds(datetime) }
      </Typography>
    </Tooltip>
  );
}

export default TimeDisplay;
