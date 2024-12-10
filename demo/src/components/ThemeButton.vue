/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import { useSettingsStore } from '@/stores/settings';
import Button from "primevue/button";
import { onMounted } from "vue";

const settings = useSettingsStore();

function toggleTheme() {
    document.documentElement.classList.toggle("dark");
    settings.toggleDark();
}


onMounted(async () => {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        toggleTheme();
    }
});
</script>

<template>
    <Button v-if="settings.dark" icon="pi pi-sun" aria-label="Turn off dark mode" @click="toggleTheme"
        severity="secondary" text />
    <Button v-else icon="pi pi-moon" aria-label="Turn on dark mode" @click="toggleTheme" severity="secondary" text />
</template>
