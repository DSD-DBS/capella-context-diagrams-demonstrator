/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

<script setup>
import { ProgressSpinner } from "primevue";
import Button from 'primevue/button';
import TieredMenu from 'primevue/tieredmenu';
import { ref } from "vue";
import Editor from './components/Editor.vue';
import { useSettingsStore } from './stores/settings';

const settings = useSettingsStore();
const loading = ref(false);
const editorRef = ref();
const editMenuRef = ref();

function handleMount(editorInstance) {
    editorRef.value = editorInstance;

    if (editorRef.value) {
        editorRef.value.addAction({
            id: 'runCodeHotkey',
            label: 'Run Code',
            keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
            precondition: null,
            keybindingContext: null,
            contextMenuGroupId: 'navigation',
            contextMenuOrder: 1.5,
            run: function (ed) {
                run();
            }
        });
        editorRef.value.addAction({
            id: 'commentLineHotkey',
            label: 'Comment Line',
            keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Digit7],
            precondition: null,
            keybindingContext: null,
            contextMenuGroupId: 'navigation',
            contextMenuOrder: 1.5,
            run: function (ed) {
                triggerSourceCommand('editor.action.commentLine');
            }
        })
    } else {
        console.error('Editor instance is not defined');
    }
}


async function handleBeforeMount(monaco) {
    const diag_types = ['custom_diagram', 'context_diagram', 'cable_tree', 'data_flow_view', 'realization_view', 'tree_view'];
    const properties = ['display_parent_relation', 'hide_direct_children', 'slim_center_box', 'display_port_labels', 'port_label_position', 'display_unused_ports', 'transparent_background', 'display_symbols_as_boxes', 'unify_edge_direction', 'name', 'display_derived_interfaces'];
    const methods = ['get', 'include', 'filter', 'collect', 'repeat'];

    const customTokenizer = {
        root: [
            ...diag_types.map(diag_type => [new RegExp(`\\b(${diag_type})\\b`), 'keyword']),
            ...properties.map(property => [new RegExp(`\\b(${property})\\b`), 'attribute.name']),
            ...methods.map(method => [new RegExp(`\\b(${method})\\b`), 'keyword']),
        ]
    };

    const allLangs = await monaco.languages.getLanguages();
    const { language: yamlLang } = await allLangs.find(({ id }) => id === 'yaml').loader();

    for (const category in customTokenizer) {
        const tokenDefs = customTokenizer[category];
        if (!yamlLang.tokenizer.hasOwnProperty(category)) {
            yamlLang.tokenizer[category] = [];
        }
        if (Array.isArray(tokenDefs)) {
            yamlLang.tokenizer[category].unshift.apply(yamlLang.tokenizer[category], tokenDefs);
        }
    }

    const keywords = ['true', 'True', 'TRUE', 'false', 'False', 'FALSE', 'null', 'Null', 'Null', '~'];
    const commonStrings = ['ports', 'inputs', 'outputs', 'links', 'exchanges', 'source', 'target', 'allocated_functional_exchanges', 'allocated_interactions', 'physical_ports', 'components', 'involved_activities', 'involved_functions'];

    monaco.languages.registerCompletionItemProvider('yaml', {
        triggerCharacters: [],
        provideCompletionItems: () => {
            return {
                suggestions: [
                    ...keywords.map(keyword => ({
                        label: keyword,
                        kind: monaco.languages.CompletionItemKind.Keyword,
                        insertText: keyword,
                    })),
                    ...diag_types.map(diag_type => ({
                        label: diag_type,
                        kind: monaco.languages.CompletionItemKind.Interface,
                        insertText: `${diag_type}:\n\t`,
                    })),
                    ...properties.map(property => ({
                        label: property,
                        kind: monaco.languages.CompletionItemKind.Property,
                        insertText: `${property}: `,
                    })),
                    ...methods.map(method => ({
                        label: method,
                        kind: monaco.languages.CompletionItemKind.Method,
                        insertText: `${method}:\n\t`,
                    })),
                    ...commonStrings.map(commonString => ({
                        label: commonString,
                        kind: monaco.languages.CompletionItemKind.Text,
                        insertText: `${commonString}`,
                    })),
                ],
            };
        },
    });
}


function triggerKeyboardCommand(command) {
    editorRef.value?.trigger('keyboard', command, null);
}

function triggerSourceCommand(command) {
    editorRef.value?.trigger('source', command);
}

function isApple() {
    const platform =
        window.navigator?.userAgentData?.platform || window.navigator.platform;
    const macosPlatforms = ["Macintosh", "MacIntel", "MacPPC", "Mac68K"];
    const iosPlatforms = ["iPhone", "iPad", "iPod"];

    if ((macosPlatforms.indexOf(platform) !== -1) || (iosPlatforms.indexOf(platform) !== -1)) {
        return true;
    } else {
        return false;
    }
}

const superKey = isApple() ? '⌘' : 'Ctrl';

const items = [
    {
        label: 'Undo',
        shortcut: superKey + ' + Z',
        command: () => triggerKeyboardCommand('undo'),
    },
    {
        label: 'Redo',
        shortcut: superKey + ' + Y',
        command: () => triggerKeyboardCommand('redo'),
    },
    {
        separator: true,
    },
    {
        label: 'Cut',
        shortcut: superKey + ' + X',
        command: () => triggerSourceCommand('editor.action.clipboardCutAction'),
    },
    {
        label: 'Copy',
        shortcut: superKey + ' + C',
        command: () => triggerSourceCommand('editor.action.clipboardCopyAction'),
    },
    {
        label: 'Paste',
        shortcut: superKey + ' + V',
        command: () => triggerSourceCommand('editor.action.clipboardPasteAction'),
    },
    {
        separator: true,
    },
    {
        label: 'Find',
        shortcut: superKey + ' + F',
        command: () => triggerKeyboardCommand('actions.find'),
    },
    {
        label: 'Replace',
        shortcut: superKey + ' + H',
        command: () => triggerKeyboardCommand('editor.action.startFindReplaceAction'),
    },
    {
        separator: true,
    },
    {
        label: 'Toggle Line Comment',
        shortcut: superKey + ' + Shift + 7',
        command: () => triggerSourceCommand('editor.action.commentLine'),
    },
];

function toggle(event) {
    editMenuRef.value.toggle(event);
}

async function run() {
    loading.value = true;
    await settings.renderDiagram();
    loading.value = false;
}
</script>

<template>
    <Editor>
        <template #edit-menu>
            <div class="card flex justify-center">
                <Button type="button" label="Edit" @click="toggle" aria-haspopup="true" aria-controls="overlay_edit"
                    severity="secondary" variant="text" />
                <TieredMenu ref="editMenuRef" id="overlay_edit" :model="items" popup>
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
        <template #run-button>
            <Button v-tooltip="{ value: superKey + ' + Enter', showDelay: 1000, hideDelay: 300 }" label="Run" @click="run"
                :disabled="loading" icon="pi pi-play" />
            <ProgressSpinner
                :style="'width: 1.5rem; height: 1.5rem; position: absolute; margin: 0 -2.5rem;' + (loading ? 'visibility: visible;' : 'visibility: hidden;')"
                strokeWidth="8" fill="transparent" />
        </template>
        <template #editor>
            <vue-monaco-editor v-model:value="settings.yamlCode" :theme="settings.dark ? 'vs-dark' : 'vs'"
                :options="settings.editorOptions" language="yaml" @mount="handleMount"
                @beforeMount="handleBeforeMount" />
        </template>
    </Editor>
</template>
