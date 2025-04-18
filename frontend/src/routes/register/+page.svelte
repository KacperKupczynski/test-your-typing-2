<script>
    import { goto } from '$app/navigation';
    import { API_URL } from '$lib/index';


    let username = '';
    let password = '';

    async function register() {
        const response = await fetch(`${API_URL}/api/register/`, {
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
            goto('/');
        } else {
            alert('Registration failed');
        }
    }
</script>

<form on:submit|preventDefault={register}>
    <h1>Register</h1>
    <div class="field">
        <label for="">Username:</label>
        <input name="username" type="text" bind:value={username} />
    </div>
    <div class="field">
        <label for="password">Password:</label>
        <input name="password" type="password" bind:value={password} />
    </div>
    <button type="submit">Register</button>
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