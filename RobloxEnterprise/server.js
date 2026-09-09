// Add this route block cleanly inside your active server.js script file
app.get('/api/v1/group-roles', authenticateToken, async (req, res) => {
    try {
        // Query the Roblox API directly to fetch full role group arrays instantly
        const groupRoles = await noblox.getRoles(GROUP_ID);
        res.json(groupRoles);
    } catch (err) {
        res.status(500).json({ error: "Roblox server connection timeout: " + err.message });
    }
});
