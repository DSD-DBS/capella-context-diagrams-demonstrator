/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

const BACKEND_URL =
    "http://" +
    import.meta.env.VITE_BACKEND_HOST +
    ":" +
    import.meta.env.VITE_BACKEND_PORT +
    "/api";

export const useSettingsStore = defineStore("settings", () => {
    const dark = ref(false);
    const targetUUID = ref("");
    const editorOptions = ref({
        automaticLayout: true,
        formatOnType: true,
        formatOnPaste: true,
        folding: true,
        fontSize: 14,
        tabSize: 2,
        minimap: {
            autohide: true,
        },
        quickSuggestions: {
            other: true,
            comments: true,
            strings: true,
        },
    });
    const previewConfigs = ref({
        showBrowser: true,
        showTitle: true,
    });
    const yamlCode = ref("");
    const svgName = ref("error");
    const svgContent = ref(
        '<svg height="100%" width="100%" id="pan-zoom"><text x="10" y="40" font-size="24" fill="red">No target selected</text></svg>'
    );
    const tableContent = ref("<h1>No target selected</h1>");
    const tableBreadcrumbs = ref([]);
    const modelElements = ref([]);
    const superKey = isApple() ? "⌘" : "Ctrl";

    async function addBreadcrum(uuid) {
        const name = await get_attributes(true, uuid);
        if (name) {
            tableBreadcrumbs.value.push({
                label: name,
                command: () => {
                    removeAllFollowingBreadcrumbs(
                        tableBreadcrumbs.value.findIndex(
                            (breadcrumb) => breadcrumb.label === name
                        ),
                        uuid
                    );
                },
            });
        }
    }

    async function removeAllFollowingBreadcrumbs(index, uuid) {
        tableBreadcrumbs.value = tableBreadcrumbs.value.slice(0, index + 1);
        await get_attributes(true, uuid);
    }

    function toggleDark() {
        dark.value = !dark.value;
    }

    async function getAllElements() {
        try {
            console.log(BACKEND_URL);
            const response = await axios.get(BACKEND_URL + "/elements");
            modelElements.value = response.data.elements;
        } catch (error) {
            console.error("Error getting elements:", error);
        }
    }

    async function setTarget(uuid) {
        try {
            const response = await axios.post(BACKEND_URL + "/target", {
                uuid: uuid,
            });
            return response.data;
        } catch (error) {
            console.error("Error setting target:", error);
            return error.response.data;
        }
    }

    async function renderDiagram(retry = true) {
        try {
            const response = await axios.post(BACKEND_URL + "/render", {
                yaml: yamlCode.value,
            });
            svgName.value = response.data.svg.name;
            svgContent.value = response.data.svg.content;
        } catch (error) {
            if (!retry) {
                svgContent.value = error.response.data.svg.content;
                return;
            }
            console.error("Retry rendering diagram:", error);
            await setTarget(targetUUID.value);
            await renderDiagram(false);
        }
    }

    async function get_attributes(retry = true, uuid = targetUUID.value) {
        try {
            const response = await axios.get(BACKEND_URL + "/attributes", {
                params: {
                    uuid: uuid,
                },
            });
            tableContent.value = response.data.repr;
            return response.data.name;
        } catch (error) {
            if (!retry) {
                tableContent.value = error.response.data.message;
                return;
            }
            console.error("Error getting attributes:", error);
            await setTarget(targetUUID.value);
            return await get_attributes(false, uuid);
        }
    }

    async function saveSVG() {
        try {
            const options = {
                suggestedName: svgName.value + ".svg",
                types: [
                    {
                        description: "SVG",
                        accept: {
                            "image/svg+xml": [".svg"],
                        },
                    },
                ],
            };
            const handle = await window.showSaveFilePicker(options);
            const writable = await handle.createWritable();
            await writable.write(svgContent.value);
            await writable.close();
        } catch (error) {
            console.error("Error saving file:", error);
        }
    }

    async function saveCode() {
        try {
            const options = {
                suggestedName: svgName.value.split(" of")[0] + ".yaml",
                types: [
                    {
                        description: "YAML",
                        accept: {
                            "text/yaml": [".yaml"],
                        },
                    },
                ],
            };
            const handle = await window.showSaveFilePicker(options);
            const writable = await handle.createWritable();
            await writable.write(yamlCode.value);
            await writable.close();
        } catch (error) {
            console.error("Error saving file:", error);
        }
    }

    async function loadCode(path) {
        try {
            const file = await fetch(path);
            yamlCode.value = await file.text();
        } catch (error) {
            console.error("Error loading file:", error);
        }
    }

    function isApple() {
        const platform =
            window.navigator?.userAgentData?.platform ||
            window.navigator.platform;
        const macosPlatforms = ["Macintosh", "MacIntel", "MacPPC", "Mac68K"];
        const iosPlatforms = ["iPhone", "iPad", "iPod"];

        if (
            macosPlatforms.indexOf(platform) !== -1 ||
            iosPlatforms.indexOf(platform) !== -1
        ) {
            return true;
        } else {
            return false;
        }
    }

    return {
        dark,
        yamlCode,
        svgContent,
        tableContent,
        renderDiagram,
        get_attributes,
        toggleDark,
        targetUUID,
        editorOptions,
        setTarget,
        saveSVG,
        saveCode,
        loadCode,
        svgName,
        previewConfigs,
        tableBreadcrumbs,
        addBreadcrum,
        modelElements,
        getAllElements,
        superKey,
    };
});
