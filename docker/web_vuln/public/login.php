<?php
require __DIR__ . '/includes/bootstrap.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $sql = "SELECT id, username, role, email FROM users WHERE username = '$username' AND password = '$password' LIMIT 1";
    $result = db()->query($sql);
    $user = $result ? $result->fetch(PDO::FETCH_ASSOC) : false;

    if ($user) {
        $_SESSION['user'] = $user;
        header('Location: /dashboard.php');
        exit;
    }

    $error = 'Invalid credentials.';
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Employee Login</h1>
        <p>Access the internal portal.</p>

        <?php if ($error): ?>
            <div class="notice danger"><?= e($error) ?></div>
        <?php endif; ?>

        <form method="post" action="/login.php">
            <label for="username">Username</label>
            <input id="username" name="username" placeholder="developer">

            <label for="password">Password</label>
            <input id="password" name="password" type="password" placeholder="********">

            <button type="submit">Sign in</button>
        </form>

        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
