<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '../stores/user';


    onMount(async () => {
        const response = await fetch('http://localhost:8000/api/getUser/', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            user.set(data.username); // setting username in a store
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
    <ul>
        <li>
            <a href="/type-test">Start typing</a>
        </li>
        <li>
            <a href="/records">Your records</a>
        </li>
        <p>
            {#if $user}
                <p>Welcome, {$user}!</p>
                <button on:click={logout}>Logout</button>
            {:else}
                <a href="/login">Login</a>
                <a href="/register">Register</a>
            {/if}
        </p>
    </ul>
</nav>

<main>
    <slot></slot>
</main>