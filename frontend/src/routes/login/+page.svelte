<script lang="ts">
    import { goto } from '$app/navigation';
    import { user } from '../../stores/user';

    let username = '';
    let password = '';

    async function login() {
        const response = await fetch('http://localhost:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            user.set(username); // setting the user in the store
            //goto('/'); 
        } else {
            alert('Login failed. Please check your credentials.');
        }
    }
</script>

<h1>Login</h1>

<form on:submit|preventDefault={login}>
    <label>
        Username:
        <input type="text" bind:value={username} placeholder="Enter your username" />
    </label>
    <label>
        Password:
        <input type="password" bind:value={password} placeholder="Enter your password" />
    </label>
    <button type="submit">Login</button>
</form>