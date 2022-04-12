import Vue from 'vue'

import axios from 'axios'


Vue.prototype.$http = axios

axios.defaults.baseURL = 'http://127.0.0.1:8000/'

axios.interceptors.request.use(
  function (request) {
    return request
  },

  function (error) {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  function (response) {
    return response;
  },

  function (error) {
       Promise.reject(error)
  }
);