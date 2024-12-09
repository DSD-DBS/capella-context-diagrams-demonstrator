/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import { useSettingsStore } from '@/stores/settings';
import Button from 'primevue/button';
import TieredMenu from 'primevue/tieredmenu';
import { ref } from "vue";

const menu = ref();
const settings = useSettingsStore();
const EXAMPLES_PATH = "/examples";

const SAMPLES = [
    { label: 'Empty', command: () => settings.yamlCode = '' },
    { label: 'Context', command: () => loadSample('context.yml') },
    { label: 'Component Exchanges', command: () => loadSample('exchanges.yml') },
    { label: 'Physical Ports', command: () => loadSample('ports.yml') },
    { label: 'Classes', command: () => settings.yamlCode = 'tree_view' },
    { label: 'Realization View', command: () => settings.yamlCode = 'realization_view' },
    { label: 'Data Flow', command: () => loadSample('dataflow.yml') },
    { label: 'Cable Tree', command: () => settings.yamlCode = 'cable_tree' },
    {
        separator: true,
    },
    {
        label: 'Upload File',
        icon: 'pi pi-upload',
        command: () => document.getElementById('file-upload').click(),
    },
];

const items = [
    {
        label: 'Save',
        command: () => settings.saveCode(),
    },
    {
        label: 'Load',
        items: SAMPLES,
    },
];

function loadSample(selectedFile) {
    settings.loadCode(`${EXAMPLES_PATH}/${selectedFile}`);
}

const toggle = (event) => {
    menu.value.toggle(event);
};

function loadFile(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        settings.yamlCode = e.target.result;
    };
    reader.readAsText(file);
}
</script>

<template>
    <div class="card flex justify-center">
        <Button type="button" label="File" @click="toggle" aria-haspopup="true" aria-controls="overlay_file"
            severity="secondary" variant="text" />
        <TieredMenu ref="menu" id="overlay_file" :model="items" popup />
    </div>
    <input type="file" id="file-upload" style="display: none" @change="loadFile($event)" />
</template>
