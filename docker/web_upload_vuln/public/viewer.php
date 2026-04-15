<?php
require __DIR__ . '/includes/layout.php';

$page = $_GET['page'] ?? 'pages/home.php';
$allowed = ['pages/home.php', 'pages/help.php'];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viewer</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Content Viewer</h1>
        <p>Rendering: <code><?= e($page) ?></code></p>
        <div class="card">
            <?php
            if (in_array($page, $allowed, true) || str_starts_with($page, 'uploads/')) {
                include $page;
            } else {
                echo 'Page not found in the approved content set.';
            }
            ?>
        </div>
        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
