<template>
	<div class='container'>
		<div class='row'>
			<div class='col-sm-12'>
				<h1>{{ name }}</h1>
				<hr><br><br>
				<button type='button' class='btn btn-success' v-b-modal.ajouter-todo-modal>Ajouter un TODO</button>
				<br><br>
				<alert :variant='alert.variant' :message='alert.message' v-if='alert.message'></alert>
				<table class='table table-hover'>
					<thead>
						<tr>
							<th scope='col'>Nom</th>
							<th scope='col'>Tâche</th>
							<th scope='col'>Date</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for='(todo, index) in todos' :key='index'>
							<td>{{ todo.name }}</td>
							<td>{{ todo.task }}</td>
							<td>{{ todo.date }}</td>
							<td>
								<div class='btn-group' role='group'>
									<button type='button' class='btn btn-info btn-sm' v-b-modal.modifier-todo-modal @click='lancerFormulaireModifier(todo)'>Modifier</button>
									<button type='button' class='btn btn-danger btn-sm' @click='surSuppression(todo.id_todo)'>Supprimer</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<b-modal ref='ajouterTodoModal' id='ajouter-todo-modal' title='Ajouter un TODO' hide-footer>
			<b-form @submit='surAjoutEnvoi' @reset='surAjoutReinitialise' class='w-100'>
				<b-form-group id='formulaire-nom-groupe' label='Nom:'>
					<b-form-input id='formulaire-nom' type='text' v-model='ajouterTodoFormulaire.name' required>
					</b-form-input>
				</b-form-group>
				<b-form-group id='formulaire-tache-groupe' label='Tâche:'>
					<b-form-input id='formulaire-tache' type='text' v-model='ajouterTodoFormulaire.task' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' class='btn btn-success btn-sm'>Envoyer</b-button>
				<b-button type='reset' class='btn btn-primary btn-sm'>Annuler</b-button>
			</b-form>
		</b-modal>

		<b-modal ref='modifierTodoModal' id='modifier-todo-modal' title='Modifier un TODO' hide-footer>
			<b-form @submit='surModificationEnvoi' @reset='surModificationReinitialise' class='w-100'>
				<b-form-group id='formulaire-nom-groupe' label='Nom:'>
					<b-form-input id='formulaire-nom' type='text' v-model='modifierTodoFormulaire.name' required>
					</b-form-input>
				</b-form-group>
				<b-form-group id='formulaire-tache-groupe' label='Tâche:'>
					<b-form-input id='formulaire-tache' type='text' v-model='modifierTodoFormulaire.task' required>
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
import Alert from '@/components/Alert.vue'
import BASE_URL from '@/config'

export default {
	data() {
		return {
			name: 'Loading...',
			todos: [],
			ajouterTodoFormulaire: {
				name:'',
				task:''
			},
			modifierTodoFormulaire: {
				id_todo: -1,
				name:'',
				task:''
			},
			id_list: this.$route.params.id_list,
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
		lancerFormulaireAjouter() {
			this.ajouterTodoFormulaire.name = '';
			this.ajouterTodoFormulaire.task = '';
		},
		lancerFormulaireModifier(todo) {
			this.modifierTodoFormulaire.id_todo = todo.id_todo;
			this.modifierTodoFormulaire.name = todo.name;
			this.modifierTodoFormulaire.task = todo.task;
		},
		recupererTodos() {
			const path = `${BASE_URL}/lists/${this.id_list}`;
			this.gestion(axios.get(path),
				res => {
					this.todos = res.data.todos;
					this.name = res.data.name;
				},
				this.surErreur
			);
		},
		surErreur(error) {
			this.alert.variant = 'danger';
			this.alert.message = error.message;
		},
		surSucces(message) {
			this.recupererTodos();
			this.alert.variant = 'success';
			this.alert.message = message;
		},
		surAjoutEnvoi(evt) {
			evt.preventDefault();
			this.$refs.ajouterTodoModal.hide();
			const path = `${BASE_URL}/lists/todos/${this.id_list}`;
			this.gestion(axios.put(path, this.ajouterTodoFormulaire),
				() => this.surSucces('TODO ajouté'),
				this.surErreur
			);
			this.lancerFormulaireAjouter();
		},
		surAjoutReinitialise(evt) {
			evt.preventDefault();
			this.$refs.ajouterTodoModal.hide();
			this.lancerFormulaireAjouter();
		},
		surModificationEnvoi(evt) {
			evt.preventDefault();
			this.$refs.modifierTodoModal.hide();
			const path = `${BASE_URL}/lists/todos/${this.id_list}/${this.modifierTodoFormulaire.id_todo}`;
			const payload = {
				name: this.modifierTodoFormulaire.name,
				task: this.modifierTodoFormulaire.task,
			};
			this.gestion(axios.patch(path, payload),
				() => this.surSucces('TODO modifié'),
				this.surErreur
			);
		},
		surModificationReinitialise(evt) {
			evt.preventDefault();
			this.$refs.modifierTodoModal.hide();
			this.lancerFormulaireModifier();
		},
		surSuppression(id_todo) {
			const path = `${BASE_URL}/lists/todos/${this.id_list}/${id_todo}`;
			this.gestion(axios.delete(path),
				() => this.surSucces('TODO supprimé'),
				this.surErreur
			);
		}
	},
	components: {
		alert: Alert
	},
	beforeMount() {
		this.recupererTodos();
	}
};

</script>
