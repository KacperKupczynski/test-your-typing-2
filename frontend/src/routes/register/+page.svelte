<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';

    async function register() {
        const response = await fetch('http://localhost:3000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.token);
            localStorage.setItem('refresh_token', data.refreshToken);
            goto('/');
        } else {
            alert('Registration failed');
        }
    }
</script>

<form on:submit|preventDefault={register}>
    <label>
        Username:
        <input type="text" bind:value={username} />
    </label>
    <label>
        Password:
        <input type="password" bind:value={password} />
    </label>
    <button type="submit">Register</button>
</form>