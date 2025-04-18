<script lang="ts">
    import { onMount } from "svelte";
	import { user } from "../../stores/user";
    import { fade } from "svelte/transition";
    import { API_URL } from '$lib/index';


    let text = "";
    let letterStates: { letter: string; state: string }[] = [];
    let input = '';
    let time = 0;
    let interval = 0;
    let isStarted = false;
    let wpm = 0;
    let message = "";
    let finalWpm = 0;
    let finalTime = 0;
    let showResults = false;
    let isText = true;

    onMount(async () => {
        fetchText();
    });


    // Enter key event listener for play again button
    // This will allow the user to press enter to play again after the test is finished
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && showResults) {
            playAgain();
        }
    });

    // Function to fetch random text from the API
    // This function is called on mounting site (component)
    async function fetchText() {
        const response = await fetch(`${API_URL}/api/randomText`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            text = data.content;
            letterStates = text.split('').map(letter => ({
                letter,
                state: 'not-typed'
            }));
        } else {
            message = "Failed to fetch text.";
            isText = false;
        }
    }

    //start test when user starts typing
    $: if (input.length == 1 && !isStarted) {
        start();
    }

    //ends test when user types all letters
    $: if (input.length === text.length && isStarted) {
        stop();
    }

    // Function to check the input against the text
    function checkInput() {
        letterStates = letterStates.map((letterState, i) => {
            if (input[i] === letterState.letter) {
                return { ...letterState, state: 'correct' };
            } else if (input[i] === undefined) {
                return { ...letterState, state: 'not-typed' };
            } else {
                return { ...letterState, state: 'incorrect' };
            }
        });
    }

    // Function to start the timer and calculate WPM
    function start() {
        isStarted = true;
        interval = setInterval(() => {
            time += 0.01;
            calcWPM();
        }, 10);
    }

    // Function to calculate WPM based on the input and time
    // WPM is calculated as (number of characters / 5) / (time in minutes)
    function calcWPM() {
        const chars = input.length;
        const words = chars / 5;
        wpm = words / (time / 60);
    }

    // Function to check if the test is correct
    function checkCorrectness() {
        return letterStates.every(letterState => letterState.state === 'correct');
    }

    // Function to reset the test
    // This function is called when the user clicks the play again button
    function reset() {
        fetchText();
        input = '';
        letterStates = text.split('').map(letter => ({
            letter,
            state: 'not-typed'
        }));
        time = 0;
        wpm = 0;
        isStarted = false;
        clearInterval(interval);
        interval = 0;
    }

    // Function to stop the test and save the result
    async function stop() {
    clearInterval(interval);
    isStarted = false;

    if (checkCorrectness()) {
        const response = await fetch(`${API_URL}/api/saveResult/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`, // Retrieve token dynamically
            },
            body: JSON.stringify({
                text,
                wpm,
                time,
            }),
        });

        if (response.ok) {
            showResults = true;
        } else {
            message = "Failed to save result.";
        }
    } else {
        reset();
        message = "Test failed. Please try again.";
    }
}
    function playAgain() {
        showResults = false;
        reset();
    }
</script>

<div class="test">
{#if !showResults && isText}
    <div class="displayer roboto-mono">
        {#each letterStates as { letter, state }, i}
            {#if letter === ' '}
                <span class="space"></span>
            {:else}
                <span class={state}>{letter}</span>
            {/if}
        {/each}
    </div>
    <div class="type-box">
        <input type="text" name="" id="" bind:value={input} oninput={checkInput} placeholder="Type text above" autofocus/>
        {#if message}
            <p class="incorrect error">{message}</p>
        {/if}
        <p>WPM: {wpm.toFixed(2)}</p>
        <p>Time: {time.toFixed(2)}</p>
    </div>
{/if} 
{#if !isText}
    <p>There's nothing to type. Add a text here:</p>
    <a href="/add-text">Add text</a>
{/if}

    {#if showResults}
        <div class="results" transition:fade={{ duration: 300 }}>
            <h2>Results</h2>
            <p>WPM: {wpm.toFixed(2)}</p>
            <p>Time: {time.toFixed(2)} seconds</p>
            <button onclick={playAgain}>Play again</button>
        </div>
    {/if}

    {#if !showResults && input.length > 0}
        <button onclick={stop}>Stop</button>
    {/if}
    {#if !isStarted && input.length === 0 && isText}
        <button onclick={fetchText}>Get new text</button>
    {/if}

</div>

<style>
    a
    {
        color: #4CAF50;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    .test {
        font-size: 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        width: 100%;
        height: 100%;
    }
    input {
        width: 300px;
        height: 32px;
        font-size: 18px;
        padding: 8px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }
    .results {
        position: absolute;
        border: 2px solid white;
        border-radius: 16px;
        width: 600px;
        height: 400px;
        background: rgba(0,0,0, 0.8);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .type-box {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .displayer {
        display: flex;
        flex-wrap: wrap;
        max-width: 80vw;
    }

    .correct {
        color: green;
    }

    .incorrect {
        color: red;
    }

    .not-typed {
        color: rgb(212, 212, 212);
    }

    .space {
        width: 0.5rem;
    }
</style>