# Hyve Backend

## Installation

TODO

## Operating behind a reverse proxy

If you run the app behind a reverse proxy, you may find that the URLs Django generates contain internal IP addresses instead of the original host. One way of fixing this is making your reverse proxy set the `X-Forwarded-Host` and `X-Forwarded-Proto` headers accordingly. Apache, for example, seems to set `X-Forwarded-Host` out-of-the-box, but for `X-Forwarded-Proto` it seems you need to add the following line to your Apache configuration:
```
RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
```
Now, to make Django take these headers into account, set the environment variable `USE_PROXY_HEADERS` to `true` (e.g., in your `.env` file).
