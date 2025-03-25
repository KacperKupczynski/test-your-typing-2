import { writable } from 'svelte/store';

export const user = writable(null); // Store for the logged-in user