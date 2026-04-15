<?php
$requested = $_GET['file'] ?? 'files/employee-handbook.txt';
$normalized = str_replace('../', '', $requested);
$target = __DIR__ . '/' . $normalized;

if (!is_file($target)) {
    http_response_code(404);
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Download Failed</title>
        <link rel="stylesheet" href="/assets/style.css">
    </head>
    <body>
    <div class="container">
        <h1>Download Failed</h1>
        <p>The requested document was not found after path normalization.</p>
        <p><strong>Requested:</strong> <code><?= htmlspecialchars($requested, ENT_QUOTES, 'UTF-8') ?></code></p>
        <p><strong>Normalized:</strong> <code><?= htmlspecialchars($normalized, ENT_QUOTES, 'UTF-8') ?></code></p>
    </div>
    </body>
    </html>
    <?php
    exit;
}

$filename = basename($target);
header('Content-Type: text/plain; charset=UTF-8');
header('Content-Disposition: inline; filename="' . $filename . '"');
readfile($target);
