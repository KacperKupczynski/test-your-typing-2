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
            goto('/'); 
        } else {
            alert('Login failed. Please check your credentials.');
        }
    }
</script>



<form on:submit|preventDefault={login}>
    <h1>Login</h1>
    <div class="field">
        <label for="username">
            Username:
        </label>
        <input type="text" bind:value={username} placeholder="Enter your username" />
    </div>
    <div class="field">
        <label for="password">
            Password:
        </label>
        <input type="password" bind:value={password} placeholder="Enter your password" />
    </div>
    <button type="submit">Login</button>
</form>

<style>

    h1 {
        text-align: center;
    }
    form {
        display: flex;
        flex-direction: column;
        width: 600px;
        border: 3px solid #f1f1f1;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        align-items: center;
        
    }

    .field {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    label {
        padding: 5px;
    }

    input {
        height: 2rem;
        padding: 6px;
        margin-bottom: 2rem;
        border-radius: 8px;
        font-size: 16px;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 16px;
        cursor: pointer;
        width: 30%;
    }
</style>