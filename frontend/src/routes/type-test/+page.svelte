<script lang="ts">

let input = '';
let time = 0;
let text = 'Lorem ipsum';
let isStarted = false;

let wpm = 0;

function startTyping() {
    if (!isStarted) {
        isStarted = true;
        startTimer();
    }
}

function startTimer() {
    setInterval(() => {
        time++;
        calcWPM();
    }, 1000);
}
    
function calcWPM() {
    const chars = input.length;
    const words = chars / 5;
    wpm = words / (time / 60);
}

</script>

<h1>Typing test</h1>
<div class="test">
    <p>{text}</p>
    <input type="text" name="" id="" bind:value={input} on:input={startTyping} />
    <p>{time}</p>
    <p>{wpm}</p>
</div>