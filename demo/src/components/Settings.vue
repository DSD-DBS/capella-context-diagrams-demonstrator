/*
* Copyright DB InfraGO AG and contributors
* SPDX-License-Identifier: Apache-2.0
*/

<script setup>
import { useSettingsStore } from '@/stores/settings';
import { FloatLabel } from 'primevue';
import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';
import Drawer from 'primevue/drawer';
import InputText from 'primevue/inputtext';
import { ref } from 'vue';

const settings = useSettingsStore();
const visible = ref(false);
const editorOptions = ref({ ...settings.editorOptions });
const previewConfigs = ref({ ...settings.previewConfigs });

function saveConfigs() {
    settings.editorOptions = { ...editorOptions.value };
    settings.previewConfigs = { ...previewConfigs.value };
    visible.value = false;
}

function resetConfigs() {
    editorOptions.value = { ...settings.editorOptions };
    previewConfigs.value = { ...settings.previewConfigs };
}

defineExpose({ visible });
</script>

<template>
    <Drawer v-model:visible="visible" header="Settings" position="right" :showCloseIcon="false" @show="resetConfigs">
        <div class="flex flex-col gap-4">
            <h2 class="text-lg font-semibold">Editor settings</h2>
            <FloatLabel variant="on">
                <InputText id="font-size" name="font-size" v-model="editorOptions.fontSize" class="w-full"
                    v-keyfilter.int />
                <label for="font-size">Font size</label>
            </FloatLabel>
            <FloatLabel variant="on">
                <InputText id="tab-size" name="font-size" v-model="editorOptions.tabSize" class="w-full"
                    v-keyfilter.int />
                <label for="tab-size">Tab size</label>
            </FloatLabel>
            <h2 class="text-lg font-semibold">Preview settings</h2>
            <div class="flex gap-2 items-center">
                <Checkbox v-model="previewConfigs.showTitle" inputId="showTitle" binary />
                <label for="showTitle"> Show diagram name </label>
            </div>
            <div class="flex gap-2 items-center">
                <Checkbox v-model="previewConfigs.showBrowser" inputId="showBrowser" binary />
                <label for="showBrowser"> Show target browser </label>
            </div>
            <div class="flex justify-end gap-2 items-center">

                <Button type="button" label="Cancel" severity="secondary" @click="visible = false" />
                <Button type="button" label="Save" @click="saveConfigs" />
            </div>
        </div>
    </Drawer>
</template>
