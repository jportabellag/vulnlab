<?php
require __DIR__ . '/includes/layout.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Center</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Upload Center</h1>
        <p>Internal portal for sharing reports and reviewing team templates.</p>

        <div class="grid">
            <div class="card">
                <h2>Uploader</h2>
                <p>Fast upload area for evidence files and scripts.</p>
                <p><a href="/upload.php">Open uploader</a></p>
            </div>
            <div class="card">
                <h2>Viewer</h2>
                <p>Simple viewer for internal pages and legacy content.</p>
                <p><a href="/viewer.php?page=pages/home.php">Open viewer</a></p>
            </div>
        </div>

        <!-- cleanup pending: /dev /backup /uploads -->
    </div>
</body>
</html>
