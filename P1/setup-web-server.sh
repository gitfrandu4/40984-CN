#!/bin/bash

# Update the system and install Apache
sudo yum update -y
sudo yum install -y httpd

# Enable and start Apache
sudo systemctl enable httpd
sudo systemctl start httpd

# Create a more elaborate HTML content with ASCII art
cat <<EOF | sudo tee /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Francisco Javier López-Dufour Morales - Crossfit Enthusiast</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #2c3e50;
        }
        pre {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>Computación en la Nube - P1</h1>
    <h2>Francisco Javier López-Dufour Morales</h1>
    <h3>Crossfit</h3>
    <pre>
     __ __   ___   _       ____      ___ ___  __ __  ____   ___     ___  
    |  |  | /   \ | |     /    |    |   |   ||  |  ||    \ |   \   /   \ 
    |  |  ||     || |    |  o  |    | _   _ ||  |  ||  _  ||    \ |     |
    |  _  ||  O  || |___ |     |    |  \_/  ||  |  ||  |  ||  D  ||  O  |
    |  |  ||     ||     ||  _  |    |   |   ||  :  ||  |  ||     ||     |
    |  |  ||     ||     ||  |  |    |   |   ||     ||  |  ||     ||     |
    |__|__| \___/ |_____||__|__|    |___|___| \__,_||__|__||_____| \___/     
</pre>
</body>
</html>
EOF

echo "Web server setup complete! Your personalized page is now live."
