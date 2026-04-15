<?php
$url = $_GET['url'] ?? 'http://example.com';
$output = '';

if (isset($_GET['url'])) {
    $context = stream_context_create([
        'http' => [
            'timeout' => 3,
        ],
    ]);
    $output = @file_get_contents($url, false, $context);
    if ($output === false) {
        $output = 'No se pudo recuperar el recurso.';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fetcher</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Endpoint Fetcher</h1>
        <div class="notice">Internal utility for checking HTTP responses from the backend.</div>

        <form method="get" action="/fetch.php">
            <label for="url">URL</label>
            <input id="url" name="url" value="<?= htmlspecialchars($url, ENT_QUOTES, 'UTF-8') ?>" placeholder="http://service.local/status">
            <button type="submit">Fetch</button>
        </form>

        <?php if ($output !== ''): ?>
            <h2>Response</h2>
            <pre><?= htmlspecialchars($output, ENT_QUOTES, 'UTF-8') ?></pre>
        <?php endif; ?>

        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
