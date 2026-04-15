<?php
$token = $_SERVER['HTTP_X_LAB_TOKEN'] ?? '';

if ($token !== 'export-token-7421') {
    http_response_code(403);
    header('Content-Type: text/plain; charset=UTF-8');
    echo "Missing or invalid export token.";
    exit;
}

header('Content-Type: text/plain; charset=UTF-8');
readfile('/opt/vulnlab/data/internal-export.txt');
