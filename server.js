const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const app = express();

// Body parsers
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Configure Multer for media uploads
const mediaStorage = multer.diskStorage({
    destination: (req, file, cb) => {
        const dest = path.join(__dirname, 'images', 'uploads');
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest, { recursive: true });
        }
        cb(null, dest);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname);
        cb(null, file.fieldname + '-' + uniqueSuffix + ext);
    }
});
const upload = multer({ storage: mediaStorage });
const PORT = 3000;

// Middleware to log all requests
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// Serve static files from multiple directories
app.use(express.static(__dirname));
app.use('/css', express.static(path.join(__dirname, 'css')));
app.use('/js', express.static(path.join(__dirname, 'js')));
app.use('/images', express.static(path.join(__dirname, 'images')));
app.use('/public', express.static(path.join(__dirname, 'public')));

// Route for the homepage
app.get('/', (req, res) => {
    const indexPath = path.join(__dirname, 'index.html');
    if (fs.existsSync(indexPath)) {
        res.sendFile(indexPath);
    } else {
        res.status(404).send('Index file not found');
    }
});

// -------- ADMIN PAGE & API ENDPOINTS --------

// Serve admin dashboard
app.get('/admin', (req, res) => {
    const adminPath = path.join(__dirname, 'admin.html');
    if (fs.existsSync(adminPath)) {
        res.sendFile(adminPath);
    } else {
        res.status(404).send('Admin page not found');
    }
});

// Upload media (images/videos)
app.post('/api/upload', upload.single('media'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ success: false, message: 'No file uploaded' });
    }
    const fileUrl = `/images/uploads/${req.file.filename}`;
    return res.json({ success: true, url: fileUrl });
});

// Save news article
app.post('/api/news', (req, res) => {
    const { title, content, date } = req.body;
    if (!title || !content) {
        return res.status(400).json({ success: false, message: 'Title and content required' });
    }
    const newsItem = { title, content, date: date || new Date().toISOString() };
    const dataPath = path.join(__dirname, 'data');
    if (!fs.existsSync(dataPath)) {
        fs.mkdirSync(dataPath);
    }
    const newsFile = path.join(dataPath, 'news.json');
    let news = [];
    if (fs.existsSync(newsFile)) {
        news = JSON.parse(fs.readFileSync(newsFile));
    }
    news.push(newsItem);
    fs.writeFileSync(newsFile, JSON.stringify(news, null, 2));
    return res.json({ success: true });
});

// Save writeup
app.post('/api/writeups', (req, res) => {
    const { title, content, date } = req.body;
    if (!title || !content) {
        return res.status(400).json({ success: false, message: 'Title and content required' });
    }
    const item = { title, content, date: date || new Date().toISOString() };
    const dataPath = path.join(__dirname, 'data');
    if (!fs.existsSync(dataPath)) {
        fs.mkdirSync(dataPath);
    }
    const file = path.join(dataPath, 'writeups.json');
    let items = [];
    if (fs.existsSync(file)) {
        items = JSON.parse(fs.readFileSync(file));
    }
    items.push(item);
    fs.writeFileSync(file, JSON.stringify(items, null, 2));
    return res.json({ success: true });
});

// ---------- PAGE MANAGEMENT ENDPOINTS ----------

// Utility to find all .html files except admin.html
function getAllPages() {
    const walk = (dir, arr = []) => {
        fs.readdirSync(dir).forEach(file => {
            const full = path.join(dir, file);
            const stat = fs.statSync(full);
            if (stat.isDirectory()) {
                // skip node_modules and data etc.
                if (!['node_modules', '.git', 'images', 'data'].includes(file)) {
                    walk(full, arr);
                }
            } else if (file.endsWith('.html') && file !== 'admin.html') {
                arr.push(path.relative(__dirname, full).replace(/\\/g, '/'));
            }
        });
        return arr;
    };
    return walk(__dirname);
}

// GET /api/pages -> list of html files
app.get('/api/pages', (req, res) => {
    try {
        const pages = getAllPages();
        res.json({ success: true, pages });
    } catch (e) {
        console.error(e);
        res.status(500).json({ success: false, message: 'Failed to list pages' });
    }
});

// GET /api/page?path=...
app.get('/api/page', (req, res) => {
    const relPath = req.query.path;
    if (!relPath) return res.status(400).json({ success: false, message: 'Path required' });
    const target = path.join(__dirname, relPath);
    if (!target.startsWith(__dirname)) return res.status(400).json({ success: false });
    if (!fs.existsSync(target)) return res.status(404).json({ success: false, message: 'File not found' });
    const content = fs.readFileSync(target, 'utf8');
    res.json({ success: true, content });
});

// POST /api/page { path, content }
app.post('/api/page', (req, res) => {
    const { path: relPath, content } = req.body;
    if (!relPath || typeof content !== 'string') return res.status(400).json({ success: false });
    const target = path.join(__dirname, relPath);
    if (!target.startsWith(__dirname) || !relPath.endsWith('.html') || relPath === 'admin.html') {
        return res.status(400).json({ success: false });
    }
    try {
        fs.writeFileSync(target, content, 'utf8');
        res.json({ success: true });
    } catch (e) {
        console.error(e);
        res.status(500).json({ success: false, message: 'Failed to save' });
    }
});

// Handle 404
app.use((req, res) => {
    res.status(404).send('404 - Not Found');});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

// Start the server
console.log('Attempting to start server...');
console.log('Current directory:', __dirname);
console.log('Index.html exists:', fs.existsSync(path.join(__dirname, 'index.html')));

const server = app.listen(PORT, () => {
    const host = 'localhost';
    console.log(`Server running at http://${host}:${PORT}`);
    console.log('Serving files from:', __dirname);
    
    // Log network interfaces for remote access
    const os = require('os');
    const ifaces = os.networkInterfaces();
    
    console.log('Network interfaces:');
    Object.keys(ifaces).forEach(ifname => {
        ifaces[ifname].forEach(iface => {
            if ('IPv4' === iface.family && !iface.internal) {
                console.log(`- http://${iface.address}:${PORT}`);
            }
        });
    });
});

// Handle server events
server.on('listening', () => {
    console.log('Server is now listening on port', PORT);
});

server.on('error', (error) => {
    console.error('Server error:', error);
    if (error.code === 'EADDRINUSE') {
        console.error(`Port ${PORT} is already in use. Please stop any other servers using this port.`);
    } else {
        console.error('Server error:', error);
    }
    process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});
