<script>
    import { onDestroy, onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '../stores/user';
    import "../app.css";
    import { API_URL } from '$lib';

    let loading = true;
    let refreshInterval;

    async function refreshAccessToken() {
        console.log('Refreshing access token...');
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            logout();
            return null;
        }

        const response = await fetch(`${API_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            console.log ('Access token refreshed');
            return data.access;
        } else {
            logout();
            goto('/login');
            return null;
        }
    }

    onMount(async () => {
        const response = await fetch(`${API_URL}/api/getUser/`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            user.set(data.username); // setting username in the store
        } else {
            user.set(null); // clearing the store
            goto('/login');
        }
        loading = false;

        refreshInterval = setInterval(() => {
            refreshAccessToken();
        }, 4 * 60 * 1000); // Refresh token every 4 minutes

    });
    onDestroy(() => {
            clearInterval(refreshInterval);
        });

    function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        user.set(null);
        goto('/login');
    }
</script>

{#if loading}
    <div class="loading">Loading...</div>
{:else}
    {#if $user}
    <nav>
        <a href="/">
            <img src="./logo.png" alt="logo" class="logo" />
        </a>
        <ul>
            <li>
                <a href="/type-test">Start typing</a>
            </li>
            <li>
                <a href="/history">History</a>
            </li>
            <li>
                <a href="/add-text">Add your text</a>
            </li>
            <li>
                <a href="/text-list">List of your texts</a>
            </li>
        </ul>
        <div class="user-info">
            <p>{$user}</p>
            <button on:click={logout}>Logout</button>
        </div>
    </nav>
    {/if}
        
    <main>
        <slot></slot>
    </main>
{/if}
<style>
    nav {
        display: flex;
        align-items: center;
        justify-content: right;
        padding: 1rem;
        height: 3rem;
        color: white;
        background-color: rgba(129, 129, 129, 0);
        background-image: linear-gradient(0deg, rgba(129, 129, 129, 0) 0%, rgba(0, 0, 0, 0.69) 10%);
    }

    nav ul {
        display: flex;
        width: 100%;
        list-style: none;
    }

    nav ul li {
        padding: 1rem;
        display: flex;
        align-items: center;
    }

    nav ul li a {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo {
        margin-top: 12px;
    }

    nav p {
        margin-left: 10rem;
        padding: 2rem;
    }
    a {
        color: white;
        text-decoration: none;
    }

    .user-info {
        display: flex;
        align-items: center;
        margin-left: auto;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100px;
    }
    
    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: calc(100vh - 5rem);
    }
</style>