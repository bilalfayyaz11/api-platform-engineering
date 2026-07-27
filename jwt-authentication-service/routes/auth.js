const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const router = express.Router();

// In-memory user storage.
// Data is lost whenever the server restarts.
const users = [];

/**
 * Register a new user.
 */
router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (
            typeof username !== 'string' ||
            typeof password !== 'string' ||
            username.trim().length < 3 ||
            password.length < 8
        ) {
            return res.status(400).json({
                message: 'Username must be at least 3 characters and password at least 8 characters'
            });
        }

        const normalizedUsername = username.trim().toLowerCase();

        const existingUser = users.find(
            (user) => user.username === normalizedUsername
        );

        if (existingUser) {
            return res.status(409).json({
                message: 'Username already exists'
            });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        users.push({
            username: normalizedUsername,
            password: hashedPassword
        });

        return res.status(201).json({
            message: 'User registered successfully',
            user: {
                username: normalizedUsername
            }
        });
    } catch (error) {
        console.error('Registration error:', error.message);

        return res.status(500).json({
            message: 'Server error'
        });
    }
});

/**
 * Authenticate a user and issue a JWT.
 */
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (
            typeof username !== 'string' ||
            typeof password !== 'string' ||
            !username.trim() ||
            !password
        ) {
            return res.status(400).json({
                message: 'Username and password are required'
            });
        }

        const normalizedUsername = username.trim().toLowerCase();

        const user = users.find(
            (storedUser) => storedUser.username === normalizedUsername
        );

        if (!user) {
            return res.status(401).json({
                message: 'Invalid username or password'
            });
        }

        const passwordMatches = await bcrypt.compare(
            password,
            user.password
        );

        if (!passwordMatches) {
            return res.status(401).json({
                message: 'Invalid username or password'
            });
        }

        const token = jwt.sign(
            {
                userId: user.username
            },
            process.env.JWT_SECRET,
            {
                expiresIn: process.env.JWT_EXPIRES_IN || '1h',
                issuer: 'jwt-auth-api',
                audience: 'jwt-auth-client'
            }
        );

        return res.status(200).json({
            message: 'Login successful',
            token,
            tokenType: 'Bearer',
            expiresIn: process.env.JWT_EXPIRES_IN || '1h'
        });
    } catch (error) {
        console.error('Login error:', error.message);

        return res.status(500).json({
            message: 'Server error'
        });
    }
});

module.exports = router;
