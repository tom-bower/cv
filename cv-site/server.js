require('dotenv').config();
const express = require('express');
const path = require('path');
const app = express();
const basicAuth = require('express-basic-auth');
const PORT = process.env.PORT || 3000;


app.use(basicAuth({
    users: {
      [process.env.BASIC_AUTH_USER]: process.env.BASIC_AUTH_PASSWORD  // Use env variables
    },
    challenge: true,  // This will prompt for Basic Auth if not authenticated
    unauthorizedResponse: 'Unauthorized'  // Custom message if authentication fails
  }));

// Serve static files (like CSS)
app.use(express.static(path.join(__dirname, 'public')));

// Route for homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
