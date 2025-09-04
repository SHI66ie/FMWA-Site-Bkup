# Federal Ministry of Women Affairs - PHP Version

This is the PHP version of the Federal Ministry of Women Affairs website, converted from Node.js to work on standard PHP hosting environments.

## Requirements

- PHP 7.4 or higher
- Apache or Nginx web server
- MySQL 5.7 or higher (if using database features)
- mod_rewrite enabled (for clean URLs)

## Installation

1. Upload all files to your web server's public directory (usually `public_html` or `htdocs`)
2. Ensure the following directories are writable by the web server:
   - `/images/uploads/`
   - Any other upload directories you create
3. Update the database configuration in `config.php` if using a database
4. Set the document root to point to the `public` directory

## Configuration

### Apache
Ensure your `.htaccess` file is properly configured and `AllowOverride All` is set for the document root.

### Nginx
Add the following to your server block:

```nginx
location / {
    try_files $uri $uri/ /index.php?$args;
}
```

## File Structure

- `/public` - Publicly accessible files
  - `index.php` - Main entry point
  - `.htaccess` - URL rewriting rules
  - `upload.php` - File upload handler
- `/departments` - Department pages
- `/images` - Image assets
- `/css` - Stylesheets
- `/js` - JavaScript files
- `config.php` - Application configuration

## Features

- Clean URL routing
- File upload handling
- Basic error pages
- MIME type handling for various file types

## Security Notes

1. Ensure file uploads are properly secured in production
2. Keep PHP updated to the latest version
3. Regularly backup your database and uploaded files
4. Use HTTPS for all connections

## Troubleshooting

- If you get a 500 error, check PHP error logs
- Ensure all required PHP extensions are installed
- Verify file permissions on upload directories
- Check that mod_rewrite is enabled

## License

This project is licensed under the MIT License.
