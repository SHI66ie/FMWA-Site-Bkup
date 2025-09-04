<?php
require_once 'includes/Database.php';

// Test database connection
$db = Database::getInstance();

try {
    // Test connection
    $version = $db->fetch("SELECT VERSION() as version");
    echo "Connected to MySQL version: " . $version->version . "<br>\n";
    
    // Test insert
    $testData = [
        'username' => 'testuser_' . time(),
        'email' => 'test' . time() . '@example.com',
        'full_name' => 'Test User',
        'password' => password_hash('test123', PASSWORD_DEFAULT),
        'role' => 'subscriber',
        'status' => 'active'
    ];
    
    $userId = $db->insert('users', $testData);
    echo "Inserted user with ID: $userId<br>\n";
    
    // Test fetch
    $user = $db->find('users', $userId);
    echo "Fetched user: " . $user->username . "<br>\n";
    
    // Test update
    $updateCount = $db->update('users', 
        ['full_name' => 'Updated Name'],
        'id = ?', 
        [$userId]
    );
    echo "Updated $updateCount user(s)<br>\n";
    
    // Test transaction
    $db->beginTransaction();
    try {
        $newId = $db->insert('users', [
            'username' => 'temp_user',
            'email' => 'temp@example.com',
            'full_name' => 'Temp User',
            'password' => password_hash('temp123', PASSWORD_DEFAULT),
            'role' => 'subscriber',
            'status' => 'active'
        ]);
        
        // This will cause a duplicate entry error due to unique constraint
        // $db->insert('users', [
        //     'username' => 'temp_user',
        //     'email' => 'temp2@example.com',
        //     'full_name' => 'Another Temp',
        //     'password' => password_hash('temp123', PASSWORD_DEFAULT),
        //     'role' => 'subscriber',
        //     'status' => 'active'
        // ]);
        
        $db->commit();
        echo "Transaction committed successfully<br>\n";
    } catch (Exception $e) {
        $db->rollback();
        echo "Transaction rolled back: " . $e->getMessage() . "<br>\n";
    }
    
    // Clean up
    $db->delete('users', 'id = ?', [$userId]);
    
} catch (Exception $e) {
    die("Error: " . $e->getMessage());
}

echo "All tests completed successfully!";
