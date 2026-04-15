<?php
require __DIR__ . '/../includes/bootstrap.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Area</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Admin Notes</h1>
        <div class="notice danger">
            <strong>Internal only.</strong> Review stale admin content before the next deployment.
        </div>
        <ul>
            <li>Audit endpoint remains enabled in staging.</li>
            <li>Old admin notes should be removed from this page.</li>
            <li>Do not store credentials in release notes or ticket comments.</li>
        </ul>
    </div>
</body>
</html>
