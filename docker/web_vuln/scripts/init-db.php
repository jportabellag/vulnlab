<?php

$dbPath = '/opt/vulnlab/data/app.db';

if (file_exists($dbPath)) {
    exit(0);
}

$dir = dirname($dbPath);
if (!is_dir($dir)) {
    mkdir($dir, 0777, true);
}

$db = new PDO('sqlite:' . $dbPath);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$db->exec('CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT NOT NULL
)');

$users = [
    ['admin', 'superadmin123', 'admin', 'admin@vulnlab.local'],
    ['developer', 'devpass', 'user', 'dev@vulnlab.local'],
    ['student', 'lab123', 'user', 'student@vulnlab.local'],
];

foreach ($users as $user) {
    $statement = $db->prepare('INSERT INTO users (username, password, role, email) VALUES (:username, :password, :role, :email)');
    $statement->bindValue(':username', $user[0], PDO::PARAM_STR);
    $statement->bindValue(':password', $user[1], PDO::PARAM_STR);
    $statement->bindValue(':role', $user[2], PDO::PARAM_STR);
    $statement->bindValue(':email', $user[3], PDO::PARAM_STR);
    $statement->execute();
}

$db->exec('CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    owner TEXT NOT NULL
)');

$tickets = [
    ['VPN offline', 'Review the gateway port in staging before the next release.', 'admin'],
    ['Login timeout', 'Users are reporting intermittent login failures.', 'developer'],
    ['Docs cleanup', 'Review legacy endpoints and stale release notes before launch.', 'developer'],
    ['Asset sync', 'Front-end bundle is still pointing to /static-legacy/ on one page.', 'developer'],
];

$db->exec('CREATE TABLE announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL
)');

$announcements = [
    ['Deployment freeze', 'Production release remains frozen until the staging review is complete.'],
    ['Theme refresh', 'Marketing requested a dashboard refresh before quarter close.'],
];

foreach ($announcements as $item) {
    $statement = $db->prepare('INSERT INTO announcements (title, body) VALUES (:title, :body)');
    $statement->bindValue(':title', $item[0], PDO::PARAM_STR);
    $statement->bindValue(':body', $item[1], PDO::PARAM_STR);
    $statement->execute();
}

foreach ($tickets as $ticket) {
    $statement = $db->prepare('INSERT INTO tickets (title, description, owner) VALUES (:title, :description, :owner)');
    $statement->bindValue(':title', $ticket[0], PDO::PARAM_STR);
    $statement->bindValue(':description', $ticket[1], PDO::PARAM_STR);
    $statement->bindValue(':owner', $ticket[2], PDO::PARAM_STR);
    $statement->execute();
}
