<script lang="ts">
    import { goto } from '$app/navigation';
    import { user } from '../../stores/user';
    import { API_URL } from '$lib/index';

    let username = '';
    let password = '';
    let message = '';
    let loading = false;

    async function login() {
        // Clear previous error messages
        message = '';
        loading = true;

        // Validate inputs
        if (!username.trim()) {
            message = 'Username is required';
            loading = false;
            return;
        }

        if (!password.trim()) {
            message = 'Password is required';
            loading = false;
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                // Fetch the user details and update the store
                const userResponse = await fetch(`${API_URL}/api/getUser/`, {
                    headers: {
                        Authorization: `Bearer ${data.access}`
                    }
                });

                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    user.set(userData.username); // Update the user store
                    window.location.href = '/'; // Use window.location for full page reload
                }
            } else {
                // Handle specific error cases
                if (response.status === 400) {
                    message = data.error || 'Please provide both username and password';
                } else if (response.status === 401) {
                    message = 'Invalid username or password';
                } else {
                    message = 'Login failed. Please try again.';
                }
            }
        } catch (error) {
            message = 'Network error. Please try again.';
            console.error('Login error:', error);
        } finally {
            loading = false;
        }
    }
</script>

<form on:submit|preventDefault={login}>
    <h1>Login</h1>
    <div class="field">
        <label for="username">
            Username:
        </label>
        <input 
            name="username" 
            type="text" 
            bind:value={username} 
            placeholder="Enter your username"
            disabled={loading}
            autofocus
        />
    </div>
    <div class="field">
        <label for="password">
            Password:
        </label>
        <input 
            type="password" 
            bind:value={password} 
            placeholder="Enter your password"
            disabled={loading} 
        />
    </div>
    
    {#if message}
        <div class="error-message">
            {message}
        </div>
    {/if}
    
    <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
    </button>
    <p>
        Don't have an account? <a href="/register">Register here</a>
    </p>
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

    a {
        color: #4CAF50;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
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
    
    .error-message {
        color: #ff5555;
        background-color: rgba(255, 85, 85, 0.1);
        border: 1px solid #ff5555;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        width: 100%;
        text-align: center;
    }
    
    button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
</style>