<?php
require __DIR__ . '/includes/bootstrap.php';
require_login();

$q = $_GET['q'] ?? '';
$results = null;

if ($q !== '') {
    $sql = "SELECT id, title, description, owner FROM tickets WHERE title LIKE '%$q%' OR description LIKE '%$q%' ORDER BY id ASC";
    $results = db()->query($sql);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Ticket Search</h1>
        <p>Search currently scans ticket titles and descriptions only.</p>
        <form method="get" action="/search.php">
            <label for="q">Query</label>
            <input id="q" name="q" value="<?= e($q) ?>" placeholder="backup">
            <button type="submit">Search</button>
        </form>

        <?php if ($results): ?>
            <h2>Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Titulo</th>
                        <th>Descripcion</th>
                        <th>Owner</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($results->fetchAll(PDO::FETCH_ASSOC) as $row): ?>
                        <tr>
                            <td><?= e((string) $row['id']) ?></td>
                            <td><?= e($row['title']) ?></td>
                            <td><?= e($row['description']) ?></td>
                            <td><?= e($row['owner']) ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php elseif ($q !== ''): ?>
            <p>No results found.</p>
        <?php endif; ?>

        <p><a href="/dashboard.php">Back to dashboard</a></p>
    </div>
</body>
</html>
