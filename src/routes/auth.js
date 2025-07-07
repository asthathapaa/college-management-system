const express = require('express');
const jwt = require('jsonwebtoken');
const router = express.Router();

// Hardcoded user for simplicity
const USER = {
  username: 'admin',
  password: 'password123'
};

router.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  if (username === USER.username && password === USER.password) {
    const token = jwt.sign(
      { username: USER.username },
      process.env.JWT_SECRET || 'your_jwt_secret',
      { expiresIn: '1h' }
    );
    res.json({ token });
  } else {
    res.status(401).json({ message: 'Invalid credentials' });
  }
});

module.exports = router;