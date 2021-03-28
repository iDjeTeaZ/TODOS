<template>
  <div class='container'>
	<b-modal ref='connexionModal' id='connexion-modal' title='Connexion' no-close-on-esc no-close-on-backdrop hide-header-close hide-footer>
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
			<router-link to='/signup' class='btn btn-primary btn-sm'>S'inscrire</router-link>
		</b-form>
	</b-modal>
  </div>
</template>

<script>
import { AUTH_REQUEST } from '@/store/actions';
import Alert from '@/components/Alert.vue';

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
		surEnvoi(evt) {
			evt.preventDefault();
			this.$store.dispatch(AUTH_REQUEST, this.userForm).then(() => {
				this.$router.push('/');
			}).catch(error => {
				this.message = error.message;
			});
		}
	},
	mounted() {
		this.$refs.connexionModal.show();
	},
	components: {
		alert: Alert
	}
}

</script>
