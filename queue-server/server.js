const express = require('express');
const { createClient } = require('redis');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config({ path: '../.env' }); 


const app = express();
const PORT = process.env.PORT || 3000;


// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Create a Redis client using the environment variable
const client = createClient({
    url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}` // Use the REDIS_URL from .env
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
