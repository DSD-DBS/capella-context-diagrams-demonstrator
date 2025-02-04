<script setup>
/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import { Button, ProgressSpinner, Splitter, SplitterPanel } from "primevue";
import { ref } from "vue";
import EditMenu from "./components/EditMenu.vue";
import FileMenu from "./components/FileMenu.vue";
import HelpMenu from "./components/HelpMenu.vue";
import Settings from "./components/Settings.vue";
import SVGDisplay from "./components/SVGDisplay.vue";
import TargetBrowser from "./components/TargetBrowser.vue";
import ThemeButton from "./components/ThemeButton.vue";
import { useSettingsStore } from "./stores/settings";

const settings = useSettingsStore();
const loading = ref(false);
const editorRef = ref();
const settingsModal = ref();

function handleMount(editorInstance) {
  editorRef.value = editorInstance;

  if (editorRef.value) {
    editorRef.value.addAction({
      id: "runCodeHotkey",
      label: "Run Code",
      keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
      precondition: null,
      keybindingContext: null,
      contextMenuGroupId: "navigation",
      contextMenuOrder: 1.5,
      run: function (ed) {
        run();
      },
    });
    editorRef.value.addAction({
      id: "commentLineHotkey",
      label: "Comment Line",
      keybindings: [
        monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Digit7,
      ],
      precondition: null,
      keybindingContext: null,
      contextMenuGroupId: "navigation",
      contextMenuOrder: 1.5,
      run: function (ed) {
        triggerSourceCommand("editor.action.commentLine");
      },
    });
  } else {
    console.error("Editor instance is not defined");
  }
}

