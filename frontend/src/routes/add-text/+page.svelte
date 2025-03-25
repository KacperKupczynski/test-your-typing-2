<script lang="ts">
    let content = '';

    async function addText() {
        const response = await fetch('http://localhost:8000/api/addText/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ content })
        });

        if (response.ok) {
            alert('Text added successfully');
        } else {
            alert('Failed to add text');
        }
    }
</script>

<h1>Add your text</h1>

<form on:submit|preventDefault={addText}>
    <label>
        Text:
        <textarea bind:value={content} placeholder="Enter your text"></textarea>
    </label>
    <button type="submit">Add text</button>
</form>