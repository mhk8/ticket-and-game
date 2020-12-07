import React, { useState, useEffect } from 'react';
import './Leaderboard.css';
import {
  Paper, Typography, CircularProgress, Table, TableBody, TableCell,
  TableHead, TableRow, TableContainer,
} from '@material-ui/core';
import 'fontsource-roboto';
import { Link } from 'react-router-dom';

import { useStyles } from '../styles';

type Transaction = {
  balance: number;
  id: number;
  name: string;
};

type LeaderboardData = {
  transactions: Array<Transaction>;
};

function Leaderboard() {
  const [transactions, setTransactions] = useState<Array<Transaction>>([]);
  const [loading, setLoading] = useState(true);

  const classes = useStyles();

  useEffect(() => {
    fetch('/api/leaderboard')
      .then((res) => res.json())
      .then((data: LeaderboardData) => {
        setTransactions(data.transactions);
        setLoading(false);
      });
  }, []);

  return (
    <div className="Leaderboard">
      <Paper className="gradient-border-leaderboard" style={{ background: 'black', color: 'white', textAlign: 'center' }}>
        <br />
        <Typography variant="h3">
          Leaderboard
        </Typography>
        <br />
        <br />
        <img src="https://media3.giphy.com/media/3Gm15eZOsNk0tptIuG/giphy.gif" alt="coinflip" style={{ height: '200px', width: '200px', borderRadius: '25px' }} />
        <br />
        <br />
        <br />
        <TableContainer component={Paper} style={{ width: '70%', margin: 'auto' }}>
          <Table className={classes.table} aria-label="simple table">
            <TableHead style={{ backgroundColor: '#fff601' }}>
              <TableRow>
                <TableCell style={{ color: 'black', fontWeight: 'bold' }}>ID</TableCell>
                <TableCell style={{ color: 'black', fontWeight: 'bold' }}>Name</TableCell>
                <TableCell style={{ color: 'black', fontWeight: 'bold' }}>Balance</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? <CircularProgress color="secondary" /> : null}
              {transactions.map((transaction) => (
                <TableRow className={classes.tableRow} component={Link} to={`/profile/${transaction.id}`} hover>
                  <TableCell>{transaction.id}</TableCell>
                  <TableCell>{transaction.name}</TableCell>
                  <TableCell>{transaction.balance}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <br />
      </Paper>
    </div>
  );
}

export default Leaderboard;
