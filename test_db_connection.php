<?php
try {
    $config = [
        'host' => 'localhost',
        'database' => 'mysql', // Connect to default system database first
        'username' => 'root',
        'password' => '',
        'charset' => 'utf8mb4',
    ];

    $dsn = "mysql:host={$config['host']};dbname={$config['database']};charset={$config['charset']}";
    $pdo = new PDO($dsn, $config['username'], $config['password'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
    
    echo "Successfully connected to MySQL server!\n";
    
    // Check if our database exists
    $stmt = $pdo->query("SHOW DATABASES LIKE 'fmwa_db'");
    if ($stmt->rowCount() > 0) {
        echo "Database 'fmwa_db' exists.\n";
    } else {
        echo "Database 'fmwa_db' does not exist.\n";
    }
    
} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage() . "\n");
}
