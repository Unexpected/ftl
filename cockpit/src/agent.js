import superagentPromise from 'superagent-promise';
import _superagent from 'superagent';

const superagent = superagentPromise(_superagent, global.Promise);

const API_ROOT = 'http://localhost:5000/api/core';

// const encode = encodeURIComponent;
const responseBody = res => res.body;

const requests = {
  del: url =>
    superagent.del(`${API_ROOT}${url}`).then(responseBody),
  get: url =>
    superagent.get(`${API_ROOT}${url}`).then(responseBody),
  put: (url, body) =>
    superagent.put(`${API_ROOT}${url}`, body).then(responseBody),
  post: (url, body) =>
    superagent.post(`${API_ROOT}${url}`, body).then(responseBody)
};

const App = {
  modules: () => requests.get('/modules')
};

const Entities = {
  getAll: () => requests.get('/entities')
};

// const limit = (count, p) => `limit=${count}&offset=${p ? p * count : 0}`;

const Attributes = {
  all: entityName =>
    requests.get(`/attributes/${entityName}`),
  /*  byAuthor: (author, page) =>
      requests.get(`/articles?author=${encode(author)}&${limit(5, page)}`),
    byTag: (tag, page) =>
      requests.get(`/articles?tag=${encode(tag)}&${limit(10, page)}`),
    del: slug =>
      requests.del(`/articles/${slug}`),
    favorite: slug =>
      requests.post(`/articles/${slug}/favorite`),
    favoritedBy: (author, page) =>
      requests.get(`/articles?favorited=${encode(author)}&${limit(5, page)}`),
    feed: () =>
      requests.get('/articles/feed?limit=10&offset=0'),
    get: slug =>
      requests.get(`/articles/${slug}`),
    unfavorite: slug =>
      requests.del(`/articles/${slug}/favorite`),
    update: article =>
      requests.put(`/articles/${article.slug}`, { article: omitSlug(article) }),
    create: article =>
      requests.post('/articles', { article })*/
};

const Person = {
  create: person =>
    requests.post('/person', { person })
}

/* const Comments = {
  create: (slug, comment) =>
    requests.post(`/articles/${slug}/comments`, { comment }),
  delete: (slug, commentId) =>
    requests.del(`/articles/${slug}/comments/${commentId}`),
  forArticle: slug =>
    requests.get(`/articles/${slug}/comments`)
};

const Profile = {
  follow: username =>
    requests.post(`/profiles/${username}/follow`),
  get: username =>
    requests.get(`/profiles/${username}`),
  unfollow: username =>
    requests.del(`/profiles/${username}/follow`)
}; */

export default {
  App,
  Entities,
  Attributes,
  Person
};
