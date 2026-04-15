<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Debug Notes</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Debug Notes</h1>
        <div class="notice">Do not expose internal references publicly. The old inventory connector is still enabled during staging review.</div>
        <ul>
            <li>Legacy backend listens on a local-only port.</li>
            <li>Metrics and secret material are still served by the same connector.</li>
        </ul>
    </div>
</body>
</html>
