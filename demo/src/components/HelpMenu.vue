/*
* Copyright DB InfraGO AG and contributors
* SPDX-License-Identifier: Apache-2.0
*/

<script setup>
import Menu from '@/components/Menu.vue';

const items = [
    {
        label: 'Documentation',
        command: () => {
            window.open('https://dsd-dbs.github.io/capella-context-diagrams-demonstrator', '_blank');
        },
    },
    {
        label: 'Report Issue',
        command: () => {
            window.open('https://github.com/DSD-DBS/capella-context-diagrams-demonstrator/issues', '_blank');
        },
    },
    {
        label: 'Show Release Notes',
        command: () => {
            window.open('https://github.com/DSD-DBS/capella-context-diagrams-demonstrator/releases', '_blank');
        },
    },
];
</script>

<template>
    <Menu label="Help" :items="items" overlay_id="overlay_help" />
</template>
