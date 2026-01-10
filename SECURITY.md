# Security Policy

## Supported Versions

We actively support the following versions of The Epiphany Engine with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of The Epiphany Engine seriously. If you discover a security vulnerability, please help us maintain the security of the project by responsibly disclosing it to us.

### How to Report

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to [axiom@i4ANeYe.com](mailto:axiom@i4ANeYe.com)
2. **GitHub Security Advisories**: Use the [GitHub Security Advisory](https://github.com/TheUniversalAxiom/TheEpiphanyEngine/security/advisories/new) feature for private disclosure
3. **Encrypted Communication**: For sensitive vulnerabilities, request our PGP key

### What to Include

Please include the following information in your report:

- **Description**: A clear description of the vulnerability
- **Impact**: What an attacker could potentially do
- **Steps to Reproduce**: Detailed steps to reproduce the vulnerability
- **Proof of Concept**: Code or screenshots demonstrating the issue (if applicable)
- **Suggested Fix**: If you have ideas on how to fix the vulnerability
- **Your Contact**: How we can reach you for follow-up questions

### Example Report

```
Subject: [SECURITY] SQL Injection in simulation endpoint

Description:
The /api/simulate endpoint is vulnerable to SQL injection through the 'preset' parameter.

Impact:
An attacker could potentially execute arbitrary SQL queries and access/modify database contents.

Steps to Reproduce:
1. Send POST request to /api/simulate
2. Include preset parameter: {"preset": "'; DROP TABLE users; --"}
3. Observe SQL error in response

Affected Version: 0.1.0
```

## Response Timeline

We are committed to responding to security reports promptly:

- **Initial Response**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix Development**: Within 30 days (depending on severity)
- **Public Disclosure**: After fix is deployed and users have had time to update

### Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Remote code execution, authentication bypass, data breach | 24 hours |
| **High** | Privilege escalation, SQL injection, XSS | 7 days |
| **Medium** | Information disclosure, DoS | 30 days |
| **Low** | Best practice violations, minor issues | 90 days |

## Security Best Practices

### For Deployment

#### 1. Authentication & Authorization

```bash
# Generate secure API keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate secure JWT secret (minimum 32 characters)
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

**Configuration:**
```bash
API_KEY_ENABLED=true
API_KEY=<generated-secure-key>
JWT_ENABLED=false
JWT_SECRET_KEY=<generated-secure-secret>
JWT_EXPIRATION_MINUTES=60
```

#### 2. HTTPS/TLS

**Always use HTTPS in production:**

```nginx
# Nginx configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable HSTS:**
```bash
ENVIRONMENT=production
HTTPS_ENABLED=true
```

#### 3. CORS Configuration

**Restrict origins to your domains:**
```bash
# Development
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Production
CORS_ORIGINS=https://app.example.com,https://example.com
```

**Never use `*` in production!**

#### 4. Rate Limiting

Default rate limits are configured in the application:
- 100 requests/hour (default)
- 20 requests/minute (simulation endpoint)

To customize:
```python
# In web/api.py
limiter = Limiter(key_func=get_remote_address, default_limits=["200/hour"])
```

#### 5. Environment Variables

**Never commit secrets:**
- All secrets should be in `.env` (which is gitignored)
- Use strong, randomly generated values
- Rotate secrets regularly (every 90 days)

**Required for production:**
```bash
API_KEY=<32+ character random string>
JWT_ENABLED=false
JWT_SECRET_KEY=<32+ character random string>
CORS_ORIGINS=https://your-domain.com
ENVIRONMENT=production
HTTPS_ENABLED=true
LOG_LEVEL=INFO
```

#### 6. Docker Security

**The Dockerfile already implements:**
- ✅ Non-root user (UID 1000)
- ✅ Multi-stage builds
- ✅ Minimal base image (python:3.11-slim)
- ✅ No cache for pip install
- ✅ Health checks

**Additional recommendations:**
```bash
# Scan for vulnerabilities
docker scan epiphany-engine:latest

# Use specific image tags
FROM python:3.11.7-slim  # Instead of :latest

# Limit container resources
docker run --memory="512m" --cpus="1.0" epiphany-engine
```

#### 7. Dependency Security

**Keep dependencies updated:**
```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Use hash-checking for reproducible builds
pip-compile --generate-hashes requirements.in
```

**GitHub Actions already runs:**
- `pip-audit` on every PR
- `safety check` on every PR

#### 8. Logging & Monitoring

**Enable structured logging:**
```bash
LOG_LEVEL=INFO  # Use INFO or WARNING in production
```

**Monitor for security events:**
- Failed authentication attempts
- Rate limit exceeded
- Invalid input patterns
- Unusual request patterns

**Log files should:**
- Never contain secrets (API keys, passwords, tokens)
- Be rotated regularly
- Be secured with proper file permissions

#### 9. Input Validation

**The application validates:**
- All numeric inputs (bounds checking)
- Parameter types (Pydantic models)
- Steps limit (max 250)
- Preset names (allowed values)

**Additional recommendations:**
- Sanitize log inputs
- Validate file uploads (if added)
- Check content-type headers

#### 10. Regular Security Audits

**Recommended schedule:**
- **Weekly**: Dependency vulnerability scans
- **Monthly**: Review authentication logs
- **Quarterly**: Security configuration review
- **Yearly**: Third-party security audit

## Security Features

### Currently Implemented ✅

- **Authentication**: Optional API key + JWT
- **Rate Limiting**: Per-IP throttling with slowapi
- **Input Validation**: Pydantic models with strict bounds
- **Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- **CORS Protection**: Configurable allowed origins
- **Non-root Container**: Docker runs as UID 1000
- **Structured Logging**: JSON logs for security monitoring
- **Dependency Scanning**: pip-audit + safety in CI/CD
- **Password Hashing**: Bcrypt via passlib

### Planned Enhancements 📋

- [ ] Request signing for API authentication
- [ ] OAuth2 support for user authentication
- [ ] API key rotation mechanism
- [ ] Audit logging for sensitive operations
- [ ] Intrusion detection/prevention
- [ ] Secrets management integration (Vault)
- [ ] Multi-factor authentication (MFA)

## Known Security Limitations

### Current Limitations

1. **No Persistent Storage**: All data is in-memory during request lifecycle
   - **Impact**: No audit trail persistence
   - **Mitigation**: External logging/monitoring recommended

2. **Dynamic Extension Loading**: Extensions loaded via importlib
   - **Impact**: Could execute untrusted code
   - **Mitigation**: Only load extensions from trusted sources
   - **Future**: Add extension signature verification

3. **Single-layer Authentication**: API key OR JWT (not both)
   - **Impact**: No defense in depth
   - **Mitigation**: Enable authentication in production
   - **Future**: Implement MFA

4. **No Request Signing**: API requests not cryptographically signed
   - **Impact**: Vulnerable to replay attacks (mitigated by rate limiting)
   - **Mitigation**: Use HTTPS + short-lived JWT tokens
   - **Future**: Implement request signing

## Compliance

### Data Protection

The Epiphany Engine:
- Does not store personal data by default
- Does not track users
- Processes simulation requests in-memory only
- Logs should be configured to exclude sensitive data

### GDPR Compliance

For GDPR compliance:
- No personal data is collected without configuration
- All processing is in-memory and temporary
- Logs should be configured to exclude PII
- No cookies are used

### HIPAA/PCI Considerations

**This application is NOT designed for HIPAA or PCI compliance out-of-the-box.**

If you need to handle:
- Protected Health Information (PHI)
- Payment Card Information (PCI)

You must:
- Implement encryption at rest
- Add comprehensive audit logging
- Implement access controls
- Undergo compliance certification
- Add data retention policies

## Security Contact

For security-related questions or concerns:

- **Security Issues**: Use GitHub Security Advisories (preferred)
- **General Questions**: Open a GitHub Discussion
- **Private Disclosure**: [axiom@i4ANeYe.com](mailto:axiom@i4ANeYe.com)

## Acknowledgments

We appreciate security researchers who help keep The Epiphany Engine secure. Security researchers who responsibly disclose vulnerabilities will be:

- Acknowledged in release notes (unless they prefer to remain anonymous)
- Listed in our security hall of fame
- Provided with swag (t-shirts, stickers) for significant findings

## Updates to This Policy

This security policy may be updated from time to time. Please check back regularly for updates.

**Last Updated**: 2026-01-10
**Version**: 1.0

---

Thank you for helping keep The Epiphany Engine and our users safe! 🔒
