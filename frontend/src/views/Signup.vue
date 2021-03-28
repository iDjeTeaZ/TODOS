<template>
  <div class='container'>
	<b-modal ref='inscriptionModal' id='inscription-modal' title='Inscription' no-close-on-esc no-close-on-backdrop hide-header-close hide-footer>
		<b-form @submit='surEnvoi' class='w-100'>
			<alert :variant='"danger"' :message='message' v-if='message'></alert>
			<b-form-group id='formulaire-identifiant-groupe' label='Identifiant:'>
				<b-form-input id='formulaire-identifiant' type='text' v-model='userForm.user' required>
				</b-form-input>
			</b-form-group>
			<b-form-group id='formulaire-mot-de-passe-groupe' label='Mot de passe:'>
				<b-form-input id='formulaire-mot-de-passe' type='password' v-model='userForm.pwd' required>
				</b-form-input>
			</b-form-group>
			<b-button type='submit' class='btn btn-success btn-sm'>Envoyer</b-button>
			<router-link to='/login' class='btn btn-primary btn-sm'>Connexion</router-link>
		</b-form>
	</b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from '@/components/Alert.vue';
import { AUTH_REQUEST } from '@/store/actions';
import BASE_URL from '@/config';

export default {
	data() {
		return {
			userForm: {
				user: '',
				pwd: ''
			},
			message: ''
		}
	},
	methods: {
		gestion(request, surSucces, surErreur) {
			request.then(res => {
				if (res.data.status == 0) {
					surSucces(res.data);
					return;
				}
				surErreur(res.data);
			}).catch(error => {
				surErreur(error.response.data);
			});
		},
		login() {
			this.$store.dispatch(AUTH_REQUEST, this.userForm).then(() => {
				this.$router.push('/');
			}).catch(error => {
				this.message = error.message;
			});
		},
		surEnvoi(evt) {
			evt.preventDefault();
			const path = `${BASE_URL}/account`;
			this.gestion(axios.post(path, this.userForm),
				this.login,
				error => { this.message = error.message; }
			);
		}
	},
	mounted() {
		this.$refs.inscriptionModal.show();
	},
	components: {
		alert: Alert
	}
}

</script>
