<?php
require __DIR__ . '/includes/layout.php';

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['document'])) {
    $name = basename($_FILES['document']['name']);
    $target = __DIR__ . '/uploads/' . $name . '.txt';

    if (move_uploaded_file($_FILES['document']['tmp_name'], $target)) {
        $message = "File uploaded to /uploads/" . $name . ".txt";
    } else {
        $message = 'Upload failed.';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uploader</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="container">
        <h1>Evidence Upload</h1>
        <p>Reports, scripts, and temporary attachments are accepted. Uploaded files are normalized before storage.</p>

        <?php if ($message): ?>
            <div class="notice"><?= e($message) ?></div>
        <?php endif; ?>

        <form method="post" enctype="multipart/form-data">
            <label for="document">File</label>
            <input id="document" type="file" name="document">
            <button type="submit">Upload</button>
        </form>

        <p>Stored files are not linked automatically from this view.</p>
        <p><a href="/">Back</a></p>
    </div>
</body>
</html>
