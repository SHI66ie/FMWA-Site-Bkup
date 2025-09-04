<?php
// Database configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'fmwa_db');
define('DB_USER', 'root');
define('DB_PASS', '');

// Application paths
define('BASE_PATH', realpath(dirname(__DIR__)));
define('UPLOAD_DIR', BASE_PATH . '/images/uploads/');

// Site settings
define('SITE_NAME', 'Federal Ministry of Women Affairs');
define('SITE_URL', 'http://' . $_SERVER['HTTP_HOST']);

// Error reporting
error_reporting(E_ALL);
ini_set('display_errors', '1');

// Timezone
date_default_timezone_set('Africa/Lagos');

// Session settings
ini_set('session.cookie_httponly', 1);
ini_set('session.use_only_cookies', 1);
ini_set('session.cookie_secure', isset($_SERVER['HTTPS']));
session_start();
?>
