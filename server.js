// Save as server.js
const noblox = require('noblox.js');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
app.use(bodyParser.json());
app.use(cors());

// ==================== CONFIGURATION ====================
const COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyJAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0WClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk";
const GROUP_ID = 160052583;
const API_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y";
const AUTH_FILE = "user_auth.json";
const PORT = 3000;
// =======================================================

function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

async function startBot() {
    await noblox.setCookie(COOKIE);
    console.log(`[JS ENGINE] Connected to Roblox API.`);

    // --- Web Authentication Endpoints ---
    app.get('/api/v1/auth-check', (req, res) => {
        res.json({ hasAccount: fs.existsSync(AUTH_FILE) });
    });

    app.post('/api/v1/signup', (req, res) => {
        const { email, password } = req.body;
        if (!email || !password || !email.includes('@')) {
            return res.status(400).json({ error: "Invalid registration layout fields." });
        }
        if (fs.existsSync(AUTH_FILE)) {
            return res.status(400).json({ error: "Account already registered." });
        }
        const payload = { registered_email: email, password_hash: hashPassword(password) };
        fs.writeFileSync(AUTH_FILE, JSON.stringify(payload, null, 4));
        res.json({ success: true });
    });

    app.post('/api/v1/login', (req, res) => {
        const { email, password } = req.body;
        if (!fs.existsSync(AUTH_FILE)) {
            return res.status(400).json({ error: "No account found." });
        }
        const stored = JSON.parse(fs.readFileSync(AUTH_FILE));
        if (email === stored.registered_email && hashPassword(password) === stored.password_hash) {
            res.json({ success: true });
        } else {
            res.status(403).json({ error: "Invalid credentials configuration." });
        }
    });

    // --- Core Automation Endpoint ---
    app.post('/api/v1/rank', async (req, res) => {
        const token = req.headers['x-api-key'];
        if (token !== API_KEY) return res.status(403).json({ error: "Unauthorized." });

        const { user_id, action, role_id } = req.body;
        try {
            let targetRole = action === "unassign" ? 12884901889 : parseInt(role_id);
            await noblox.setRank(GROUP_ID, parseInt(user_id), targetRole);
            res.json({ success: true });
        } catch (err) {
            res.status(500).json({ error: err.message });
        }
    });

    app.listen(PORT, () => console.log(`[JS CORE] Listening on port ${PORT}`));
}

startBot().catch(err => console.error(err));
