# Web Upload And LFI Lab Walkthrough

## Goal

Abuse unrestricted file upload and identify local file inclusion in the viewer.

## Expected path

1. Enumerate:

- `/upload.php`
- `/viewer.php`
- `/dev/`
- `/backup/dev-config.php.bak`
- `/uploads/`

2. Upload a harmless test file first to understand the storage behavior.

3. Observe that the application rewrites the stored filename and does not directly hand you code execution.

4. Test the legacy viewer:

```text
/viewer.php?page=pages/home.php
```

Then include your uploaded content through:

```text
/viewer.php?page=uploads/<your-file>.txt
```

5. Use `/dev/` and the backup file for hints about developer assumptions and server paths.

## Learning outcome

- unrestricted upload discovery
- LFI surface identification
- developer artifact leakage
