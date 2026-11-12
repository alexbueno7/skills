# Mailcheap API v1 — Referência Validada

Base: `https://{MAILCHEAP_HOST}/api/v1/`

Docs: https://www.mailcheap.co/help/hosted-email/api/v1/

Legenda: `MA` = MasterAdmin, `DA` = DomainAdmin, `MU` = MailUser

**Validado** contra a documentação oficial em jun/2026. Slugs de cada página listados ao final.

## Padrões importantes

- Vários `DELETE` e alguns `PUT` usam **JSON no body** na URL da coleção (sem path param).
- `204` = sucesso sem corpo (`text/html` vazio).
- Respostas não-JSON: logs do servidor (`text/html`), export status etc.
- Thresholds e wlbl usam subpaths `global/` e `domain/{domain}/`.

---

## Authentication

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/auth/` | Não | — |
| GET | `/auth/` | Sim | MA/DA/MU |
| DELETE | `/auth/` | Sim | MA/DA/MU |

**POST /auth/** — `{username, password, otp?}` → `auth.auth_token`, `valid_to`

---

## Two-Factor Authentication (2FA)

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/2fa/{username}/` | Sim | MA/DA/MU |
| POST | `/2fa/verify/` | Sim | MA/DA/MU |
| GET | `/2fa/{username}/` | Sim | MA/DA/MU |
| DELETE | `/2fa/{username}/` | Sim | MA/DA/MU |
| POST | `/2fa/device_password/` | Sim | MU |
| GET | `/2fa/device_password/` | Sim | MU |
| DELETE | `/2fa/device_password/` | Sim | MU |

