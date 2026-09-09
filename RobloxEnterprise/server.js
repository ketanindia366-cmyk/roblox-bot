// Save as server.js
const noblox = require('noblox.js');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

const app = express();
app.use(bodyParser.json());
app.use(cors()); // Critical: Allows your separate HTML pages to talk to port 3000 safely

// ==================== CONFIGURATION ENVIRONMENT ====================
const COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyJAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0WClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk";
const GROUP_ID = 160052583;
const API_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y";
const JWT_SECRET = "CRITICAL_SESSION_SIGNATIVE_KEY_HASH_5921867!";
const AUTH_FILE = "user_auth.json";
const PORT = 3000;
// ===================================================================

// In-Memory Firewall Brute-Force Rate Limiting Tracker
const loginAttempts = {};

// Secure Password Verification Hash Function
function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// Token Verification Gatekeeper Middleware
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) return res.status(401).json({ error: "Session token missing." });

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) return res.status(403).json({ error: "Session tracking invalid or manipulated." });
        req.user = user;
        next();
    });
};

async function startBot() {
    // 1. Authenticate with Roblox API Natively via JS
    try {
        await noblox.setCookie(COOKIE);
        const currentBotUser = await noblox.getAuthenticatedUser();
        console.log(`\x1b[32m[JS CORE] Connected! Logged into Roblox Bot Account: ${currentBotUser.UserName}\x1b[0m`);
    } catch (cookieError) {
        console.error(`\x1b[31m[ROBLOX ERROR] Cookie verification completely failed. Check your security parameters.\x1b[0m`);
    }

    // --- ENDPOINT 1: Check if an Admin account exists ---
    app.get('/api/v1/auth-check', (req, res) => {
        res.json({ hasAccount: fs.existsSync(AUTH_FILE) });
    });

    // --- ENDPOINT 2: Secure Account Sign Up ---
    app.post('/api/v1/signup', (req, res) => {
        const { email, password } = req.body;
        if (!email || !password || !email.includes('@')) {
            return res.status(400).json({ error: "Invalid registration layout fields." });
        }
        if (fs.existsSync(AUTH_FILE)) {
            return res.status(400).json({ error: "An account has already been registered on this machine deployment core." });
        }
        
        // Hashing password securely
        const payload = { registered_email: email, password_hash: hashPassword(password) };
        fs.writeFileSync(AUTH_FILE, JSON.stringify(payload, null, 4));
        console.log(`[JS ENGINE] Registered fresh admin profile: ${email}`);
        res.json({ success: true });
    });

    // --- ENDPOINT 3: Secure JWT Portal Login ---
    app.post('/api/v1/login', (req, res) => {
        const { email, password } = req.body;
        const clientIp = req.ip;

        // Brute-force verification check step
        if (loginAttempts[clientIp] && loginAttempts[clientIp].count >= 5 && loginAttempts[clientIp].lockout > Date.now()) {
            return res.status(429).json({ error: "Temporary firewall defense activated. Try again in 15 mins." });
        }

        if (!fs.existsSync(AUTH_FILE)) {
            return res.status(400).json({ error: "No account profile data found." });
        }

        const storedData = JSON.parse(fs.readFileSync(AUTH_FILE));
        
        // Compare request string parameters with storage profile records safely
        if (email === storedData.registered_email && hashPassword(password) === storedData.password_hash) {
            // Reset brute force counter on clear auth verification
            loginAttempts[clientIp] = { count: 0, lockout: 0 };
            
            // Mint an official cryptographically secure session token
            const token = jwt.sign({ email: email, role: "administrator" }, JWT_SECRET, { expiresIn: '2h' });
            console.log(`[JS ENGINE] Session authenticated successfully for: ${email}`);
            res.json({ success: true, sessionToken: token });
        } else {
            // Log attempt infrastructure rules
            if (!loginAttempts[clientIp]) loginAttempts[clientIp] = { count: 0, lockout: 0 };
            loginAttempts[clientIp].count++;
            if (loginAttempts[clientIp].count >= 5) {
                loginAttempts[clientIp].lockout = Date.now() + 15 * 60 * 1000; // 15-Minute Timeout lockout
            }
            res.status(403).json({ error: "Identity verification failed. Invalid credentials." });
        }
    });

    // --- ENDPOINT 4: Get Group Roles Catalog Sheet (Used by dashboard.html) ---
    app.get('/api/v1/group-roles', authenticateToken, async (req, res) => {
        try {
            console.log(`[JS ENGINE] Fetching full catalog tier arrays for authorized user...`);
            const groupRoles = await noblox.getRoles(GROUP_ID);
            res.json(groupRoles);
        } catch (err) {
            res.status(500).json({ error: "Roblox server connection timeout: " + err.message });
        }
    });

    // --- ENDPOINT 5: Core Rank Modification Execution Gateway ---
    app.post('/api/v1/rank', async (req, res) => {
        const token = req.headers['x-api-key'];
        if (token !== API_KEY) return res.status(403).json({ error: "Access denied. Handshake signature failed." });

        const { user_id, action, role_id } = req.body;
        try {
            let targetRole = action === "unassign" ? 12884901889 : parseInt(role_id);
            await noblox.setRank(GROUP_ID, parseInt(user_id), targetRole);
            console.log(`\x1b[36m[SUCCESS]\x1b[0m Successfully adjusted User ${user_id} -> Rank ID ${targetRole}`);
            res.json({ success: true });
        } catch (err) {
            console.error(`\x1b[31m[RANK FAILED]\x1b[0m External modification rejected: ${err.message}`);
            res.status(500).json({ error: err.message });
        }
    });

    // Listen loop activation mapping parameters
    app.listen(PORT, () => console.log(`🚀 \x1b[35m[CORE ONLINE] Node API Core listening securely on http://127.0.0.1:${PORT}\x1b[0m`));
}

startBot().catch(err => console.error("Critical server boot trace failure: ", err));
