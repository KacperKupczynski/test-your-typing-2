<script lang="ts">
    import { onMount } from "svelte";

    let text = "";
    let letterStates: { letter: string; state: string }[] = [];
    let input = '';
    let time = 0;
    let interval = 0;
    let isStarted = false;
    let wpm = 0;

    onMount(async () => {
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
    });

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

    function stop() {
        clearInterval(interval);
        isStarted = false;
        if (checkCorrectness()) {
            alert('You typed the text correctly!');
        } else {
            alert('You made a mistake!');
        }
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
        <input type="text" name="" id="" bind:value={input} on:input={checkInput} placeholder="Type text above"/>
        <p>WPM: {wpm.toFixed(2)}</p>
        <p>Time: {time.toFixed(2)}</p>
    </div>
</div>

<style>
    .test {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    input {
        width: 300px;
        padding: 8px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: white;
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