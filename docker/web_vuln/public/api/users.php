<?php
http_response_code(403);
header('Content-Type: application/json');

echo json_encode([
    'error' => 'forbidden',
    'message' => 'directory listing disabled',
]);
