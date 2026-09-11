# GameVerse - Gaming Community Platform

A modern, full-featured gaming community platform with user authentication, game uploads, and discovery.

## Features

✅ **User Authentication**
- Sign up / Login system
- Secure password hashing
- User profiles

✅ **Game Management**
- Upload and showcase games
- Game categories and filtering
- Game ratings and download tracking
- Creator profiles

✅ **Dashboard**
- Creator dashboard
- Game statistics
- Auto-generated game pages

✅ **Community**
- Browse all games
- Filter by category
- Sort by popularity/rating
- User profiles

✅ **Responsive Design**
- Mobile-friendly interface
- Dark theme
- Modern UI with animations

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd gameverse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Visit in browser**
   ```
   http://localhost:5000
   ```

## Deployment

### Deploy to .gg Domain

1. **Get a .gg domain** from [GoDaddy](https://www.godaddy.com), [Namecheap](https://www.namecheap.com), or similar

2. **Deploy to Heroku/Railway/Render**:
   ```bash
   # Using Railway
   railway init
   railway up
   ```

3. **Configure DNS** pointing to your hosting provider

4. **Set environment variables**:
   ```
   SECRET_KEY=your-secure-key
   DATABASE_URL=your-db-url
   ```

## Usage

### Create Account
1. Click "Register"
2. Fill in username, email, password
3. Click "Register"

### Upload Game
1. Log in to your account
2. Go to Dashboard
3. Click "Upload New Game"
4. Fill in game details
5. Submit

### Browse Games
1. Click "Games" in navigation
2. Filter by category
3. Sort by latest/popular/rated
4. Click game to view details

## File Structure

```
GameVerse/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── games.html        # Games listing
│   └── profile.html      # User profile
├── static/
│   ├── style.css         # Main styles
│   ├── main.js           # JavaScript
│   └── images/           # Game images
└── README.md
```

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Flask-Login
- **Styling**: Custom CSS with dark theme

## Future Enhancements

- [ ] Game reviews and ratings
- [ ] Comment system
- [ ] Social features (follow creators)
- [ ] In-game achievements
- [ ] Payment system for premium games
- [ ] API endpoints
- [ ] Advanced search
- [ ] Game statistics and analytics

## License

MIT License - feel free to use for personal/commercial projects

## Support

For issues or questions, create an issue on GitHub.

---

**Ready to launch your gaming community? Deploy now!** 🚀