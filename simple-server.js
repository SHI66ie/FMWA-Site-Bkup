const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3003;
// Define multiple public directories to serve files from
const PUBLIC_DIRS = [
    __dirname,  // Root directory
    path.join(__dirname, 'css'),
    path.join(__dirname, 'js'),
    path.join(__dirname, 'images'),
    path.join(__dirname, 'public')
];

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.woff2': 'application/font-woff2',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
};

const server = http.createServer((req, res) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    
    // Parse URL
    const parsedUrl = url.parse(req.url);
    console.log(`[${new Date().toISOString()}] Request for: ${req.url}`);
    let pathname;
    
    // Default to index.html if root
    if (parsedUrl.pathname === '/' || parsedUrl.pathname === '') {
        pathname = path.join(__dirname, 'index.html');
    } else {
        // Try to find the file in one of the public directories
        const potentialPaths = [
            path.join(__dirname, parsedUrl.pathname),  // Root
            path.join(__dirname, 'css', parsedUrl.pathname.replace(/^\/css\//, '')),
            path.join(__dirname, 'js', parsedUrl.pathname.replace(/^\/js\//, '')),
            path.join(__dirname, 'images', parsedUrl.pathname.replace(/^\/images\//, '')),
            path.join(__dirname, 'public', parsedUrl.pathname.replace(/^\/public\//, ''))
        ];
        
        // Find the first existing path
        pathname = potentialPaths.find(p => {
            try {
                const exists = fs.existsSync(p) && fs.statSync(p).isFile();
                if (exists) {
                    console.log(`Found file at: ${p}`);
                }
                return exists;
            } catch (e) {
                console.error(`Error checking path ${p}:`, e.message);
                return false;
            }
        }) || path.join(__dirname, parsedUrl.pathname);
        
        console.log(`Using path: ${pathname}`);
    }
    
    // Prevent directory traversal
    pathname = path.normalize(pathname).replace(/^(\/\\)+(\.+\/)+/, '');
    
    // Check if file exists
    fs.exists(pathname, (exist) => {
        if (!exist) {
            // File not found
            res.statusCode = 404;
            res.end(`File ${pathname} not found!`);
            return;
        }

        // If it's a directory, look for index.html
        if (fs.statSync(pathname).isDirectory()) {
            pathname += '/index.html';
        }

        // Read file from file system
        fs.readFile(pathname, (err, data) => {
            if (err) {
                res.statusCode = 500;
                res.end(`Error getting the file: ${err}.`);
            } else {
                // Based on the URL path, extract the file extension
                const ext = path.parse(pathname).ext;
                // If the file is found, set Content-type and send data
                res.setHeader('Content-type', MIME_TYPES[ext] || 'application/octet-stream');
                res.end(data);
            }
        });
    });
});

server.on('error', (e) => {
    console.error('Server error:', e);
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log('Serving files from:', path.resolve(__dirname));
    console.log('Press Ctrl+C to stop the server');
});
