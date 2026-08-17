# Security Policy

## Sensitive inputs

Content Universe is designed to process browser/network artifacts that may contain secrets. Treat the following as sensitive by default:

- HAR files
- browser cookies
- authorization headers
- API keys
- Cloudflare/Turnstile clearance tokens
- session IDs
- private asset URLs
- downloaded private creative assets
- local SQLite catalogs containing private generations

These are ignored by the repository where practical, but `.gitignore` is not a security boundary.

## Before publishing a fixture

1. Start from a copy, never the original capture.
2. Run the conservative sanitizer where applicable.
3. Remove irrelevant requests and response bodies.
4. Search for `authorization`, `cookie`, `token`, `session`, `bearer`, `key`, email addresses, user IDs, and private URLs.
5. Manually inspect the diff before committing.
6. Prefer synthetic fixtures over redacted production data when a synthetic sample tests the same parser behavior.

## Live transports

The core library does not own or persist Ideogram/Suno browser credentials. Any live authenticated transport must be supplied by the caller. Do not add code that embeds personal cookies, tokens, browser profiles, or hard-coded credentials.

## Asset downloads

The built-in public Ideogram downloader only accepts HTTPS URLs from an explicit host allowlist and does not copy browser authentication state. Private/authenticated download integrations should remain opt-in and caller-controlled.

## Reporting

Do not open a public issue containing credentials or raw private captures. Report sensitive problems privately to the repository owner through GitHub's private security reporting facilities when enabled.
