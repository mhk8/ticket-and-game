import React from 'react';

interface Props {
  hand: Array<number|String>,
}

function BlackjackCard(props: Props) {
  const { hand } = props;
  const displayHand : JSX.Element[] = [];
  for (let i = 0; i < hand.length; i += 2) {
    if (hand[i] === 'A' && hand[i + 1] === 'D') {
      displayHand.push(
        <img className="blackjack-card" src="AceofDiamonds.png" alt="playing Card" />,
      );
    } else {
      const link = ['https://deckofcardsapi.com/static/img/', hand[i], hand[i + 1], '.png'].join('');
      displayHand.push(
        <img className="blackjack-card" src={link} alt="Playing Card" />,
      );
    }
  }
  return <div>{displayHand}</div>;
}

export default BlackjackCard;
