<?php
// Disable error reporting for production
// error_reporting(0);
// Enable for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

$step = $_GET['step'] ?? 1;
$message = '';
$error = '';
$success = false;

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($step === 1) {
        // Save database configuration
        $config = [
            'host' => $_POST['host'] ?? 'localhost',
            'database' => $_POST['database'] ?? 'fmwa_db',
            'username' => $_POST['username'] ?? 'root',
            'password' => $_POST['password'] ?? '',
            'charset' => 'utf8mb4',
        ];
        
        // Test connection
        try {
            $dsn = "mysql:host={$config['host']};charset={$config['charset']}";
            $pdo = new PDO($dsn, $config['username'], $config['password'], [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
            ]);
            
            // Save config
            $configContent = "<?php\n\nreturn " . var_export($config, true) . ";\n";
            file_put_contents(__DIR__ . '/config/database.php', $configContent);
            
            // Proceed to next step
            header('Location: setup.php?step=2');
            exit;
            
        } catch (PDOException $e) {
            $error = "Database connection failed: " . $e->getMessage();
        }
    } elseif ($step === 2) {
        // Create database and tables
        try {
            $config = require __DIR__ . '/config/database.php';
            
            // Create database if it doesn't exist
            $dsn = "mysql:host={$config['host']};charset={$config['charset']}";
            $pdo = new PDO($dsn, $config['username'], $config['password'], [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
            ]);
            
            $pdo->exec("CREATE DATABASE IF NOT EXISTS `{$config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
            $pdo->exec("USE `{$config['database']}`");
            
            // Read and execute schema
            $schema = file_get_contents(__DIR__ . '/database/schema.sql');
            $pdo->exec($schema);
            
            $success = true;
            $message = "Database setup completed successfully!";
            
        } catch (PDOException $e) {
            $error = "Database setup failed: " . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FMWA Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .setup-container { max-width: 600px; margin: 0 auto; }
        .step { display: none; }
        .step.active { display: block; }
    </style>
</head>
<body>
    <div class="container setup-container">
        <h1 class="mb-4">FMWA Website Setup</h1>
        
        <?php if ($error): ?>
            <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <?php if ($success): ?>
            <div class="alert alert-success">
                <?php echo htmlspecialchars($message); ?>
                <p class="mt-3">
                    <a href="admin/" class="btn btn-primary">Go to Admin Panel</a>
                </p>
            </div>
        <?php else: ?>
            <div class="card">
                <div class="card-header">
                    <ul class="nav nav-tabs card-header-tabs">
                        <li class="nav-item">
                            <a class="nav-link <?php echo $step == 1 ? 'active' : ''; ?>" href="?step=1">1. Database Setup</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link <?php echo $step == 2 ? 'active' : ''; ?>" href="?step=2" <?php echo $step < 2 ? 'disabled' : ''; ?>>2. Install Database</a>
                        </li>
                    </ul>
                </div>
                <div class="card-body">
                    <?php if ($step == 1): ?>
                        <h5 class="card-title">Database Configuration</h5>
                        <p class="card-text">Enter your database connection details below.</p>
                        
                        <form method="post" action="">
                            <div class="mb-3">
                                <label for="host" class="form-label">Database Host</label>
                                <input type="text" class="form-control" id="host" name="host" value="localhost" required>
                            </div>
                            <div class="mb-3">
                                <label for="database" class="form-label">Database Name</label>
                                <input type="text" class="form-control" id="database" name="database" value="fmwa_db" required>
                            </div>
                            <div class="mb-3">
                                <label for="username" class="form-label">Database Username</label>
                                <input type="text" class="form-control" id="username" name="username" value="root" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Database Password</label>
                                <input type="password" class="form-control" id="password" name="password">
                            </div>
                            <button type="submit" class="btn btn-primary">Continue</button>
                        </form>
                        
                    <?php elseif ($step == 2): ?>
                        <h5 class="card-title">Install Database</h5>
                        <p class="card-text">Click the button below to install the database tables and initial data.</p>
                        
                        <form method="post" action="">
                            <div class="alert alert-warning">
                                <strong>Warning:</strong> This will create all necessary database tables. 
                                Any existing data with the same table names will be lost.
                            </div>
                            <button type="submit" class="btn btn-primary" onclick="return confirm('Are you sure you want to install the database?')">
                                Install Database
                            </button>
                        </form>
                    <?php endif; ?>
                </div>
            </div>
        <?php endif; ?>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
