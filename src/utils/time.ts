/* eslint-disable import/prefer-default-export */

const MINUTE_TO_SECONDS = 60;
const HOUR_TO_SECONDS = MINUTE_TO_SECONDS * 60;
const DAY_TO_SECONDS = HOUR_TO_SECONDS * 24;
const WEEK_TO_SECONDS = DAY_TO_SECONDS * 7;

export function humanizeSeconds(datetime: Date) {
  const currentTime = new Date();
  const timeDelta = Math.round((currentTime.getTime() - datetime.getTime()) / 1000);

  if (timeDelta < MINUTE_TO_SECONDS) {
    return 'Just now';
  }
  if (timeDelta < HOUR_TO_SECONDS) {
    const minutes = Math.floor(timeDelta / MINUTE_TO_SECONDS);
    return `${minutes} minutes ago`;
  }
  if (timeDelta < DAY_TO_SECONDS) {
    const hours = Math.floor(timeDelta / HOUR_TO_SECONDS);
    return `${hours} hours ago`;
  }
  if (timeDelta < WEEK_TO_SECONDS) {
    const days = Math.floor(timeDelta / DAY_TO_SECONDS);
    return `${days} days ago`;
  }

  return datetime.toDateString();
}
