<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '../stores/user';
    import "../app.css";


    onMount(async () => {
        const response = await fetch('http://localhost:8000/api/getUser/', {
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
    });

    function logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        user.set(null);
        goto('/login');
    }
</script>

<nav>
    <a href="/">
        <img src="./logo.png" alt="logo" class="logo" />
    </a>
    <ul>
        <li>
            <a href="/type-test">Start typing</a>
        </li>
        <li>
            <a href="/records">Your records</a>
        </li>
        <li>
            <a href="/add-text">Add your text</a>
        </li>
        <li>
            <a href="/text-list">List of your texts</a>
        </li>
    </ul>
    <div class="user-info">
        {#if $user}
            <p>{$user}</p>
            <button on:click={logout}>Logout</button>
        {:else}
            <a href="/login">Login</a>
        {/if}
    </div>
</nav>

<main>
    <slot></slot>
</main>

<style>
    nav {
        display: flex;
        align-items: center;
        justify-content: right;
        padding: 1rem;
        height: 3rem;
        background-color: #333;
        color: white;
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
        margin-left: 10rem;;
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
    }
    
    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: calc(100vh - 4rem);
    }
</style>