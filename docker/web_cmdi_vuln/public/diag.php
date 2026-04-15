<?php
$target = $_GET['target'] ?? '127.0.0.1';
$output = '';

if (isset($_GET['target'])) {
    $filtered = str_replace([';', '&', '|'], '', $target);
    $command = "ping -c 1 " . $filtered;
    $output = shell_exec($command . " 2>&1") ?? "No output";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnostics</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Diagnostics</h1>
        <div class="notice">Internal utility for checking latency from the server. Basic separators are filtered.</div>

        <form method="get" action="/diag.php">
            <label for="target">Target</label>
            <input id="target" name="target" value="<?= htmlspecialchars($target, ENT_QUOTES, 'UTF-8') ?>" placeholder="127.0.0.1">
            <button type="submit">Run</button>
        </form>

        <?php if ($output !== ''): ?>
            <h2>Output</h2>
            <pre><?= htmlspecialchars($output, ENT_QUOTES, 'UTF-8') ?></pre>
        <?php endif; ?>

        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
