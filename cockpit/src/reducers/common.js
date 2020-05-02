
import {
  APP_INITIALIZE,
  MODULE_INITIALIZE,
  MODULE_UNLOAD,
  VIEW_INITIALIZE
} from '../constants/actionTypes';

const defaultState = {
  appInitialized: false,

  appLoaded: false,
  viewLoaded: false,
  viewChangeCounter: 0,

  view: {}
};

export default (state = defaultState, action) => {
  var view = { ...state.view }
  switch (action.type) {
    case APP_INITIALIZE:
      return {
        ...state,
        modules: action.payload[0],
        appInitialized: true
      };
    case MODULE_INITIALIZE:
      view.name = "default";
      return {
        ...state,
        currentModule: action.moduleName,
        module: action.metadata[0],
        view: view
      };
    case MODULE_UNLOAD:
      return {
        ...state,
        currentModule: null,
        module: null
      };
    case VIEW_INITIALIZE:
      view.name = action.viewName;
      view.entityName = action.entityName;
      view.queryName = action.queryName;
      view.keys = action.keys;
      return {
        ...state,
        view: view,
        viewInitialized: true
      };
    case 'LOCATION_CHANGE':
      return {
        ...state,
        viewLoaded: false
      };
    case 'LIST_LOAD':
      return {
        ...state,
        viewLoaded: true,
        viewData: action.payload
      };
    case 'APP_LOAD':
      return {
        ...state,
        entities: action.payload[0],
        appLoaded: true
      }
    default:
      return state;
  }
  /*
  switch (action.type) {
    case APP_LOAD:
      return {
        ...state,
        token: action.token || null,
        appLoaded: true,
        currentUser: action.payload ? action.payload.user : null
      };
    case REDIRECT:
      return { ...state, redirectTo: null };
    case LOGOUT:
      return { ...state, redirectTo: '/', token: null, currentUser: null };
    case ARTICLE_SUBMITTED:
      const redirectUrl = `/article/${action.payload.article.slug}`;
      return { ...state, redirectTo: redirectUrl };
    case SETTINGS_SAVED:
      return {
        ...state,
        redirectTo: action.error ? null : '/',
        currentUser: action.error ? null : action.payload.user
      };
    case LOGIN:
    case REGISTER:
      return {
        ...state,
        redirectTo: action.error ? null : '/',
        token: action.error ? null : action.payload.user.token,
        currentUser: action.error ? null : action.payload.user
      };
    case DELETE_ARTICLE:
      return { ...state, redirectTo: '/' };
    case ARTICLE_PAGE_UNLOADED:
    case EDITOR_PAGE_UNLOADED:
    case HOME_PAGE_UNLOADED:
    case PROFILE_PAGE_UNLOADED:
    case PROFILE_FAVORITES_PAGE_UNLOADED:
    case SETTINGS_PAGE_UNLOADED:
    case LOGIN_PAGE_UNLOADED:
    case REGISTER_PAGE_UNLOADED:
      return { ...state, viewChangeCounter: state.viewChangeCounter + 1 };*/

};
