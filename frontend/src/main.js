import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import store from './store';

Vue.use(BootstrapVue)
Vue.config.productionTip = false;

axios.interceptors.request.use(request => {
	const token = localStorage.getItem('jwt');
	if (token) {
		request.headers['jwt'] = token;
	}
	return request;
}, err => {
	return Promise.reject(err);
});

new Vue({
	router,
	store,
	render: h => h(App)
}).$mount('#app');
