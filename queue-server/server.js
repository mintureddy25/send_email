const express = require('express');
const { createClient } = require('redis');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config({ path: '../.env' }); 


const app = express();
const PORT = process.env.PORT || 3000;


// Middleware
const corsOptions = {
  origin: process.env.CLIENT_URL, // Allow requests only from the client URL stored in .env
  methods: ['POST'], // You can specify allowed HTTP methods here
  allowedHeaders: ['Content-Type', 'Authorization'], // Specify allowed headers if needed
};
app.use(cors(corsOptions));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Create a Redis client using the environment variable
const client = createClient({
    username: process.env.REDIS_USERNAME,
    password: process.env.REDIS_PASSWORD,
    socket: {
        host: process.env.REDIS_HOST,
        port: process.env.REDIS_PORT
    }
});

// Connect to Redis
client.connect().catch(console.error);

// Function to put a job into the Redis queue
async function putJob(data, queueName) {
    const jobData = JSON.stringify(data);
    await client.lPush(queueName, jobData);
    console.log(`Job added to queue: ${jobData}`);
}

// API endpoint to add a job to the queue
app.post('/queue/jobs', async (req, res) => {
    const { email, subject } = req.body;
    console.log(email, subject, "queue testing");

    try {
        await putJob({ email, subject }, 'email_queue');
        res.status(201).json({ message: 'Job added to queue' });
    } catch (error) {
        console.error('Caught error:', error);
        res.status(500).json({ error: 'Failed to add job to queue' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Handle graceful shutdown
process.on('SIGINT', async () => {
    await client.quit();
    process.exit();
});
