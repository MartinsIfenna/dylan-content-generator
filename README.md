# Dylan Content Generator

A modern, client-side commercial real estate content generator designed for GitHub Pages deployment.

## 🚀 Features

- **Zero Server Dependencies** - Pure client-side JavaScript
- **GitHub Pages Ready** - Deploy instantly with no build process
- **AI-Powered Content** - OpenAI integration for dynamic content
- **Real Market Data** - FRED API integration for economic indicators
- **Template Fallbacks** - Works without API keys
- **Modern UI** - Responsive design with Tailwind CSS
- **Industry News** - Latest CRE news integration
- **Export Options** - Copy to clipboard or download content

## 📋 Content Types

### Short LinkedIn Posts
- Multifamily Market Trends
- Interest Rate Impact
- Gateway Market Analysis
- Sun Belt Dynamics
- Capital Flow Trends
- Development Pipeline
- Investment Strategy
- Debt Markets

### Long Articles
- Comprehensive market analysis
- Investment implications
- Regional spotlights
- Trend analysis

## 🔧 Setup

### GitHub Pages Deployment (Recommended)
1. Fork this repository
2. Enable GitHub Pages in repository settings
3. Point to root directory (`/`)
4. Access at `https://yourusername.github.io/dylan-content-generator/`

### Local Development
1. Clone repository
2. Open `index.html` in browser
3. Or serve with: `python -m http.server 8000`

## 🔑 API Configuration

### OpenAI API Key (Optional)
- Enables AI-powered content generation
- Get key from: https://platform.openai.com/api-keys
- Enter in the web interface (stored locally only)

### FRED API Key (Optional)
- Enables real economic data
- Get key from: https://fred.stlouisfed.org/docs/api/api_key.html
- Free registration required

## 🏗️ Architecture

```
dylan-content-generator/
├── index.html          # Main application
├── js/
│   └── app.js         # Core application logic
├── .env.example       # API key reference
└── README.md          # This file
```

### Dependencies
- **Tailwind CSS** - Styling (CDN)
- **Font Awesome** - Icons (CDN)
- **Vanilla JavaScript** - No frameworks
- **Browser APIs** - Fetch, Clipboard, File Download

## 🎯 Key Benefits

✅ **No Build Process** - Works immediately  
✅ **No Server Required** - Pure client-side  
✅ **No Package Dependencies** - CDN only  
✅ **GitHub Pages Compatible** - Deploy in seconds  
✅ **API Key Optional** - Template fallbacks included  
✅ **Mobile Responsive** - Works on all devices  
✅ **Fast Loading** - Minimal dependencies  
✅ **Secure** - API keys never leave browser  

## 🔄 Data Sources

### Economic Data (FRED API)
- Federal Funds Rate
- 10-Year Treasury Rate
- 30-Year Mortgage Rate
- Unemployment Rate

### Market Intelligence
- Transaction trends
- Cap rate movements
- Market sentiment
- Investment activity

### Industry News
- Latest CRE headlines
- Market reports
- Investment trends
- Regional updates

## 📱 Usage

1. **Configure APIs** (optional)
   - Enter OpenAI key for AI generation
   - Enter FRED key for real economic data

2. **Select Content Type**
   - Short LinkedIn post
   - Long article

3. **Choose Topic**
   - Pick from 8 CRE-focused topics

4. **Generate Content**
   - AI-powered or template-based
   - Incorporates real market data

5. **Export Content**
   - Copy to clipboard
   - Download as text file

## 🚀 Deployment

### GitHub Pages Setup
```bash
# 1. Create new repository or use existing
# 2. Upload files to root directory
# 3. Go to repository Settings > Pages
# 4. Select source branch (main)
# 5. Set folder to / (root)
# 6. Save and wait for deployment
```

### Custom Domain (Optional)
```bash
# Add CNAME file with your domain
echo "your-domain.com" > CNAME
```

## 🔒 Security

- API keys stored in browser memory only
- No server-side data storage
- HTTPS required for clipboard API
- CORS-compliant API calls

## 🎨 Customization

### Adding New Topics
Edit `contentTemplates` in `js/app.js`:
```javascript
this.contentTemplates = {
    short: {
        'new-topic': `Your template here...`,
    },
    long: {
        'new-topic': `Your long-form template...`
    }
};
```

### Styling Changes
- Modify Tailwind classes in `index.html`
- Or add custom CSS

### New Data Sources
Add to `fetchPublicMarketData()` method in `js/app.js`

## 📊 Performance

- **Load Time**: < 2 seconds
- **Bundle Size**: ~50KB (HTML + JS)
- **Dependencies**: 2 CDN resources
- **Browser Support**: Modern browsers (ES6+)

## 🆘 Troubleshooting

### API Issues
- Check API key validity
- Verify CORS settings
- Check browser console for errors

### GitHub Pages Issues
- Ensure repository is public (or GitHub Pro)
- Check Pages settings in repository
- Verify file paths are correct

### Content Generation Issues
- Templates work without API keys
- Check browser console for errors
- Verify internet connection for data sources

---

**Built for reliability, simplicity, and instant deployment.**
