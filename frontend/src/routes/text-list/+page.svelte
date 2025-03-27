<script lang="ts">
    import { onMount } from "svelte";

    let textList: { content: string }[] = [];
    onMount(getTextList);

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
            alert('Failed to get text list');
        }
    }

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
            alert('Text deleted successfully');
            getTextList();
        } else {
            alert('Failed to delete text');
        }
    }
</script>

<h1>Text list</h1>


{#if textList.length > 0}
    <ul>
        {#each textList as text}
            <li>{text.content}</li>
            <button on:click={() => deleteText(text.content)}>Delete</button>
        {/each}
    </ul>
{:else}
    <p>No texts found</p>
{/if}