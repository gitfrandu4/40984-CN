#!/bin/bash

# Update the system
sudo yum update -y

# Install Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js
nvm install 16

# Create a new directory for the application
mkdir ~/myapp
cd ~/myapp

# Initialize a new Node.js project and install Express
npm init -y
npm install express

# Create a simple Express server
cat << EOF > app.js
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('<h1>Express Server on AWS EC2</h1><p>Hostname: ' + require('os').hostname() + '</p>');
});

app.listen(port, () => {
  console.log(\`Server running at http://localhost:\${port}\`);
});
EOF

# Install PM2 globally
npm install pm2 -g

# Start the Express server with PM2
pm2 start app.js

# Configure PM2 to start on system boot
pm2 startup
pm2 save

# Install and configure nginx as a reverse proxy
sudo yum install nginx

# Configure nginx
sudo tee /etc/nginx/conf.d/myapp.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Remove the default nginx configuration
sudo rm /etc/nginx/conf.d/default.conf

# Start and enable nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Print the public IP address
echo "Setup complete. Your server's public IP address is:"
curl -s http://169.254.169.254/latest/meta-data/public-ipv4

echo "You can access your Express server by visiting this IP address in your web browser."
