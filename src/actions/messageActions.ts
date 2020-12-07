export const ADD_MESSAGE = 'ADD_MESSAGE';
export const CLEAR_ALL = 'CLEAR_ALL';
export const DELETE_MESSAGE = 'DELETE_MESSAGE';

export interface IAddMessageAction {
  readonly type: typeof ADD_MESSAGE;
  payload: {
    message: string;
    type: 'error' | 'warning' | 'info' | 'success';
  };
}

export interface IClearAllMessageAction {
  readonly type: typeof CLEAR_ALL;
}

export interface IDeleteErrorAction {
  readonly type: typeof DELETE_MESSAGE;
  payload: {
    id: number;
  };
}

export type MessageActions = IAddMessageAction | IClearAllMessageAction | IDeleteErrorAction;
