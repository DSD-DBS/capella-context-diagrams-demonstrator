<script setup>
/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import Menu from "@/components/Menu.vue";
import { useSettingsStore } from "@/stores/settings";
import { onMounted } from "vue";

const settings = useSettingsStore();
const EXAMPLES_PATH = "/examples";

const SAMPLES = [
  { label: "Context", command: () => loadSample("context.yml") },
  { label: "Component Exchanges", command: () => loadSample("exchanges.yml") },
  { label: "Physical Ports", command: () => loadSample("ports.yml") },
  { label: "Classes", command: () => (settings.yamlCode = "tree_view") },
  {
    label: "Realization View",
    command: () => (settings.yamlCode = "realization_view"),
  },
  { label: "Data Flow", command: () => loadSample("dataflow.yml") },
  { label: "Cable Tree", command: () => (settings.yamlCode = "cable_tree") },
];

const items = [
  {
    label: "New",
    shortcut: settings.superKey + " + N",
  },
  {
    label: "Open",
    shortcut: settings.superKey + " + O",
    command: () => openFile(),
  },
  {
    label: "Save",
    shortcut: settings.superKey + " + S",
    command: () => settings.saveCode(),
  },
  {
    label: "Load example",
    items: SAMPLES,
  },
];

function loadSample(selectedFile) {
  settings.loadCode(`${EXAMPLES_PATH}/${selectedFile}`);
}

function newFile() {
  settings.yamlCode = "";
}

function openFile() {
  document.getElementById("file-upload").click();
}

function loadFile(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    settings.yamlCode = e.target.result;
  };
  reader.readAsText(file);
}

onMounted(() => {
  window.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key === "o") {
      e.preventDefault();
      openFile();
    } else if (e.ctrlKey && e.key === "s") {
      e.preventDefault();
      settings.saveCode();
    }
  });
});
</script>

<template>
  <Menu label="File" :items="items" overlay_id="overlay_file" />
  <input
    type="file"
    id="file-upload"
    style="display: none"
    @change="loadFile($event)"
  />
</template>
