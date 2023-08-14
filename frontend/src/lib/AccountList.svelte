<script>
	import { onMount } from 'svelte';
	import { defaultClient } from '$lib/ApiClient.js';

	let url = '';
	onMount(() => {
		url = window.location.href;
	});
</script>

<div class="list-group">
	{#await defaultClient.listAccounts()}
		Loading...
	{:then accounts}
		{#each accounts as account}
			<li class="list-group-item d-flex align-items-center">
				<img class="avatar me-3" src={account.openid.picture} alt={account.openid.email} />{account
					.openid.display_name} &lt;{account.openid.email}&gt;
				<a
					href="#0"
					class="btn btn-danger ms-auto"
					on:click={() => defaultClient.deleteAccount(account.openid.email)}
					title="Remove account"><i class="fa-solid fa-trash" /></a
				>
			</li>
		{/each}
	{:catch error}
		<li class="list-group-item">
			<div class="alert alert-danger" role="alert">
				{error.message}
			</div>
		</li>
	{/await}
	<li class="list-group-item list-group-item-action">
		<a href="{defaultClient.baseUrl}/auth/login?state={url}"
			><li class="fa-solid fa-plus" />
			Add account...</a
		>
	</li>
</div>

<style>
	img.avatar {
		max-width: 64px;
		border-radius: 50%;
	}
</style>
