import Vue from 'vue';
import Router from 'vue-router';
import Input from '../components/Input.vue';
import Sentiment from '../components/Sentiment.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Input',
      component: Input,
      props: true,
    },
    {
      path: '/result',
      name: 'Sentiment',
      component: Sentiment,
      props: true,
    },
  ],
});
