/* eslint-disable import/prefer-default-export */
import { makeStyles, Theme } from '@material-ui/core';

export const useStyles = makeStyles((theme: Theme) => ({
  root: {
    flexGrow: 1,
    color: 'white',
    background: 'none',
    boxShadow: 'none',
    display: 'flex',
    flexDirection: 'column',
    flexWrap: 'wrap',
    position: 'relative',
    top: '7vh',
    alignItems: 'center',
    width: '100%',
    margin: 'auto',
    padding: '8px',
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  stepper: {},
  table: {
    textAlign: 'center',
    margin: 'auto',
  },
  tableRow: {
    textDecoration: 'none',
  },
  card: {
    minWidth: 275,
    margin: theme.spacing(1),
  },
  media: {
    height: 140,
  },
  form: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  toolbar: {
    minHeight: 128,
    alignItems: 'flex-start',
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(2),
  },
  withoutLabel: {
    marginTop: theme.spacing(3),
    width: '200px',
    marginLeft: 'auto',
    marginRight: 'auto',
  },
  textField: {
    width: '200px',
    marginLeft: 'auto',
    marginRight: 'auto',
    background: '#fff',
    color: '#000',
    paddingLeft: '15px',
  },
  headButton: {
    backgroundColor: '#aa9549',
    padding: '7px 18px',
    borderRadius: '30px',
  },
  tailButton: {
    backgroundColor: '#aa9549',
    padding: '7px 23px',
    borderRadius: '30px',
  },
  betNowButton: {
    backgroundColor: '#aa9549',
    padding: '7px 30px',
    borderRadius: '30px',
  },
}));
