const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Get all network interfaces
const networkInterfaces = os.networkInterfaces();
console.log('Network Interfaces:', JSON.stringify(networkInterfaces, null, 2));

const server = http.createServer((req, res) => {
    const clientIP = req.socket.remoteAddress;
    console.log(`[${new Date().toISOString()}] Request from ${clientIP} for: ${req.url}`);
    
    if (req.url === '/') {
        const filePath = path.join(__dirname, 'index.html');
        console.log(`Attempting to serve file: ${filePath}`);
        
        fs.access(filePath, fs.constants.F_OK, (err) => {
            if (err) {
                console.error('File does not exist:', filePath);
                res.writeHead(404, { 'Content-Type': 'text/plain' });
                return res.end('File not found');
            }
            
            fs.readFile(filePath, (err, content) => {
                if (err) {
                    console.error('Error reading file:', err);
                    res.writeHead(500, { 'Content-Type': 'text/plain' });
                    return res.end('Server Error');
                }
                console.log('Serving file successfully');
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(content, 'utf-8');
            });
        });
    } else {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Test server is running!\n' + 
                `Server time: ${new Date().toISOString()}\n` +
                `Node.js version: ${process.version}\n` +
                `Platform: ${process.platform} ${process.arch}\n`);
    }
});

const PORT = 3003;
const HOST = '0.0.0.0'; // Listen on all network interfaces

// Get server URLs
const getServerUrls = () => {
    const urls = [`http://localhost:${PORT}`];
    
    // Add all non-internal IPv4 addresses
    Object.values(networkInterfaces).forEach(iface => {
        iface.forEach(details => {
            if (details.family === 'IPv4' && !details.internal) {
                urls.push(`http://${details.address}:${PORT}`);
            }
        });
    });
    
    return urls;
};

server.listen(PORT, HOST, () => {
    console.log('\n=== Test Server Started ===');
    console.log(`Node.js version: ${process.version}`);
    console.log(`Platform: ${process.platform} ${process.arch}`);
    console.log(`Server time: ${new Date().toISOString()}`);
    console.log(`Server PID: ${process.pid}`);
    console.log('\nAvailable at:');
    getServerUrls().forEach(url => console.log(`  - ${url}`));
    console.log('\nCurrent directory:', __dirname);
    console.log('===========================\n');
});

// Handle server errors
server.on('error', (error) => {
    console.error('\n=== SERVER ERROR ===');
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);
    console.error('========================\n');
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('\nShutting down server...');
    server.close(() => {
        console.log('Server stopped');
        process.exit(0);
    });
});
