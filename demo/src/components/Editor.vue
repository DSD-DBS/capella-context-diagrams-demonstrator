/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import FileMenu from "@/components/FileMenu.vue";
import Settings from "@/components/Settings.vue";
import SVGDisplay from "@/components/SVGDisplay.vue";
import TargetBrowser from "@/components/TargetBrowser.vue";
import { useSettingsStore } from '@/stores/settings';
import Button from "primevue/button";
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import { onMounted, ref } from "vue";

const settings = useSettingsStore();
const settingsModal = ref(null);

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
    <nav class="flex gap-2 items-center px-4 py-2">
        <div class="flex flex-1 items-center gap-2">
            <h1 class="text-2xl font-semibold">CCDD</h1>
            <FileMenu />
            <slot name="edit-menu" />
        </div>
        <div class="flex gap-2 items-center">
            <slot name="run-button" />
        </div>
        <div class="flex flex-1 justify-end items-center">
            <Button icon="pi pi-cog" aria-label="Open settings" @click="settingsModal.visible = true"
                severity="secondary" text />
            <Button v-if="settings.dark" icon="pi pi-sun" aria-label="Turn off dark mode" @click="toggleTheme"
                severity="secondary" text />
            <Button v-else icon="pi pi-moon" aria-label="Turn on dark mode" @click="toggleTheme" severity="secondary"
                text />
        </div>
    </nav>
    <main class="flex-1 min-h-0 px-4">
        <Splitter class="h-full">
            <SplitterPanel class="flex flex-col h-full">
                <Splitter layout="vertical" class="h-full">
                    <SplitterPanel class="flex flex-col">
                        <slot name="editor" />
                    </SplitterPanel>
                    <SplitterPanel class="flex flex-col" v-if="settings.previewConfigs.showBrowser">
                        <TargetBrowser />
                    </SplitterPanel>
                </Splitter>
            </SplitterPanel>
            <SplitterPanel class="flex flex-col">
                <SVGDisplay />
            </SplitterPanel>
        </Splitter>
    </main>
    <footer class="flex items-center justify-between px-4 py-2">
        <a href="https://github.com/DSD-DBS/capella-context-collector/issues" target="_blank" rel="noopener noreferrer"
            class="flex items-center gap-2">
            <i class="pi pi-github"></i>
            <span>Report an issue</span>
        </a>
        <p>© 2024 DB InfraGO AG</p>
    </footer>
    <Settings ref="settingsModal" />
</template>
