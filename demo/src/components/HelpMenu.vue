/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import Button from 'primevue/button';
import TieredMenu from 'primevue/tieredmenu';
import { ref } from "vue";

const menu = ref();

const items = [
    {
        label: 'Documentation',
        url: 'https://dsd-dbs.github.io/capella-context-diagrams-demonstrator',
    },
    {
        label: 'Report Issue',
        url: 'https://github.com/DSD-DBS/capella-context-diagrams-demonstrator/issues',
    },
];

const toggle = (event) => {
    menu.value.toggle(event);
};
</script>

<template>
    <div class="card flex justify-center">
        <Button type="button" label="Help" @click="toggle" aria-haspopup="true" aria-controls="overlay_file"
            severity="secondary" variant="text" />
        <TieredMenu ref="menu" id="overlay_file" :model="items" popup />
    </div>
</template>
