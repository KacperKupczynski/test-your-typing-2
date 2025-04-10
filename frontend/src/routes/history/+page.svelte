<script lang="ts">
	import { onMount } from "svelte";

    let results: { text: string; wpm: number; time: number, created_at: Date }[] = [];

    onMount(getResults);

    async function getResults() {
        const response = await fetch('http://localhost:8000/api/getResults/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            results = data.results.map((result: { text: string; wpm: number; time: number, created_at: Date }) => ({
                text: result.text,
                wpm: result.wpm,
                time: result.time,
                created_at: new Date(result.created_at).toLocaleString()

            }));
        } else {
            alert('Failed to get results');
        }
    }
</script>
<div class="history">
    <div class="introduction">
        <h1>
            Results history
        </h1>
        <p>
            Once you take the test, you will see your results here.
        </p>
    </div>
    
    <div class="list">
        {#if results.length > 0}
        <ul>
            {#each results as result}
                <li>
                    <p class="bold">{result.text}</p>
                    <p>WPM: {result.wpm}</p>
                    <p>Time: {result.time} seconds</p>
                    <p>Taken: {result.created_at}</p>
                </li>
            {/each}
        </ul>
        {:else}
        <p>No results found</p>
        {/if}
    </div>
</div>

<style>
.history {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
}
.introduction {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.list {
    width: 100%;
    max-height: 600px;
    overflow: scroll;
    border: 3px solid #f1f1f1;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
}
</style>