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
</script>

<h1>Text list</h1>


{#if textList.length > 0}
    <ul>
        {#each textList as text}
            <li>{text.content}</li>
        {/each}
    </ul>
{:else}
    <p>No texts found</p>
{/if}