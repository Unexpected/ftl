import { combineReducers } from 'redux';
import common from './reducers/common';
import home from './reducers/home';

const createRootReducer = (history) => combineReducers({
  common,
  home
  // rest of your reducers
})
export default createRootReducer