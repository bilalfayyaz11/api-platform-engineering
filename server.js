require('dotenv').config();

const express = require('express');
const authRoutes = require('./routes/auth');
const protectedRoutes = require('./routes/protected');

const app = express();
const PORT = process.env.PORT || 3000;

if (!process.env.JWT_SECRET) {
    console.error('JWT_SECRET is missing from the environment.');
    process.exit(1);
}

// Parse JSON request bodies.
app.use(express.json({ limit: '10kb' }));

// Application routes.
app.use('/api/auth', authRoutes);
app.use('/api', protectedRoutes);

// Health endpoint.
app.get('/', (req, res) => {
    return res.status(200).json({
        message: 'JWT Authentication API is running'
    });
});

// Handle unknown routes.
app.use((req, res) => {
    return res.status(404).json({
        message: 'Endpoint not found'
    });
});

// Handle malformed JSON and unexpected application errors.
app.use((error, req, res, next) => {
    if (error instanceof SyntaxError && error.status === 400 && 'body' in error) {
        return res.status(400).json({
            message: 'Invalid JSON request body'
        });
    }

    console.error('Unhandled server error:', error.message);

    return res.status(500).json({
        message: 'Internal server error'
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