async function handleBeforeMount(monaco) {
  const diag_types = [
    "context_diagram",
    "cable_tree",
    "data_flow_view",
    "realization_view",
    "tree_view",
  ];
  const properties = [
    "display_parent_relation",
    "mode",
    "slim_center_box",
    "display_port_labels",
    "port_label_position",
    "display_unused_ports",
    "transparent_background",
    "display_symbols_as_boxes",
    "edge_direction",
    "display_derived_interfaces",
    "display_actor_relation",
    "hide_context_owner",
    "include_interface",
    "include_port_allocations",
    "hide_functions",
    "include_children_context",
    "edgeRouting",
    "direction",
    "nodeSizeConstraints",
    "edgeLabelsSide",
    "partitioning",
    "collect",
    "depth",
    "super",
    "sub",
    "name",
    "search_direction",
    "show_owners",
    "layer_sizing",
  ];
  const methods = ["get", "include", "filter", "repeat"];

  const customTokenizer = {
    root: [
      ...diag_types.map((diag_type) => [
        new RegExp(`\\b(${diag_type})\\b`),
        "keyword",
      ]),
      ...properties.map((property) => [
        new RegExp(`\\b(${property})\\b`),
        "attribute.name",
      ]),
      ...methods.map((method) => [new RegExp(`\\b(${method})\\b`), "keyword"]),
    ],
  };

  const allLangs = await monaco.languages.getLanguages();
  const { language: yamlLang } = await allLangs
    .find(({ id }) => id === "yaml")
    .loader();

  for (const category in customTokenizer) {
    const tokenDefs = customTokenizer[category];
    if (!yamlLang.tokenizer.hasOwnProperty(category)) {
      yamlLang.tokenizer[category] = [];
    }
    if (Array.isArray(tokenDefs)) {
      yamlLang.tokenizer[category].unshift.apply(
        yamlLang.tokenizer[category],
        tokenDefs,
      );
    }
  }

  const keywords = [
    "true",
    "True",
    "TRUE",
    "false",
    "False",
    "FALSE",
    "null",
    "Null",
    "~",
  ];
  const commonStrings = [
    "ports",
    "inputs",
    "outputs",
    "links",
    "exchanges",
    "source",
    "target",
    "allocated_functional_exchanges",
    "allocated_interactions",
    "physical_ports",
    "components",
    "involved_activities",
    "involved_functions",
    "BLACKBOX",
    "WHITEBOX",
    "GRAYBOX",
    "LEFT",
    "RIGHT",
    "TREE",
    "NONE",
    "SMART",
    "ALL",
    "ABOVE",
    "BELOW",
    "UNION",
    "HEIGHT",
    "WIDTH",
    "INDIVIDUAL",
    "UNDEFINED",
    "POLYLINE",
    "ORTHOGONAL",
    "SPLINES",
    "UP",
    "DOWN",
    "PORTS",
    "NODE_LABELS",
    "PORT_LABELS",
    "MINIMUM_SIZE",
    "ALWAYS_UP",
    "ALWAYS_DOWN",
    "DIRECTION_UP",
    "DIRECTION_DOWN",
    "SMART_UP",
    "SMART_DOWN",
    "ROOT",
    "ALL",
  ];

  monaco.languages.registerCompletionItemProvider("yaml", {
    triggerCharacters: [],
    provideCompletionItems: () => {
      return {
        suggestions: [
          ...keywords.map((keyword) => ({
            label: keyword,
            kind: monaco.languages.CompletionItemKind.Keyword,
            insertText: keyword,
          })),
          ...diag_types.map((diag_type) => ({
            label: diag_type,
            kind: monaco.languages.CompletionItemKind.Interface,
            insertText: `${diag_type}:\n\t`,
          })),
          ...properties.map((property) => ({
            label: property,
            kind: monaco.languages.CompletionItemKind.Property,
            insertText: `${property}: `,
          })),
          ...methods.map((method) => ({
            label: method,
            kind: monaco.languages.CompletionItemKind.Method,
            insertText: `${method}:\n\t`,
          })),
          ...commonStrings.map((commonString) => ({
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
  editorRef.value?.trigger("keyboard", command, null);
}

function triggerSourceCommand(command) {
  editorRef.value?.trigger("source", command);
}

async function run() {
  if (!settings.targetUUID) {
    return;
  }
  loading.value = true;
  await settings.renderDiagram();
  loading.value = false;
}
</script>

<template>
  <nav class="flex items-center gap-2 px-4 py-2">
    <div class="flex flex-1 items-center gap-2">
      <h1 class="text-2xl font-semibold">CCDD</h1>
      <FileMenu />
      <EditMenu
        :trigger-keyboard-command="triggerKeyboardCommand"
        :trigger-source-command="triggerSourceCommand"
      />
      <HelpMenu />
    </div>
    <div class="flex items-center gap-2">
      <Button
        v-tooltip="{
          value: settings.superKey + ' + Enter',
          showDelay: 1000,
          hideDelay: 300,
        }"
        label="Run"
        @click="run"
        :disabled="loading || !settings.targetUUID"
        icon="pi pi-play"
      />
      <ProgressSpinner
        :style="
          'width: 1.5rem; height: 1.5rem; position: absolute; margin: 0 -2.5rem;' +
          (loading ? 'visibility: visible;' : 'visibility: hidden;')
        "
        strokeWidth="8"
        fill="transparent"
      />
    </div>
    <div class="flex flex-1 items-center justify-end">
      <Button
        icon="pi pi-cog"
        aria-label="Open settings"
        @click="settingsModal.visible = true"
        severity="secondary"
        text
      />
      <ThemeButton />
    </div>
  </nav>
  <main class="min-h-0 flex-1 px-4">
    <Splitter class="h-full">
      <SplitterPanel class="flex h-full flex-col">
        <Splitter layout="vertical" class="h-full">
          <SplitterPanel class="flex flex-col">
            <vue-monaco-editor
              v-model:value="settings.yamlCode"
              :theme="settings.dark ? 'vs-dark' : 'vs'"
              :options="settings.editorOptions"
              language="yaml"
              @mount="handleMount"
              @beforeMount="handleBeforeMount"
            />
          </SplitterPanel>
          <SplitterPanel
            class="flex flex-col"
            v-if="settings.previewConfigs.showBrowser"
          >
            <TargetBrowser />
          </SplitterPanel>
        </Splitter>
      </SplitterPanel>
      <SplitterPanel class="flex flex-col">
        <SVGDisplay />
      </SplitterPanel>
    </Splitter>
  </main>
  <footer class="flex items-center justify-end px-4 py-2">
    <p>© 2025 DB InfraGO AG</p>
  </footer>
  <Settings ref="settingsModal" />
</template>
