import {
  ADD_MESSAGE, CLEAR_ALL, DELETE_MESSAGE, MessageActions,
} from '../actions/messageActions';

type MessageState = {
  id: number;
  message: string;
  type: 'error' | 'warning' | 'info' | 'success';
};

const initialMessageState: Array<MessageState> = [];

function messagesReducer(
  state: typeof initialMessageState = initialMessageState,
  action: MessageActions,
) {
  switch (action.type) {
    case ADD_MESSAGE:
      return [
        ...state,
        {
          id: state.length,
          message: action.payload.message,
          type: action.payload.type,
        },
      ];
    case CLEAR_ALL:
      return initialMessageState;
    case DELETE_MESSAGE:
      return state.filter((error) => error.id !== action.payload.id);
    default:
      return state;
  }
}

export default messagesReducer;
