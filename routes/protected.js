const express = require('express');
const verifyToken = require('../middleware/authMiddleware');

const router = express.Router();

/**
 * Public endpoint.
 * No authentication is required.
 */
router.get('/public', (req, res) => {
    return res.status(200).json({
        message: 'This is a public endpoint'
    });
});

/**
 * Protected dashboard endpoint.
 */
router.get('/dashboard', verifyToken, (req, res) => {
    return res.status(200).json({
        message: `Welcome ${req.user.userId}`,
        data: {
            authenticated: true,
            userId: req.user.userId,
            issuedAt: req.user.iat,
            expiresAt: req.user.exp
        }
    });
});

/**
 * Protected user profile endpoint.
 */
router.get('/profile', verifyToken, (req, res) => {
    return res.status(200).json({
        profile: {
            username: req.user.userId,
            tokenIssuer: req.user.iss,
            tokenAudience: req.user.aud
        }
    });
});

module.exports = router;
