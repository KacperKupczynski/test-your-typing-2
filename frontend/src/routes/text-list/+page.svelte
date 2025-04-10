<script lang="ts">
    import { onMount } from "svelte";

    let textList: { content: string }[] = [];
    onMount(getTextList);

    let message = '';

    // Function to fetch text list from the API
    // This function is called on mounting site (component)
    async function getTextList() {
        const response = await fetch('http://localhost:8000/api/textList/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            textList = data.texts.map((content: string) => ({ content }));
        } else {
            message = 'Failed to get text list';
        }
    }

    // Function to delete text from the database
    // This function is called when the delete button is clicked
    // It sends a DELETE request to the API with the text content to be deleted
    async function deleteText(content: string) {
        const response = await fetch('http://localhost:8000/api/deleteText/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ content })
        });
    
        if (response.ok) {
            getTextList();
        } else {
            message = 'Failed to delete text';
        }
    }
</script>

<div class="main">
    <h1>Text list</h1>
    
    {#if textList.length > 0}
    {#each textList as text}
        <ul>
                <li class="roboto-mono">{text.content}</li>
                <button on:click={() => deleteText(text.content)}>Delete</button>
            </ul>
        {/each}
    {:else}
        <p>No texts found</p>
    {/if}
    {#if message}
        <p class="error">{message}</p>
    {/if}
</div>



<style>
    .main {
        width: 100%;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 8px;
    }

    h1 {
        text-align: center;
    }

    ul {
        list-style-type: none;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap:16px;
    }

    li {
        margin: 10px 0;
        font-family: 'Roboto Mono', monospace;
        font-size: 16px;
        max-width: 50vw;
        padding: 10px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid white;
    }

    button {
        background-color: #ff4d4d;
        color: white;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
    }

    button:hover {
        background-color: #af0000;
    }
</style>