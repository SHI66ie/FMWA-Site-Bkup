<?php
// Simple MySQL connection test
try {
    $pdo = new PDO('mysql:host=localhost;charset=utf8mb4', 'root', '');
    echo "Successfully connected to MySQL server!\n";
    
    // Test query
    $stmt = $pdo->query('SELECT VERSION()');
    $version = $stmt->fetchColumn();
    echo "MySQL Server version: " . $version . "\n";
    
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage() . "\n";
    
    // Provide troubleshooting steps
    echo "\nTroubleshooting steps:\n";
    echo "1. Make sure MySQL service is running in XAMPP Control Panel\n";
    echo "2. Check if MySQL is running on port 3306\n";
    echo "3. Try connecting with MySQL command line: mysql -u root -p\n";
    echo "4. Check XAMPP error logs for MySQL\n";
}