**POST /2fa/verify/** — `{username, otp}`

**POST /2fa/device_password/** — `{friendly_name}` → `device_password`

**DELETE /2fa/device_password/** — body `{friendly_name}`

---

## Passwordless (WebAuthn)

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/webauthn/registration/options/` | Sim | MA/DA/MU |
| POST | `/webauthn/registration/verify/` | Sim | MA/DA/MU |
| GET | `/webauthn/authentication/options/` | Não | — |
| POST | `/webauthn/authentication/verify/` | Não | — |
| GET | `/webauthn/credentials/` | Sim | MA/DA/MU |
| PUT | `/webauthn/credentials/` | Sim | MA/DA/MU |
| DELETE | `/webauthn/credentials/` | Sim | MA/DA/MU |

**POST /webauthn/authentication/verify/** — retorna `auth.auth_token` (login passwordless).

**DELETE /webauthn/credentials/** — body `{friendly_name}`

---

## Password Authentication

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/auth/password/disable/{username}/` | Sim | MA/DA/MU |
| POST | `/auth/password/disable/{username}/` | Sim | MA/DA/MU |
| DELETE | `/auth/password/disable/{username}/` | Sim | MA/DA/MU |

GET = status (`enabled`/`disabled`). POST = desabilitar. DELETE = habilitar.

Desabilitar exige ≥2 credenciais WebAuthn. MailUsers sem senha usam device passwords.

---

## Account Recovery

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/auth/password/recovery/` | Não | — |
| POST | `/auth/password/reset/` | Não | — |

**POST /auth/password/reset/** — `{username, new_password, recovery_code}`

---

## Accounts

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/accounts/` | Sim | MA/DA* |
| GET | `/accounts/` | Sim | MA/DA/MU |
| GET | `/accounts/{username}/` | Sim | MA/DA/MU |
| PATCH | `/accounts/{username}/` | Sim | MA/DA/MU |
| DELETE | `/accounts/{username}/` | Sim | MA/DA |
| PATCH | `/accounts/cascade/domainadmin/{username}/{action}/` | Sim | MA |
| DELETE | `/accounts/cascade/domainadmin/{username}/` | Sim | MA |
| POST | `/accounts/cascade/ownership/domainadmin/{username}/` | Sim | MA |

\* Criar MailUser: `DA` ou `MA`.

**action** em cascade: `enable` ou `disable` (204).

**GET /accounts/** — query: `limit` (max 50), `start`, `search`, `perm_level`, `enabled`, `api_access`

**POST MailUser:**
```json
{
  "username": "user@domain.tld",
  "password": "SenhaSegura123",
  "perm_level": "MailUser",
  "api_access": 0,
  "enabled": 1,
  "recovery_email": "recovery@domain.tld",
  "language": "pt",
  "domain": "domain.tld",
  "storagequota_total": 100
}
```

---

## Domains

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/domains/` | Sim | MA/DA |
| GET | `/domains/` | Sim | MA/DA |
| DELETE | `/domains/` | Sim | MA/DA |
| POST | `/domains/sdr/{domain}/` | Sim | MA/DA |
| GET | `/domains/sdr/{domain}/` | Sim | MA/DA |
| DELETE | `/domains/sdr/{domain}/` | Sim | MA/DA |
| POST | `/domains/dkim/{domain}/` | Sim | MA/DA |
| GET | `/domains/dkim/{domain}/` | Sim | MA/DA |
| DELETE | `/domains/dkim/{domain}/` | Sim | MA/DA |

**DELETE /domains/** — body `{domain}` (não path param).

**POST /domains/dkim/{domain}/** — body placeholder `{null: null}` na doc oficial.

---

## Domain Aliases

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/domainaliases/` | Sim | MA/DA |
| GET | `/domainaliases/` | Sim | MA/DA |
| DELETE | `/domainaliases/` | Sim | MA/DA |

**POST** — `{domain_alias, rcpt_domain}`

**DELETE** — body `{domain_alias}`

---

## Relay Domains

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/relaydomains/` | Sim | MA/DA |
| GET | `/relaydomains/` | Sim | MA/DA |
| DELETE | `/relaydomains/` | Sim | MA/DA |

**POST** — `{relay_domain, destination_hostname, destination_port}`

**DELETE** — body `{relay_domain}`

---

## Aliases

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/aliases/` | Sim | MA/DA |
| GET | `/aliases/` | Sim | MA/DA |
| PUT | `/aliases/` | Sim | MA/DA |
| DELETE | `/aliases/` | Sim | MA/DA |

**POST/PUT** — `{alias, recipients}` (recipients comma-separated string)

**DELETE** — body `{alias}`

Catch-all: `alias` = `@domain.tld` (desencorajado).

---

## Sender Addresses

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/sender_addresses/` | Sim | MA/DA |
| GET | `/sender_addresses/` | Sim | MA/DA |
| PUT | `/sender_addresses/` | Sim | MA/DA |
| DELETE | `/sender_addresses/` | Sim | MA/DA |

**POST/PUT** — `{sender_address, usernames}`

**DELETE** — body `{sender_address}`

---

## Antispam Thresholds

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/antispam/thresholds/global/` | Sim | MA |
| PUT | `/antispam/thresholds/global/` | Sim | MA |
| POST | `/antispam/thresholds/domain/{domain}/` | Sim | MA/DA |
| GET | `/antispam/thresholds/domain/{domain}/` | Sim | MA/DA |
| PUT | `/antispam/thresholds/domain/{domain}/` | Sim | MA/DA |
| DELETE | `/antispam/thresholds/domain/{domain}/` | Sim | MA/DA |

**Body** — `{reject, add_header, greylist}` (scores inteiros)

---

## Whitelist & Blacklist

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/antispam/wlbl/global/` | Sim | MA |
| GET | `/antispam/wlbl/global/` | Sim | MA |
| PUT | `/antispam/wlbl/global/` | Sim | MA |
| DELETE | `/antispam/wlbl/global/` | Sim | MA |
| POST | `/antispam/wlbl/domain/{domain}/` | Sim | MA/DA |
| GET | `/antispam/wlbl/domain/{domain}/` | Sim | MA/DA |
| PUT | `/antispam/wlbl/domain/{domain}/` | Sim | MA/DA |
| DELETE | `/antispam/wlbl/domain/{domain}/` | Sim | MA/DA |

**Body POST/PUT** — `{action: "whitelist"|"blacklist", sender_domains?, sender_emails?, sender_ips?}` (pelo menos um opcional obrigatório)

**DELETE** — body `{action}` (global ou per-domain)

---

## Auto Migration

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/automigration/setup/` | Sim | MA/DA |
| GET | `/automigration/setup/` | Sim | MA/DA |
| DELETE | `/automigration/setup/` | Sim | MA/DA |
| POST | `/automigration/users/` | **Não** | — |
| GET | `/automigration/users/` | Sim | MA/DA |
| DELETE | `/automigration/users/` | Sim | MA/DA |
| POST | `/automigration/resync/domain/{domain}/` | Sim | MA/DA |
| POST | `/automigration/resync/user/{username}/` | Sim | MA/DA |

**POST /automigration/setup/** — `{domain, imap_serverhost, imap_serverport, imap_session, test_username, test_password}`

**POST /automigration/users/** (sem auth) — `{username, old_password, new_password, recovery_email, language, storagequota_total}`

**DELETE /automigration/setup/** — body `{domain}`

**DELETE /automigration/users/** — body `{username}`

---

## Contacts

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/contacts/` | Sim | MU |
| GET | `/contacts/` | Sim | MU |
| DELETE | `/contacts/` | Sim | MU |

**POST** — `{friendly_name}` → CardDAV `url`

**DELETE** — body `{friendly_name}`

---

## Contacts Sharing

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/contacts/share/` | Sim | MU |
| GET | `/contacts/share/` | Sim | MU |
| PUT | `/contacts/share/` | Sim | MU |
| DELETE | `/contacts/share/` | Sim | MU |

**POST/PUT** — `{friendly_name, recipients: []}`

---

## Calendars

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/calendars/` | Sim | MU |
| GET | `/calendars/` | Sim | MU |
| DELETE | `/calendars/` | Sim | MU |

**POST** — `{friendly_name}`

**DELETE** — body `{friendly_name}`

---

## Calendar Sharing

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/calendars/share/` | Sim | MU |
| GET | `/calendars/share/` | Sim | MU |
| PUT | `/calendars/share/` | Sim | MU |
| DELETE | `/calendars/share/` | Sim | MU |

**POST/PUT** — `{friendly_name, recipients: []}`

---

## Sieve Filters

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/sieve_filters/` | Sim | MU |
| GET | `/sieve_filters/` | Sim | MU |
| PUT | `/sieve_filters/` | Sim | MU |
| DELETE | `/sieve_filters/` | Sim | MU |

**PUT/DELETE** — `filter_position` no body (1–99), não na URL.

**match_type:** `all_rules` | `any_rule` | `all_messages`

**perform_action:** `move` | `copy` | `keep` | `forward` | `keep_and_forward` | `reject` | `discard` | `stop`

Máximo 4 forwards por MailUser.

---

## Vacation Autoresponder

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/vacation_autoreply/` | Sim | MU |
| GET | `/vacation_autoreply/` | Sim | MU |
| PUT | `/vacation_autoreply/` | Sim | MU |
| DELETE | `/vacation_autoreply/` | Sim | MU |

**POST/PUT** — `{subject, body, start_time?, end_time?}` (UNIX segundos)

---

## Webmail Password

| Método | Path | Auth | Perm |
|--------|------|------|------|
| POST | `/webmail/password/{webmail_id}/` | Sim | MU |
| DELETE | `/webmail/password/{webmail_id}/` | Sim | MU |

`webmail_id`: `1` ou `2`. Senha descartável para clientes IMAP/POP/SMTP.

---

## Settings

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/settings/{setting}/` | Sim | MA |
| POST | `/settings/{setting}/` | Sim | MA |
| DELETE | `/settings/{setting}/` | Sim | MA |

**setting:** `system_mailer` | `postfix_relayhost` | `junk_trash_clearing_interval` | `imap_master_password`

GET retorna `204` se nunca configurado.

---

## Statistics

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/stats/mail/` | Sim | MA |
| GET | `/stats/quota/` | Sim | MA/DA |
| GET | `/stats/blocked/sender/` | Sim | MA/DA/MU |

**GET /stats/quota/** — query: `limit`, `start`, `search`, `perm_level` (DA só vê MailUser)

---

## Server

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/server/logs/{service}/` | Sim | MA |
| GET | `/server/load/{report}/` | Sim | MA |
| GET | `/server/disk/usage/` | Sim | MA |
| POST | `/server/dovecot/quota/recalc/` | Sim | MA |
| POST | `/server/dovecot/rebuild/index/` | Sim | MA |
| POST | `/server/postfix/cache/clear/` | Sim | MA |
| POST | `/server/export/radicale/` | Sim | MA |
| GET | `/server/export/radicale/` | Sim | MA |

**service:** `postfix` | `dovecot` | `fail2ban`

**report:** `load_avg` | `cpu` | `memory` | `disk`

Logs: últimas 10000 linhas, `text/html`.

---

## API & System

| Método | Path | Auth | Perm |
|--------|------|------|------|
| GET | `/log/` | Sim | MA/DA/MU |
| GET | `/status/` | Não | — |
| GET | `/system/version/` | Sim | MA |

**GET /log/** — query: `limit` (max 50), `start`, `search`

---

## Índice doc slug → path

| Doc slug | Path real |
|----------|-----------|
| `auth_post` | `POST /auth/` |
| `twofa_post` | `POST /2fa/{username}/` |
| `twofa_verify_post` | `POST /2fa/verify/` |
| `twofa_devicepwd_post` | `POST /2fa/device_password/` |
| `webauthn_registration_get` | `GET /webauthn/registration/options/` |
| `webauthn_registration_post` | `POST /webauthn/registration/verify/` |
| `webauthn_auth_get` | `GET /webauthn/authentication/options/` |
| `webauthn_auth_post` | `POST /webauthn/authentication/verify/` |
| `webauthn_creds_get` | `GET /webauthn/credentials/` |
| `nopwdlogin_get` | `GET /auth/password/disable/{username}/` |
| `account_da_cascade_patch` | `PATCH /accounts/cascade/domainadmin/{u}/{action}/` |
| `account_da_cascade_delete` | `DELETE /accounts/cascade/domainadmin/{u}/` |
| `account_da_cascade_transfer` | `POST /accounts/cascade/ownership/domainadmin/{u}/` |
| `global_antispam_thresh_get` | `GET /antispam/thresholds/global/` |
| `perdomain_antispam_thresh_post` | `POST /antispam/thresholds/domain/{domain}/` |
| `global_wlbl_post` | `POST /antispam/wlbl/global/` |
| `perdomain_wlbl_post` | `POST /antispam/wlbl/domain/{domain}/` |
| `am_setup_post` | `POST /automigration/setup/` |
| `am_user_post` | `POST /automigration/users/` (sem auth) |
| `am_resync_domain_post` | `POST /automigration/resync/domain/{domain}/` |
| `sa_post` | `POST /sender_addresses/` |
| `sieve_filter_put` | `PUT /sieve_filters/` |
| `sieve_filter_delete` | `DELETE /sieve_filters/` |
| `conshare_post` | `POST /contacts/share/` |
| `calshare_post` | `POST /calendars/share/` |
| `wp_post` | `POST /webmail/password/{id}/` |
| `setting_post` | `POST /settings/{setting}/` |
| `server_quota_reclac_post` | `POST /server/dovecot/quota/recalc/` |
| `server_rebuild_index_post` | `POST /server/dovecot/rebuild/index/` |
| `server_cache_clear_post` | `POST /server/postfix/cache/clear/` |
| `export_radicale_post` | `POST /server/export/radicale/` |
| `api_log_get` | `GET /log/` |
| `api_status_get` | `GET /status/` |
| `stats_blocked_senders_get` | `GET /stats/blocked/sender/` |

Lista completa de slugs: ver crawl em `auth_post/` na doc oficial.
