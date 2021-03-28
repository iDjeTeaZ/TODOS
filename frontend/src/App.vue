<template>
	<div id="app">
		<navbar></navbar>
		<router-view/>
	</div>
</template>

<style>
	h1 {
		margin-top: 60px !important;
	}
</style>

<script>
import Menu from '@/components/Menu.vue';

export default {
	components: {
		navbar: Menu
	}
}
</script>
