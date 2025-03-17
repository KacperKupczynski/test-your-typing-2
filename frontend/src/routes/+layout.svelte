<script>
    import { user } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    onMount(async () => {
        const response = await fetch('http://localhost:3000/api/getUser', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        });

        if (response.ok) {
            user.set(true);
        } else {
            user.set(false);
        }
    });
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
            {#if user}
                <a href="/logout">Logout</a>
            {:else}
                <a href="/login">Login</a>
                <a href="/register">Register</a>
            {/if}
        </p>
    </ul>
    
</nav>

<main>
    <slot>
    </slot>
</main>