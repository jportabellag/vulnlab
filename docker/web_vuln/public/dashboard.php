<?php
require __DIR__ . '/includes/bootstrap.php';
require_login();

$tickets = db()->query('SELECT id, title, description, owner FROM tickets ORDER BY id ASC')
    ->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Dashboard</h1>
        <p>Welcome, <strong><?= e($_SESSION['user']['username']) ?></strong> (<?= e($_SESSION['user']['role']) ?>).</p>
        <p>
            <a href="/search.php">Search tickets</a> |
            <a href="/profile.php">My profile</a> |
            <a href="/logout.php">Sign out</a>
        </p>

        <h2>Internal tickets</h2>
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
                <?php foreach ($tickets as $ticket): ?>
                    <tr>
                        <td><?= e((string) $ticket['id']) ?></td>
                        <td><?= e($ticket['title']) ?></td>
                        <td><?= e($ticket['description']) ?></td>
                        <td><?= e($ticket['owner']) ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</body>
</html>
