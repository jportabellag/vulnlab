<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dev Notes</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Developer Notes</h1>
        <div class="notice">
            Do not publish this in production. Review `/backup/dev-config.php.bak` and clean old uploads.
        </div>
        <ul>
            <li>The `/uploads/` directory still allows attachments without filtering.</li>
            <li>The legacy viewer still loads paths directly from the query string.</li>
        </ul>
    </div>
</body>
</html>
