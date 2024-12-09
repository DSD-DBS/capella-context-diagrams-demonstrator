/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import { useSettingsStore } from '@/stores/settings';
import ContextMenu from 'primevue/contextmenu';
import { onMounted, ref, watch } from 'vue';

const settings = useSettingsStore();
const menu = ref();
const items = ref([
    { label: 'Save', command: settings.saveSVG },
]);

watch(() => settings.svgContent, () => {
    setTimeout(() => {
        initPanZoom();
    }, 0);
});

const onImageRightClick = (event) => {
    menu.value.show(event);
};

function initPanZoom() {
    svgPanZoom('#pan-zoom');
}

onMounted(() => {
    initPanZoom();
});
</script>


<template>
    <div class="flex flex-col items-center flex-1">
        <h2 v-if="settings.previewConfigs.showTitle" class="text-xl font-semibold">{{ settings.svgName }}</h2>
        <div class="flex-1 w-full" id="svg-container" v-html="settings.svgContent" @contextmenu="onImageRightClick">
        </div>
    </div>
    <ContextMenu ref="menu" :model="items" />
</template>
