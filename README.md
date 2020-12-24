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
manage.py createsuperuser
```

You will be prompted for an email address (which will also serve as the account's username) and password.

In this project, users are identified by the combination of their email address and organization. (For admin users, the organization should always be `NULL`.) Since Django assumes that users can be identified by a single field, the user model contains a redundant field `username` that is automatically set to a string containing both email address and organization.

This implies that you will **not** be able to log in with this admin account to frontend instances. If you want to log in to an organization's frontend, you must create an account there. The email address may be the same.

If, for example, your admin account has the email address `me@example.com` and then you also use that email address for an account with the organization whose UUID is `123e4567-e89b-12d3-a456-426614174000`, you will have the following two usernames in the database:
- `me@example.com` (your admin account, used for the Django admin interface)
- `me@example.com:123e4567-e89b-12d3-a456-426614174000` (the account for the organization's frontend)

## Setting up a frontend instance

Typically, every organization has its own frontend. So before you deploy a frontend instance, you'll have to create an organization in the Django admin interface.

Once you created the organization, take note of its UUID. One way of obtaining it is navigating to it in Django admin and extracting it from the URL. You will need to configure this organization's frontend instance to use that UUID to identify the organization.

The frontend instance may also require static pages to be set up. You can also do this with the Django admin interface.