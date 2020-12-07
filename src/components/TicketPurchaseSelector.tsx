import React from 'react';
import {
  Box, Card, CardHeader, Radio,
} from '@material-ui/core';

import { useStyles } from '../styles';

type Item = {
  tickets: number,
  price: number,
};

type Props = {
  activeItem: number | null,
  setActiveItem: (activeItem: number) => void,
  items: Array<Item>,
};

function TicketPurchaseSelector(props: Props) {
  const { activeItem, setActiveItem, items } = props;

  const classes = useStyles();

  return (
    <Box justifyContent="center" display="flex" flexDirection="row" flexWrap="wrap">
      { items.map((item, index) => (
        <Card className={classes.card} key={item.tickets} onClick={() => setActiveItem(index)}>
          <CardHeader
            action={(
              <Radio checked={index === activeItem} onClick={() => setActiveItem(index)} />
            )}
            title={`${item.tickets.toLocaleString()} tickets`}
            subheader={`${item.price.toLocaleString(undefined, { style: 'currency', currency: 'USD' })}`}
          />
        </Card>
      ))}
    </Box>
  );
}

export default TicketPurchaseSelector;
