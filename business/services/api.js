import { useNuxtApp } from '#app';

const getApiInstance = () => {
  const nuxtApp = useNuxtApp();
  return nuxtApp.$api;
};

export default {
  get(url, options) {
    return getApiInstance()(url, { ...options, method: 'GET' });
  },
  post(url, data, options) {
    return getApiInstance()(url, { ...options, method: 'POST', body: data });
  },
  put(url, data, options) {
    return getApiInstance()(url, { ...options, method: 'PUT', body: data });
  },
  delete(url, options) {
    return getApiInstance()(url, { ...options, method: 'DELETE' });
  },
};