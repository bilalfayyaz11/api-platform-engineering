const jwt = require('jsonwebtoken');

/**
 * Verify a JWT from the Authorization header.
 *
 * Expected format:
 * Authorization: Bearer <token>
 */
const verifyToken = (req, res, next) => {
    const authorizationHeader = req.headers.authorization;

    if (!authorizationHeader) {
        return res.status(403).json({
            message: 'Authentication token is required'
        });
    }

    const [scheme, token] = authorizationHeader.split(' ');

    if (scheme !== 'Bearer' || !token) {
        return res.status(403).json({
            message: 'Authorization header must use Bearer token format'
        });
    }

    try {
        const decoded = jwt.verify(
            token,
            process.env.JWT_SECRET,
            {
                issuer: 'jwt-auth-api',
                audience: 'jwt-auth-client'
            }
        );

        req.user = decoded;
        return next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({
                message: 'Authentication token has expired'
            });
        }

        if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({
                message: 'Invalid authentication token'
            });
        }

        console.error('Token verification error:', error.message);

        return res.status(401).json({
            message: 'Token verification failed'
        });
    }
};

module.exports = verifyToken;
