<script lang="ts">
    import { onMount } from "svelte";
    import { API_URL } from '$lib/index';

    let textList: { content: string }[] = [];
    onMount(getTextList);

    let message = '';

    // Function to fetch text list from the API
    // This function is called on mounting site (component)
    async function getTextList() {
        const response = await fetch(`${API_URL}/api/textList/`, {
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
        const response = await fetch(`${API_URL}/api/deleteText/`, {
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
    <div class="texts">
        <!-- {#if textList.length > 0}
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
        {/if} -->
        <table>
            <thead>
                <tr>
                    <th>Text</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each textList as text}
                    <tr>
                        <td>{text.content}</td>
                        <td><button on:click={() => deleteText(text.content)}>Delete</button></td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
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

    .texts {
        max-height: calc(100vh - 10rem);
        overflow: auto;
        padding: 3rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }

    th, td {
        border: 1px solid #f1f1f1;
        padding: 8px;
    }

    th {
        background-color: rgba(255, 255, 255, 0.1);
        font-weight: bold;
    }

    td {
        word-wrap: break-word;
        max-width: 800px;
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