# Web SQLi Lab Walkthrough

## Goal

Gain authenticated access by exploiting SQL injection and extract sensitive information from exposed routes.

## Expected path

1. Enumerate the web root and note:

- `/login.php`
- `/admin/`
- `/api/status.php`
- `/backup/config.php.bak`
- `/robots.txt`
- `/releases.php`

2. Review hints:

- `robots.txt` is mostly noise
- `/admin/` contains stale internal notes but not direct credentials
- `/releases.php` and other public pages add noise
- `/backup/` still matters if you discover it through enumeration

3. Exploit login SQL injection:

Use a payload such as:

```text
admin' OR '1'='1' --
```

Any password value should work.

4. After access, inspect:

- `/dashboard.php`
- `/search.php`
- `/profile.php`

5. Use the second-stage SQL injection in search to recover more useful data than the initial foothold gives you.

`search.php?q=' OR '1'='1`

## Learning outcome

- route enumeration
- SQL injection authentication bypass
- second-step data access after foothold
