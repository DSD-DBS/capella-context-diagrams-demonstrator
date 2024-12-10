/*
* Copyright DB InfraGO AG and contributors
* SPDX-License-Identifier: Apache-2.0
*/

<script setup>
import Button from 'primevue/button';
import TieredMenu from 'primevue/tieredmenu';
import { ref } from "vue";

const props = defineProps({
    label: {
        type: String,
        required: true,
    },
    items: {
        type: Array,
        required: true,
    },
    overlay_id: {
        type: String,
        required: true,
    },
});

const menu = ref();

const toggle = (event) => {
    menu.value.toggle(event);
};
</script>


<template>
    <div class="card flex justify-center">
        <Button type="button" :label="label" @click="toggle" aria-haspopup="true" :aria-controls="overlay_id"
            severity="secondary" variant="text" />
        <TieredMenu ref="menu" :id="overlay_id" :model="items" popup>
            <template #item="{ item, props, hasSubmenu }">
                <a class="flex items-center justify-between" v-bind="props.action">
                    <span class="ml-2">{{ item.label }}</span>
                    <span v-if="item.shortcut"
                        class="border border-surface rounded bg-emphasis text-muted-color text-xs p-1">{{
                            item.shortcut }}</span>
                    <i v-if="hasSubmenu" class="pi pi-angle-right"></i>
                </a>
            </template>
        </TieredMenu>
    </div>
</template>
