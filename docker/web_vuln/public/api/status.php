<?php
header('Content-Type: application/json');

echo json_encode([
    'app' => 'vulnlab-intranet',
    'environment' => 'training',
    'status' => 'ok',
    'modules' => ['login', 'tickets', 'profile'],
]);
