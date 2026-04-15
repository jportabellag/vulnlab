<?php
require __DIR__ . '/includes/bootstrap.php';
require_login();

$user = current_user();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Profile</h1>
        <p>This view intentionally exposes only the current session profile.</p>
        <table>
            <tr><th>Username</th><td><?= e($user['username']) ?></td></tr>
            <tr><th>Role</th><td><?= e($user['role']) ?></td></tr>
            <tr><th>Email</th><td><?= e($user['email']) ?></td></tr>
        </table>
        <p><a href="/dashboard.php">Back to dashboard</a></p>
    </div>
</body>
</html>
