const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const FILE = path.join(__dirname, 'public', 'index.html');
const html = fs.readFileSync(FILE);

http.createServer(function (req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(html);
}).listen(PORT, function () {
  console.log('Blueberry wheel listening on ' + PORT);
});
