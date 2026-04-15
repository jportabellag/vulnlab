# Web SSRF Lab

## Summary

A PHP target with server-side URL fetching and a backend-only localhost service.

## Recommended Tools

- `ffuf`
- browser
- Burp Suite
- `curl`

## Learning Goals

- identify SSRF in a legitimate-looking fetch flow
- target localhost-only internal services through the vulnerable server
- recover internal-only data through the backend request path
