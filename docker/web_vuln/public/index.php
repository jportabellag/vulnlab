<?php
require __DIR__ . '/includes/bootstrap.php';

$user = current_user();
$announcements = db()->query('SELECT title, body FROM announcements ORDER BY id DESC')
    ->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VulnLab Intranet</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Intranet Portal</h1>
        <p>Sample internal application for a basic web security training lab.</p>

        <div class="grid">
            <div class="card">
                <h2>Access</h2>
                <p>Authentication portal for employees and administrators.</p>
                <p><a href="/login.php">Open login</a></p>
            </div>
            <div class="card">
                <h2>Status</h2>
                <p>Authenticated users can review internal tickets and support utilities.</p>
                <?php if ($user): ?>
                    <p>Signed in as <strong><?= e($user['username']) ?></strong>.</p>
                    <p><a href="/dashboard.php">Open dashboard</a></p>
                <?php else: ?>
                    <p>No active session.</p>
                <?php endif; ?>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <h2>Company Updates</h2>
            <?php foreach ($announcements as $item): ?>
                <p><strong><?= e($item['title']) ?>:</strong> <?= e($item['body']) ?></p>
            <?php endforeach; ?>
        </div>

        <!-- TODO: clean stale release content before launch -->
    </div>
</body>
</html>
