# Hyve Backend

## Installation

TODO

## Operating behind a reverse proxy

If you run the app behind a reverse proxy, you may find that the URLs Django generates contain internal IP addresses instead of the original host. One way of fixing this is making your reverse proxy set the `X-Forwarded-Host` and `X-Forwarded-Proto` headers accordingly. Apache, for example, seems to set `X-Forwarded-Host` out-of-the-box, but for `X-Forwarded-Proto` it seems you need to add the following line to your Apache configuration:
```
RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
```
Now, to make Django take these headers into account, set the environment variable `USE_PROXY_HEADERS` to `true` (e.g., in your `.env` file).

## Creating an admin account (superuser)

Once the backend is running, you'll probably want to create an admin user. Run the following command:

```
manage.py createsuperuser --username x
```

You will be prompted for an email address and password. It does not matter what argument you specify for `--username`. The username you specify will be ignored and the new user's username will be the email address.  Unfortunately there does not seem to be an easy way to prevent `createsuperuser` from requiring a username, so you have to supply a dummy value.

In this project, users are identified by the combination of their email address and organization. (For admin users, the organization should always be `NULL`.) Since Django assumes that users can be identified by a single field, the user model contains a redundant field `username` that is automatically set to a string containing both email address and organization.