<script lang="ts">
    let content = '';
    let message = '';
    import { API_URL } from '$lib/index';
	import { onMount } from 'svelte';

    onMount(() => {
        // Check if the user is logged in
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            window.location.href = '/login';
        }
    });

    // Function to add text to the database
    // This function is called when the form is submitted
    async function addText() {
        if (!content.trim()) {
            message = "Text cannot be empty";
            return;
        }
        const response = await fetch(`${API_URL}/api/addText/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ content })
        });

        if (response.ok) {
            message = "Text added"
            content = "";
        } else {
            message = "Failed when adding text";
        }
    }
</script>

<div class="page-box">
    <h1>Add your text</h1>

    <form on:submit|preventDefault={addText}>
        <label for="text">Enter a text:</label>
        <textarea name="text" bind:value={content} placeholder="Enter your text" required></textarea>
        <button type="submit">Add text</button>
    </form>
    {#if message}
        <p>{message}</p>
    {/if}
</div>


<style>
.page-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

</style>