import React, { Dispatch, useEffect, useState } from 'react';

import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { Link } from 'react-router-dom';
import {
  Box, Button, Paper, Stepper, Step, StepLabel, Typography,
} from '@material-ui/core';

import { useDispatch } from 'react-redux';
import { MessageActions, ADD_MESSAGE } from '../actions/messageActions';
import { useStyles } from '../styles';

import TicketPurchaseSelector from '../components/TicketPurchaseSelector';

import './TicketPurchase.css';

type Item = {
  tickets: number,
  price: number,
};

function getSteps() {
  return ['Select number of tickets to purchase', 'Enter payment details', 'Complete'];
}

function TicketPurchase() {
  const stripe = useStripe();
  const elements = useElements();
  const [clientSecret, setClientSecret] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const [activeItem, setActiveItem] = useState(-1);
  const [items, setItems] = useState<Array<Item>>([]);
  const steps = getSteps();
  const classes = useStyles();

  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();

  const done = activeStep === steps.length - 1;

  useEffect(() => {
    if (activeStep === 1) {
      fetch('/api/purchase/payment-intent', {
        method: 'POST',
        body: JSON.stringify({
          item_index: activeItem,
        }),
      }).then((response) => {
        response.json().then((data) => {
          setClientSecret(data.client_secret);
        });
      });
    }
  }, [activeStep]);

  useEffect(() => {
    fetch('/api/purchase/list').then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          setItems(data.items);
        });
      } else {
        messagesDispatch({
          type: ADD_MESSAGE,
          payload: {
            message: 'Unknown error occured fetching ticket list',
            type: 'error',
          },
        });
      }
    });
  }, []);

  const handlePay = async () => {
    if (!stripe || !elements) {
      return;
    }

    const cardElement = elements.getElement(CardElement);

    if (cardElement !== null) {
      const payload = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: cardElement,
        },
      });

      if (payload.error) {
        messagesDispatch({
          type: ADD_MESSAGE,
          payload: {
            message: payload.error.message ?? 'Unknown stripe error',
            type: 'error',
          },
        });
      } else {
        messagesDispatch({
          type: ADD_MESSAGE,
          payload: {
            message: 'Tickets purchased successfully',
            type: 'success',
          },
        });
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
      }
    }
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const getStepContent = (stepIndex: number) => {
    switch (stepIndex) {
      case 0:
        return (
          <TicketPurchaseSelector
            activeItem={activeItem}
            setActiveItem={setActiveItem}
            items={items}
          />
        );
      case 1:
        return (
          <Box style={{ width: '50%' }}>
            <form className={classes.form}>
              <CardElement
                options={{
                  hidePostalCode: true,
                }}
              />
            </form>
          </Box>
        );
      case 2:
        return <Typography>Thank your for your purchase!</Typography>;
      default:
        return <Typography>Unknown step.</Typography>;
    }
  };

  return (
    <Paper className={classes.root}>
      <Stepper className={classes.stepper} activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      {getStepContent(activeStep)}
      { !done ? (
        <Box>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
          >
            Back
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={(activeStep === steps.length - 2) ? handlePay : handleNext}
          >
            {activeStep === steps.length - 2 ? 'Pay' : 'Next'}
          </Button>
        </Box>
      )
        : (
          <Button
            variant="contained"
            color="primary"
            component={Link}
            to="/"
          >
            Back to Home
          </Button>
        ) }
    </Paper>
  );
}

export default TicketPurchase;
