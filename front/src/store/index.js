import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
  },

  mutations: {
    setToken(state, token) {
      state.token = token
    }
  },

  actions: {
    setToken(context, value) {
      context.commit('setToken', value);
    },
  },

  modules: {
  },

  plugins: [createPersistedState({
    storage: {
      getItem: key => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 3, secure: false }),
      removeItem: key => Cookies.remove(key)
    }
  })],
})
