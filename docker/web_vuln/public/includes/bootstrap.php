<?php

session_start();

function db(): PDO
{
    static $db = null;

    if ($db === null) {
        $db = new PDO('sqlite:/opt/vulnlab/data/app.db');
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    return $db;
}

function current_user(): ?array
{
    if (!isset($_SESSION['user'])) {
        return null;
    }

    return $_SESSION['user'];
}

function require_login(): void
{
    if (!current_user()) {
        header('Location: /login.php');
        exit;
    }
}

function e(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}
