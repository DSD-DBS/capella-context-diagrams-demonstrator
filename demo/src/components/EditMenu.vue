/*
* Copyright DB InfraGO AG and contributors
* SPDX-License-Identifier: Apache-2.0
*/

<script setup>
import Menu from '@/components/Menu.vue';
import { useSettingsStore } from '@/stores/settings';

const settings = useSettingsStore();

const props = defineProps({
    triggerKeyboardCommand: {
        type: Function,
        required: true,
    },
    triggerSourceCommand: {
        type: Function,
        required: true,
    },
});

const items = [
    {
        label: 'Undo',
        shortcut: settings.superKey + ' + Z',
        command: () => props.triggerKeyboardCommand('undo'),
    },
    {
        label: 'Redo',
        shortcut: settings.superKey + ' + Y',
        command: () => props.triggerKeyboardCommand('redo'),
    },
    {
        separator: true,
    },
    {
        label: 'Cut',
        shortcut: settings.superKey + ' + X',
        command: () => props.triggerKeyboardCommand('editor.action.clipboardCutAction'),
    },
    {
        label: 'Copy',
        shortcut: settings.superKey + ' + C',
        command: () => props.triggerKeyboardCommand('editor.action.clipboardCopyAction'),
    },
    {
        label: 'Paste',
        shortcut: settings.superKey + ' + V',
        command: () => props.triggerKeyboardCommand('editor.action.clipboardPasteAction'),
    },
    {
        separator: true,
    },
    {
        label: 'Find',
        shortcut: settings.superKey + ' + F',
        command: () => props.triggerKeyboardCommand('actions.find'),
    },
    {
        label: 'Replace',
        shortcut: settings.superKey + ' + H',
        command: () => props.triggerKeyboardCommand('editor.action.startFindReplaceAction'),
    },
    {
        separator: true,
    },
    {
        label: 'Toggle Line Comment',
        shortcut: settings.superKey + ' + Shift + 7',
        command: () => props.triggerKeyboardCommand('editor.action.commentLine'),
    },
];
</script>

<template>
    <Menu label="Edit" :items="items" overlay_id="overlay_edit" />
</template>
