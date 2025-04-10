<script lang="ts">
	import { onMount } from "svelte";

    let results: { text: string; wpm: number; time: number, created_at: Date }[] = [];

    // Fetch results when the component mounts
    onMount(getResults);

    let message = '';

    // Function to fetch results from the API
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
            message = 'Failed to get results';
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
    
    <!-- box for results and statistics -->
    <div class="listbox">
        {#if results.length > 0}
        <div class="headers">
            <h2>Results</h2>
            <h2>Statistics</h2>
        </div>
        <!-- box for table and statistics, things below headers-->
        <div class="table-and-stats">
            <!-- container for records of results -->
            <div class="list">
                <table>
                    <thead>
                        <tr>
                            <th>Text</th>
                            <th>WPM</th>
                            <th>Time</th>
                            <th>Taken</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each results as result}
                            <tr>
                                <td class="roboto-mono">{result.text}</td>
                                <td>{result.wpm}</td>
                                <td>{result.time.toFixed(2)} seconds</td>
                                <td>{result.created_at}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
            <!-- container for statistics -->
                <div class="stats">
                <p>Total results: {results.length}</p>
                <p>Average WPM: {Math.round(results.reduce((acc, result) => acc + result.wpm, 0) / results.length)}</p>
                <p>Average time: {Math.round(results.reduce((acc, result) => acc + result.time, 0) / results.length)} seconds</p>
                <p>Best WPM: {results.reduce((acc, result) => Math.max(acc, result.wpm), 0)}</p>
                <p>Best time: {results.reduce((acc, result) => Math.min(acc, result.time), Infinity).toFixed(2)} seconds</p>
                <p>Worst WPM: {results.reduce((acc, result) => Math.min(acc, result.wpm), Infinity)}</p>
                <p>Worst time: {results.reduce((acc, result) => Math.max(acc, result.time), 0).toFixed(2)} seconds</p>
                <p>Words typed: {results.reduce((acc, result) => acc + result.text.split(' ').length, 0)} </p>
                <p>Characters typed: {results.reduce((acc, result) => acc + result.text.length, 0)} </p>

            </div>
        </div>
        {:else}
        <p>No results found</p>
        {/if}
    </div>
    {#if message}
        <p class="error">{message}</p>
    {/if}
</div>

<style>
.history {
    width: 100%;
    padding: 3rem;
}

.introduction {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.listbox {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 600px;
    border: 3px solid #f1f1f1;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    overflow: hidden;
}

.headers {
    height: 64px;
    display: flex;
    border-bottom: 2px solid white;
    justify-content: space-around;
    align-items: center;
    text-align: center;
}

.table-and-stats {
    display: flex;
    align-items: center;
    width: 100%;
    height: calc(100% - 66px);
    flex-wrap: wrap; /* Allow wrapping for smaller screens */
}

.stats {
    width: 50%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    box-sizing: border-box;
}

.list {
    width: 50%;
    height: 100%;
    overflow-y: auto;
    box-sizing: border-box;
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
    max-width: 400px;
}

/* Responsive Styles */
@media (max-width: 1024px) {
    .table-and-stats {
        flex-direction: column; /* Stack table and stats vertically */
    }

    .stats, .list {
        width: 100%; /* Full width for both sections */
        height: auto; /* Adjust height dynamically */
    }

    .list {
        max-height: 300px; /* Limit height for scrolling */
    }
}

@media (max-width: 768px) {
    .listbox {
        height: auto; /* Adjust height dynamically for smaller screens */
    }

    .headers {
        font-size: 14px; /* Smaller font size for headers */
    }

    th, td {
        font-size: 12px; /* Smaller font size for table content */
        padding: 6px; /* Reduce padding */
    }

    .stats p {
        font-size: 14px; /* Smaller font size for stats */
    }
}

@media (max-width: 480px) {
    .history {
        padding: 1rem; /* Reduce padding for smaller screens */
    }

    .headers {
        flex-direction: column; /* Stack headers vertically */
        height: auto;
    }

    .stats p {
        font-size: 12px; /* Further reduce font size for stats */
    }

    th, td {
        font-size: 10px; /* Further reduce font size for table content */
        padding: 4px; /* Reduce padding further */
    }
}</style>