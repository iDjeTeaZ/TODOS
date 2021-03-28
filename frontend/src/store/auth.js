import axios from 'axios';
import BASE_URL from '@/config';
import {
	AUTH_REQUEST,
	AUTH_ERROR,
	AUTH_SUCCESS,
	AUTH_LOGOUT
} from "@/store/actions";

const state = {
	token: localStorage.getItem('jwt') || '',
	user: localStorage.getItem('user') || '',
	status: ''
};

const getters = {
	isAuthenticated: state => !!state.token,
	authStatus: state => state.status,
	user: state => state.user
};

const actions = {
	[AUTH_REQUEST]: ({commit}, user) => {
		return new Promise((resolve, reject) => {
			commit(AUTH_REQUEST);
			const path = `${BASE_URL}/login`;
			console.log(user)
			axios.post(path, user).then(res => {
				const token = res.data.data.token;
				const username = user.user;
				const payload = {
					token: token,
					user: username
				}
				localStorage.setItem('jwt', token);
				localStorage.setItem('user', username);
				commit(AUTH_SUCCESS, payload);
				resolve(res.data);
			}).catch(error => {
				commit(AUTH_ERROR);
				localStorage.removeItem('jwt');
				if (error.response && error.response.data) {
					reject(error.response.data);
				} else {
					const data = { status:-1, message:'Server down' };
					reject(data);
				}
			});
		});
	},
	[AUTH_LOGOUT]: ({commit}) => {
		return new Promise((resolve) => {
			commit(AUTH_LOGOUT);
			localStorage.removeItem('jwt');
			resolve();
		});
	}
};

const mutations = {
	[AUTH_REQUEST]: (state) => {
		state.status = 'loading';
	},
	[AUTH_SUCCESS]: (state, payload) => {
		state.status = 'success';
		state.token = payload.token;
		state.user = payload.user;
	},
	[AUTH_ERROR]: (state) => {
		state.status = 'error';
	},
	[AUTH_LOGOUT]: (state) => {
		state.status = '';
		state.token = '';
		state.user = '';
	}
};

export default {
	state,
	getters,
	actions,
	mutations
};
