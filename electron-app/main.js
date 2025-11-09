const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        fullscreen: false,
        backgroundColor: '#000000',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    mainWindow.loadFile('mid_web_electron.html');
    
    // Open DevTools in development (comment out for production)
    // mainWindow.webContents.openDevTools();

    // Enter fullscreen after load
    mainWindow.webContents.on('did-finish-load', () => {
        mainWindow.setFullScreen(true);
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Get the base path for resources (works both in dev and production)
function getResourcePath(filename) {
    if (app.isPackaged) {
        // In production, resources are in the app.asar or extraResources
        return path.join(process.resourcesPath, filename);
    } else {
        // In development, go up one level to access the parent directory
        return path.join(__dirname, '..', filename);
    }
}

// Get file URL for images (works both in dev and production)
function getImageFileUrl(imagePath) {
    const fullPath = getResourcePath(imagePath);
    // Use Node's pathToFileURL for proper file:// URL conversion (handles all platforms)
    return pathToFileURL(fullPath).href;
}

// IPC Handlers for file operations
ipcMain.handle('read-file', async (event, filePath) => {
    try {
        const fullPath = getResourcePath(filePath);
        const content = fs.readFileSync(fullPath, 'utf-8');
        return { success: true, content };
    } catch (error) {
        console.error('Error reading file:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('save-csv', async (event, csvData, filename) => {
    try {
        // Create data directory in the app's directory
        const dataDir = getResourcePath('data');
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }

        const filePath = path.join(dataDir, filename);
        fs.writeFileSync(filePath, csvData, 'utf-8');
        
        return { success: true, path: filePath };
    } catch (error) {
        console.error('Error saving CSV:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('show-save-dialog', async (event, defaultFilename) => {
    try {
        const result = await dialog.showSaveDialog(mainWindow, {
            title: 'Speichern Sie die Experimentdaten',
            defaultPath: path.join(app.getPath('documents'), defaultFilename),
            filters: [
                { name: 'CSV Files', extensions: ['csv'] },
                { name: 'All Files', extensions: ['*'] }
            ]
        });

        if (!result.canceled && result.filePath) {
            return { success: true, filePath: result.filePath };
        } else {
            return { success: false, canceled: true };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
});

ipcMain.handle('write-file', async (event, filePath, content) => {
    try {
        const fullPath = path.join(app.getPath('documents'), filePath);
        fs.writeFileSync(fullPath, content, 'utf-8');
        return { success: true, path: fullPath };
    } catch (error) {
        return { success: false, error: error.message };
    }
});

ipcMain.handle('quit-app', () => {
    app.quit();
});

// IPC handler to get image file URL
ipcMain.handle('get-image-url', async (event, imagePath) => {
    try {
        const fileUrl = getImageFileUrl(imagePath);
        // Verify file exists
        const fullPath = getResourcePath(imagePath);
        if (fs.existsSync(fullPath)) {
            return { success: true, url: fileUrl };
        } else {
            console.error('Image not found:', fullPath);
            return { success: false, error: 'Image not found: ' + imagePath };
        }
    } catch (error) {
        console.error('Error getting image URL:', error);
        return { success: false, error: error.message };
    }
});

