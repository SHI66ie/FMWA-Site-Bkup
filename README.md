# Federal Ministry of Women Affairs website

 Federal Ministry of Women Affairs up to date website following the Nigerian Government Guidlines.

## Features

- **Fully Responsive**: Works on all devices from mobile phones to desktops
- **Modern UI/UX**: Clean and professional design with smooth animations
- **Bootstrap 5**: Built with the latest version of Bootstrap framework

## Getting Started

### Prerequisites

- Node.js 14.x or higher
- npm 6.x or higher
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A code editor (VS Code, Sublime Text, etc.)

### Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Production Deployment

1. Install dependencies with production flag:
   ```bash
   npm install --production
   ```
2. Start the server:
   ```bash
   npm start
   ```
3. The application will be available on the specified port (default: 3000)

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
NODE_ENV=production
PORT=3000
```

## Project Structure

```
ohcsf-website/
├── server.js          # Express server
├── package.json       # Dependencies and scripts
├── .env               # Environment variables (create this file)
├── .gitignore         # Git ignore file
├── index.html         # Main HTML file
├── css/              # Stylesheets
│   └── style.css     # Main styles
├── js/               # JavaScript files
│   └── main.js       # Main JavaScript
└── images/           # Image assets
```

## Deployment Options

### PM2 (Recommended for Production)

1. Install PM2 globally:
   ```bash
   npm install -g pm2
   ```
2. Start the application:
   ```bash
   pm2 start server.js --name "ohcsf-website"
   ```
3. Set up PM2 to start on system boot:
   ```bash
   pm2 startup
   pm2 save
   ```

### Docker

1. Build the Docker image:
   ```bash
   docker build -t ohcsf-website .
   ```
2. Run the container:
   ```bash
   docker run -p 3000:3000 -d ohcsf-website
   ```

## Monitoring

For production monitoring, consider using:
- PM2 Monitoring
- New Relic
- Datadog

## Security

- All dependencies are regularly audited
- Security headers are set using Helmet
- Rate limiting is implemented
- CORS is properly configured
- Environment variables are used for sensitive data

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS 10+)
- Chrome for Android

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)
- [Animate.css](https://animate.style/) (for animations)

## Contact

For any inquiries, please contact the OHCSF ICT Department at [your.email@example.com]
