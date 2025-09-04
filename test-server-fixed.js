const http = require('http');

// Simple HTTP server
const server = http.createServer((req, res) => {
    console.log(`Request from: ${req.socket.remoteAddress}`);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Server is working!\n');
});

// Try different ports
const PORT = 3000; // Try different ports if needed (3000, 3001, 3002, etc.)

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running at http://localhost:${PORT}`);
}).on('error', (err) => {
    console.error('Server error:', err);
});
