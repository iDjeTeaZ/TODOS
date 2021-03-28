<template>
	<div class='container'>
		<div class='row'>
			<div class='col-sm-12'>
				<h1>Listes TODO</h1>
				<hr><br><br>
				<button type='button' class='btn btn-success' v-b-modal.ajouter-liste-modal>Ajouter une liste</button>
				<br><br>
				<alert :variant='alert.variant' :message='alert.message' v-if='alert.message'></alert>
				<table class='table table-hover'>
					<thead>
						<tr>
							<th scope='col'>Nom</th>
							<th scope='col'>Todos</th>
							<th scope='col'>Date</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for='(list, index) in lists' :key='index' @click='allerAListe(list, $event)'>
							<td>{{ list.name }}</td>
							<td>{{ list.todos.length }}</td>
							<td>---</td>
							<td>
								<div class='btn-group' role='group'>
									<button type='button' class='btn btn-info btn-sm' v-b-modal.modifier-liste-modal @click='lancerFormulaireModifier(list)'>Modifier</button>
									<button type='button' class='btn btn-danger btn-sm' @click='surSuppression(list.id_list)'>Supprimer</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<b-modal ref='ajouterListeModal' id='ajouter-liste-modal' title='Ajouter une liste TODO' hide-footer>
			<b-form @submit='surAjoutEnvoi' @reset='surAjoutReinitialise' class='w-100'>
				<b-form-group id='formulaire-ajouter-liste-group' label='Nom:'>
					<b-form-input id='formulaire-nom' type='text' v-model='ajouterListeFormulaire.name' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' class='btn btn-success btn-sm'>Envoyer</b-button>
				<b-button type='reset' class='btn btn-primary btn-sm'>Annuler</b-button>
			</b-form>
		</b-modal>

		<b-modal ref='modifierListeModal' id='modifier-liste-modal' title='Modifier une liste TODO' hide-footer>
			<b-form @submit='surModificationEnvoi' @reset='surModificationReinitialise' class='w-100'>
				<b-form-group id='formulaire-modifier-liste-group' label='Nom:'>
					<b-form-input id='formulaire-nom' type='text' v-model='modifierListeFormulaire.name' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' class='btn btn-success btn-sm'>Envoyer</b-button>
				<b-button type='reset' class='btn btn-primary btn-sm'>Annuler</b-button>
			</b-form>
		</b-modal>
	</div>
</template>

<script>
import axios from 'axios';
import Alert from '@/components/Alert.vue';
import BASE_URL from '@/config';

export default {
	data() {
		return {
			lists: [],
			ajouterListeFormulaire: {
				name:''
			},
			modifierListeFormulaire: {
				id_list: -1,
				name:''
			},
			alert: {
				message: '',
				variant: 'danger'
			}
		};
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
		recupererListes() {
			const path = `${BASE_URL}/lists`;
			this.gestion(axios.get(path),
				res => {
					this.lists = res.data;
				},
				this.surErreur
			);
		},
		lancerFormulaireAjouter() {
			this.ajouterListeFormulaire.name = '';
		},
		lancerFormulaireModifier(list) {
			this.modifierListeFormulaire.id_list = list.id_list;
			this.modifierListeFormulaire.name = list.name;
		},
		surErreur(error) {
			this.alert.variant = 'danger';
			this.alert.message = error.message;
		},
		surSucces(message) {
			this.recupererListes();
			this.alert.variant = 'success';
			this.alert.message = message;
		},
		surAjoutEnvoi(evt) {
			evt.preventDefault();
			this.$refs.ajouterListeModal.hide();
			const path = `${BASE_URL}/lists`;
			this.gestion(axios.put(path, this.ajouterListeFormulaire),
				() => this.surSucces('Liste TODO ajoutée'),
				this.surErreur
			);
			this.lancerFormulaireAjouter();
		},
		surAjoutReinitialise(evt) {
			evt.preventDefault();
			this.$refs.ajouterListeModal.hide();
			this.lancerFormulaireAjouter();
		},
		surModificationEnvoi(evt) {
			evt.preventDefault();
			this.$refs.modifierListeModal.hide();
			const path = `${BASE_URL}/lists/${this.modifierListeFormulaire.id_list}`;
			const payload = {
				name: this.modifierListeFormulaire.name
			};
			this.gestion(axios.patch(path, payload),
				() => this.surSucces('Liste TODO modifiée'),
				this.surErreur
			);
		},
		surModificationReinitialise(evt) {
			evt.preventDefault();
			this.$refs.modifierListeModal.hide();
		},
		surSuppression(id_list) {
			const path = `${BASE_URL}/lists/${id_list}`;
			this.gestion(axios.delete(path),
				() => this.surSucces('Liste TODO supprimée'),
				this.surErreur
			);
		},
		allerAListe(list, event) {
			if (event.target.tagName == 'TD') {
				this.$router.push(`list/${list.id_list}`);
			}
		}
	},
	components: {
		alert: Alert
	},
	beforeMount() {
		this.recupererListes();
	}
};

</script>
