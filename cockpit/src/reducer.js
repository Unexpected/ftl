/*import article from './reducers/article';
import articleList from './reducers/articleList';
import auth from './reducers/auth';*/
import { combineReducers } from 'redux';
import common from './reducers/common';
import home from './reducers/home';
/*import editor from './reducers/editor';
import profile from './reducers/profile';
import settings from './reducers/settings';*/
import { connectRouter } from 'connected-react-router'

const createRootReducer = (history) => combineReducers({
  router: connectRouter(history),
  common,
  home
  // rest of your reducers
})
export default createRootReducer