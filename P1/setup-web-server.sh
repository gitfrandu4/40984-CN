#!/bin/bash
yum update -y
yum -y install httpd
systemctl enable httpd
systemctl start httpd
echo '<html><h1>My Name: Your Name</h1><p>My Favorite Hobby: Your Hobby</p></html>' > /var/www/html/index.html
