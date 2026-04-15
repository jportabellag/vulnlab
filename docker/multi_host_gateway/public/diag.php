<?php
$target = $_GET['target'] ?? '127.0.0.1';
$output = '';

if (isset($_GET['target'])) {
    $command = "curl -s " . $target;
    $output = shell_exec($command . " 2>&1") ?? "No output";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diag</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Gateway Diagnostic</h1>
        <div class="notice">Temporary utility for reviewing URLs from the gateway.</div>

        <form method="get" action="/diag.php">
            <label for="target">Target URL</label>
            <input id="target" name="target" value="<?= htmlspecialchars($target, ENT_QUOTES, 'UTF-8') ?>" placeholder="http://ops-relay-cache:8080/health">
            <button type="submit">Run</button>
        </form>

        <?php if ($output !== ''): ?>
            <h2>Response</h2>
            <pre><?= htmlspecialchars($output, ENT_QUOTES, 'UTF-8') ?></pre>
        <?php endif; ?>

        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
