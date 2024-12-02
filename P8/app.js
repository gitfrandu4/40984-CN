// app.js
const express = require('express');
const { Pool } = require('pg');
const AWS = require('aws-sdk');
const multer = require('multer');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(express.json());
app.use(express.static('public'));

// Database configuration
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT || 5432,
  ssl: {
    rejectUnauthorized: false
  }
});

// S3 configuration
const s3 = new AWS.S3();
const upload = multer({ dest: 'uploads/' });

// Serve the main page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Create a new product
app.post('/products', async (req, res) => {
  try {
    const { name, price, description } = req.body;
    
    // Generate S3 URL for the product image
    const s3Url = `https://${process.env.S3_BUCKET}.s3.amazonaws.com/products/${name}`;
    
    const result = await pool.query(
      'INSERT INTO products (name, price, description, image_url) VALUES ($1, $2, $3, $4) RETURNING *',
      [name, price, description, s3Url]
    );
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error creating product:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get all products
app.get('/products', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM products ORDER BY created_at DESC');
    
    // Generate presigned URLs for each product
    const productsWithUrls = await Promise.all(result.rows.map(async (product) => {
      const params = {
        Bucket: process.env.S3_BUCKET,
        Key: `products/${product.name}`,
        Expires: 3600 // URL valid for 1 hour
      };
      
      const signedUrl = await s3.getSignedUrlPromise('getObject', params);
      return {
        ...product,
        image_url: signedUrl
      };
    }));
    
    res.json(productsWithUrls);
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get product by ID
app.get('/products/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM products WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    const product = result.rows[0];
    
    // Generate presigned URL for the product image
    const params = {
      Bucket: process.env.S3_BUCKET,
      Key: `products/${product.name}`,
      Expires: 3600 // URL valid for 1 hour
    };
    
    const signedUrl = await s3.getSignedUrlPromise('getObject', params);
    product.image_url = signedUrl;
    
    res.json(product);
  } catch (error) {
    console.error('Error fetching product:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Upload product image to S3
app.post('/products/:name/image', upload.single('image'), async (req, res) => {
  try {
    const { name } = req.params;
    const file = req.file;

    const uploadParams = {
      Bucket: process.env.S3_BUCKET,
      Key: `products/${name}`,
      Body: require('fs').createReadStream(file.path),
      ContentType: file.mimetype
    };

    const result = await s3.upload(uploadParams).promise();
    require('fs').unlinkSync(file.path);
    
    res.json({ imageUrl: result.Location });
  } catch (error) {
    console.error('Error uploading image:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Database initialization
const initDatabase = async () => {
  try {
    console.log('Attempting database connection...');
    console.log('Connection params:', {
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      database: process.env.DB_NAME,
      port: process.env.DB_PORT || 5432
    });

    await pool.query(`
      CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        description TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
    console.error('Error details:', {
      code: error.code,
      message: error.message,
      detail: error.detail
    });
    process.exit(1);
  }
};

const PORT = process.env.PORT || 3000;
app.listen(PORT, async () => {
  await initDatabase();
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;