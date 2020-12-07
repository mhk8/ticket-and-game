import React, { useState } from 'react';

type Color = {
  item_type: number,
  name: string,
};

interface Props {
  colors: Array<Color>,
}

function Colors(props: Props) {
  const { colors } = props;
  const [curColor, setCurColor] = useState('');

  function HandleColorChange(event) {
    setCurColor(event.target.value);
  }

  function SubmitColor() {
    fetch('/api/settings/textcolor', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        item_type: curColor,
      }),
    });
  }

  return (
    <div>
      { colors.length !== 0
        ? (
          <div>
            <select onChange={HandleColorChange}>
              {colors.map((color) => (
                <option key={color.item_type} value={color.item_type}>{color.name}</option>
              ))}
            </select>
            <button type="button" value="Confirm" onClick={SubmitColor}>Confirm</button>
          </div>
        )
        : (
          <div />
        )}
    </div>
  );
}

export default Colors;
