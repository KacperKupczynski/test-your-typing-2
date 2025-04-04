<script lang="ts">
    import { onMount } from "svelte";
	import { user } from "../../stores/user";

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

    onMount(async () => {
        fetchText();
    });

    async function fetchText() {
        const response = await fetch('http://localhost:8000/api/randomText', {
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
            alert('Failed to get text');
        }
    }

    $: if (input.length == 1 && !isStarted) {
        start();
    }

    $: if (input.length === text.length && isStarted) {
        stop();
    }

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

    function start() {
        isStarted = true;
        interval = setInterval(() => {
            time += 0.01;
            calcWPM();
        }, 10);
    }

    function calcWPM() {
        const chars = input.length;
        const words = chars / 5;
        wpm = words / (time / 60);
    }

    function checkCorrectness() {
        return letterStates.every(letterState => letterState.state === 'correct');
    }
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

    async function stop() {
        clearInterval(interval);
        isStarted = false;
        if (checkCorrectness()) {
            const response = await fetch('http://localhost:8000/api/saveResult/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({
                    text,
                    wpm
                })
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
    <div class="displayer">
        {#each letterStates as { letter, state }, i}
            {#if letter === ' '}
                <span class="space"></span>
            {:else}
                <span class={state}>{letter}</span>
            {/if}
        {/each}
    </div>
    <div class="type-box">
        <input type="text" name="" id="" bind:value={input} oninput={checkInput} placeholder="Type text above"/>
        {#if message}
            <p class="incorrect error">{message}</p>
        {/if}
        <p>WPM: {wpm.toFixed(2)}</p>
        <p>Time: {time.toFixed(2)}</p>
    </div>


    {#if showResults}
        <div class="results">
            <h2>Results</h2>
            <p>WPM: {wpm.toFixed(2)}</p>
            <p>Time: {time.toFixed(2)} seconds</p>
            <button onclick={playAgain}>Play again</button>
            albo spacja powinno byc
        </div>
    {/if}
</div>

<style>

    .test {
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