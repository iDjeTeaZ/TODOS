import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Todos from '../views/Todos.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import store from '@/store'

Vue.use(VueRouter);
function loginIfNot(to, from, next) {
	if (!store.getters.isAuthenticated) {
		next('/login');
	} else {
		next();
	}
}

const routes = [
{
	path: '/',
	name: 'home',
	component: Home,
	beforeEnter: loginIfNot
},
{
	path: '/list/:id_list',
	name: 'todos',
	component: Todos,
	beforeEnter: loginIfNot
},
{
	path: '/login',
	name: 'login',
	component: Login
},
{
	path: '/signup',
	name: 'signup',
	component: Signup
},
{
	path: '*',
	beforeEnter: (from, to, next) => next('/login')
}];

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
});

export default router;
