// Save as server.js
const noblox = require('noblox.js');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// ==================== CONFIGURATION ====================
const COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS...[YOUR_COOKIE]";
const GROUP_ID = 160052583;
const API_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y";
const PORT = 3000;
// =======================================================

async function startBot() {
    // Log into Roblox backend natively via JavaScript
    await noblox.setCookie(COOKIE);
    console.log(`✨ Node.js Bot Logged in as: ${(await noblox.getAuthenticatedUser()).UserName}`);

    // Secure API Endpoint for Python GUI / Web dashboards
    app.post('/api/v1/rank', async (req, res) => {
        const token = req.headers['x-api-key'];
        if (token !== API_KEY) {
            return res.status(403).json({ error: "Unauthorized handshake signature." });
        }

        const { user_id, role_id } = req.body;
        try {
            // Change rank natively inside Roblox systems
            await noblox.setRank(GROUP_ID, parseInt(user_id), parseInt(role_id));
            console.log(`✅ [JS ENGINE] Ranked User ${user_id} to Role ${role_id}`);
            res.json({ success: true, message: `Rank changed successfully.` });
        } catch (err) {
            console.error(`❌ [JS ENGINE] Error: ${err.message}`);
            res.status(500).json({ error: err.message });
        }
    });

    app.listen(PORT, () => console.log(`🚀 Node.js Group Link Active on http://localhost:${PORT}`));
}

startBot().catch(err => console.error("Critical JS Boot Failure:", err));
