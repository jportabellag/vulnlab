<?php
$downloads = [
    'files/employee-handbook.txt' => 'Employee handbook',
    'files/network-faq.txt' => 'Network FAQ',
    'files/expense-policy.txt' => 'Expense policy',
];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document Gateway</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<div class="container">
    <h1>Document Gateway</h1>
    <p>Legacy documentation front-end for operations, HR, and export workflows.</p>

    <div class="notice">
        Path normalization is enabled on the download gateway. Legacy mobile clients still use header-based export authentication.
    </div>

    <div class="grid">
        <section class="card">
            <h2>Download Center</h2>
            <p>Use <code>download.php?file=...</code> for portable access from old clients.</p>
            <ul class="downloads">
                <?php foreach ($downloads as $path => $label): ?>
                    <li><a href="/download.php?file=<?= urlencode($path) ?>"><?= htmlspecialchars($label, ENT_QUOTES, 'UTF-8') ?></a></li>
                <?php endforeach; ?>
            </ul>
        </section>

        <section class="card">
            <h2>Service Pages</h2>
            <ul>
                <li><a href="/release-notes.php">Release notes</a></li>
                <li><a href="/status.php">Portal status</a></li>
                <li><a href="/docs/connector.txt">Connector guide</a></li>
            </ul>
        </section>

        <section class="card">
            <h2>Legacy Export</h2>
            <p>Restricted export route for field clients. Browser access is denied without the expected request header.</p>
        </section>
    </div>
</div>
</body>
</html>
