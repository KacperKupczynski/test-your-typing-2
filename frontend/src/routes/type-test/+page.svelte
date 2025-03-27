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
            letterStates = text.split('').map(letter => ({ letter, state: 'not-typed' }));
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
        let correct = false;
        letterStates.forEach(letterState => {
            if (letterState.state === 'correct') {
                correct = true;
            } else {
                correct = false;
            }
        });
        return correct;
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

<h1>Typing test</h1>
<div class="test">
    <div class="displayer">
        {#each letterStates as { letter, state }, i}
            <span class={state}>{letter}</span>
        {/each}
    </div>
    <input type="text" name="" id="" bind:value={input} on:input={checkInput} />
    <p>{time.toFixed(2)}</p>
    <p>{wpm.toFixed(2)}</p>
</div>



<style>
    .test {
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
        color: black;
    }
</style>