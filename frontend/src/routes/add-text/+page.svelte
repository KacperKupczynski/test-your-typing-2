<script lang="ts">
    let content = '';
    let message = '';

    async function addText() {
        const response = await fetch('http://localhost:8000/api/addText/', {
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
        <textarea name="text" bind:value={content} placeholder="Enter your text"></textarea>
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