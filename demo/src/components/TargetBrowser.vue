/*
* Copyright DB InfraGO AG and contributors
* SPDX-License-Identifier: Apache-2.0
*/

<script setup>
import { useSettingsStore } from '@/stores/settings';
import AutoComplete from 'primevue/autocomplete';
import Breadcrumb from 'primevue/breadcrumb';
import Button from 'primevue/button';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';

const toast = useToast();
const settings = useSettingsStore();
const selectedElement = ref("");
const filteredElements = ref([]);

function handleHlink(event) {
    if (event.target.tagName === 'A' && event.target.href.startsWith('hlink://')) {
        event.preventDefault();
        const uuid = event.target.href.replace('hlink://', '');
        settings.addBreadcrum(uuid);
    }
}

async function loadTarget() {
    console.log(selectedElement.value);
    if (selectedElement.value.uuid ?? false) {
        selectedElement.value = selectedElement.value.uuid;
    }
    let result = await settings.validateTarget(selectedElement.value);
    if (result.status === 'success') {
        settings.targetUUID = selectedElement.value;
        settings.tableBreadcrumbs = [];
        settings.addBreadcrum(selectedElement.value);
        return;
    }
    selectedElement.value = settings.targetUUID;
    toast.add({ severity: 'error', summary: result.name, detail: result.message, life: 3000 });
}

const search = (event) => {
    setTimeout(() => {
        if (!event.query.length) {
            filteredElements.value = [...settings.modelElements];
        } else {
            filteredElements.value = settings.modelElements.filter((elem) => {
                return elem.name.toLowerCase().includes(event.query.toLowerCase()) || elem.uuid.includes(event.query);
            });
        }
    }, 250);
}

onMounted(async () => {
    document.addEventListener('click', handleHlink);
    await settings.getAllElements();
});
</script>
<template>
    <div class="h-full overflow-auto">
        <div class="flex sticky top-0 flex-grow searchbar">
            <Breadcrumb :model="settings.tableBreadcrumbs" class="flex-1 overflow-auto">
            </Breadcrumb>
            <InputGroup class="flex-1 p-2">
                <AutoComplete v-model="selectedElement" optionLabel="uuid" :suggestions="filteredElements"
                    :invalid="!settings.targetUUID" @complete="search" :completeOnFocus="true"
                    @keydown.enter="loadTarget" @option-select="loadTarget">
                    <template #option="slotProps">
                        <div class="flex items-center">
                            <div>{{ slotProps.option.name }}</div>
                            <div class="text-xs text-gray-500 ml-2">{{ slotProps.option.uuid }}</div>
                        </div>
                    </template>
                </AutoComplete>
                <InputGroupAddon>
                    <Button type="submit" icon="pi pi-search" severity="secondary" variant="text" @click="loadTarget" />
                </InputGroupAddon>
            </InputGroup>
        </div>
        <div v-html="settings.tableContent" class="px-4 pb-4" />
    </div>
    <Toast />
</template>

<style scoped>
.searchbar {
    background-color: var(--p-breadcrumb-background);
}
</style>
