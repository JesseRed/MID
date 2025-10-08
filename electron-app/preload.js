const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    readFile: (filePath) => ipcRenderer.invoke('read-file', filePath),
    saveCSV: (csvData, filename) => ipcRenderer.invoke('save-csv', csvData, filename),
    showSaveDialog: (defaultFilename) => ipcRenderer.invoke('show-save-dialog', defaultFilename),
    writeFile: (filePath, content) => ipcRenderer.invoke('write-file', filePath, content),
    quitApp: () => ipcRenderer.invoke('quit-app'),
    isElectron: true
});

