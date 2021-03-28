<template>
	<div>
		<b-alert :variant=variant show>{{ message }}</b-alert>
		<br>
	</div>
</template>

<script>
	export default {
		props: ['message', 'variant']
	};
</script>
