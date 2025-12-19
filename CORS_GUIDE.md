# CORS Configuration Guide

## 🌐 Understanding CORS (Cross-Origin Resource Sharing)

CORS allows your backend (on one domain) to accept requests from your frontend (on a different domain).

## 🔒 Current Configuration

### Production-Safe CORS Logic

```python
if FLASK_ENV == 'production' AND CORS_ORIGINS is set AND != '*':
    ✅ Allow specific origins only (secure)
else:
    ⚠️  Allow all origins (development only)
```

### Key Security Features

1. **Environment-based**: Uses `FLASK_ENV` to determine mode
2. **Explicit production check**: Won't accidentally allow `*` in production
3. **No credentials**: `supports_credentials=False` (safer, no cookies)
4. **Extended headers**: Supports common browser headers

## 📋 Configuration by Environment

### Local Development

**Environment Variables:**
```bash
FLASK_ENV=development
# CORS_ORIGINS not set, or set to "*"
```

**Behavior:**
- ✅ Allows ALL origins (`*`)
- ✅ Perfect for local testing
- ✅ Frontend can be on any port
- ⚠️  NOT safe for production

**Use Case:**
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5001`
- Works without CORS errors

---

### Docker Development

**Environment Variables:**
```bash
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000
```

**Behavior:**
- ✅ Allows all origins (development mode)
- ✅ Same as local development
- ⚠️  `CORS_ORIGINS` setting ignored in dev mode

---

### Production (Render + Vercel)

**Environment Variables on Render:**
```bash
FLASK_ENV=production
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app
```

**Behavior:**
- 🔒 Only allows `https://ai-interviewer-reactjs.vercel.app`
- 🔒 All other origins are blocked
- ✅ Secure for production
- ✅ Prevents unauthorized API access

**Multiple Origins:**
```bash
CORS_ORIGINS=https://frontend1.com,https://frontend2.com,https://frontend3.com
```

---

## 🚨 Common CORS Errors & Fixes

### Error 1: "No 'Access-Control-Allow-Origin' header is present"

**Symptoms:**
```
Access to fetch at 'https://backend.com/api' from origin 'https://frontend.com' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.
```

**Causes:**
1. Backend `CORS_ORIGINS` doesn't include your frontend URL
2. Frontend URL has typo (trailing slash, http vs https)
3. Backend not running or crashed

**Fix:**
```bash
# On Render backend, set exact frontend URL:
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app

# NOT: https://ai-interviewer-reactjs.vercel.app/  (no trailing slash)
# NOT: http://... (use https)
```

---

### Error 2: "The 'Access-Control-Allow-Origin' header contains multiple values"

**Symptoms:**
```
Access-Control-Allow-Origin header contains multiple values 
'https://frontend.com, *', but only one is allowed.
```

**Cause:**
- CORS configured twice (middleware + manual headers)
- Our current config doesn't have this issue ✅

**Prevention:**
- Use Flask-CORS only (no manual `after_request` handlers)
- We removed the redundant handler in the latest update ✅

---

### Error 3: "Credentials flag is 'true', but the 'Access-Control-Allow-Origin' is '*'"

**Symptoms:**
```
Access to fetch has been blocked by CORS policy: 
The value of the 'Access-Control-Allow-Credentials' header must not be 'true' 
when the 'Access-Control-Allow-Origin' value is '*'.
```

**Cause:**
- `supports_credentials=True` with `origins="*"` (browser rejects this)

**Our Fix:**
```python
supports_credentials=False  # Always False, we don't use cookies ✅
```

---

### Error 4: OPTIONS Preflight Fails (404)

**Symptoms:**
```
OPTIONS /api/interview/create 404 (Not Found)
```

**Cause:**
- Route doesn't handle OPTIONS method
- CORS middleware not applied to route

**Our Fix:**
```python
# Flask-CORS automatically handles OPTIONS ✅
# Explicit OPTIONS in routes where needed ✅
methods=['POST', 'OPTIONS']
```

---

## 🔍 Testing CORS

### Test 1: Check CORS Headers

```bash
# Test OPTIONS preflight
curl -X OPTIONS \
  -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v \
  https://ai-interviewer-reactjs.onrender.com/api/interview/create

# Look for:
# Access-Control-Allow-Origin: https://ai-interviewer-reactjs.vercel.app
# Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization, Accept
```

### Test 2: Check Actual Request

```bash
# Test POST with Origin header
curl -X POST \
  -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
  -H "Content-Type: application/json" \
  -d '{"technology":"Python","position":"Developer"}' \
  -v \
  https://ai-interviewer-reactjs.onrender.com/api/interview/create

# Should return data + CORS headers
```

### Test 3: Wrong Origin (Should Fail)

```bash
# Test with unauthorized origin
curl -X OPTIONS \
  -H "Origin: https://malicious-site.com" \
  -H "Access-Control-Request-Method: POST" \
  -v \
  https://ai-interviewer-reactjs.onrender.com/api/interview/create

# Should NOT have Access-Control-Allow-Origin header
# Or should not match the malicious origin
```

---

## 📊 CORS Configuration Matrix

| Environment | FLASK_ENV | CORS_ORIGINS | Actual Behavior | Security |
|-------------|-----------|--------------|-----------------|----------|
| Local Dev | development | (not set) | Allow `*` | Low (dev only) |
| Local Dev | development | `*` | Allow `*` | Low (dev only) |
| Local Dev | development | `https://specific.com` | Allow `*` (ignored) | Low (dev only) |
| Docker Dev | development | anything | Allow `*` | Low (dev only) |
| Production | production | (not set) | Allow `*` ⚠️ | **Unsafe!** |
| Production | production | `*` | Allow `*` ⚠️ | **Unsafe!** |
| Production | production | `https://frontend.com` | Allow only that origin ✅ | **Secure!** |
| Production | production | `https://a.com,https://b.com` | Allow both ✅ | **Secure!** |

## ✅ Production Deployment Checklist

### Backend (Render)

- [ ] `FLASK_ENV=production` (set in environment variables)
- [ ] `CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app` (exact URL, no trailing slash)
- [ ] `FLASK_DEBUG=False`
- [ ] Verify backend logs show: `🔒 CORS (Production): Allowing specific origins:`

### Frontend (Vercel)

- [ ] `VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api`
- [ ] Deployed and accessible
- [ ] Backend URL is HTTPS (not HTTP)

### Testing

- [ ] Open frontend in browser
- [ ] Open DevTools → Network tab
- [ ] Try creating an interview
- [ ] Verify OPTIONS preflight returns 200
- [ ] Verify POST request succeeds
- [ ] No CORS errors in console

---

## 🎯 Best Practices

### DO ✅

1. **Use FLASK_ENV to control CORS mode**
   ```bash
   FLASK_ENV=production  # Enables strict CORS
   ```

2. **Set specific origins in production**
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Use HTTPS in production**
   ```bash
   CORS_ORIGINS=https://frontend.com  # Not http://
   ```

4. **Test CORS before deploying**
   ```bash
   curl -X OPTIONS -H "Origin: https://..." ...
   ```

5. **Monitor backend logs**
   ```
   Look for: 🔒 CORS (Production): Allowing specific origins: [...]
   ```

### DON'T ❌

1. **Don't use `*` in production**
   ```bash
   CORS_ORIGINS=*  # Allows anyone to call your API!
   ```

2. **Don't mix HTTP and HTTPS**
   ```bash
   # If frontend is HTTPS, backend must be HTTPS
   CORS_ORIGINS=http://frontend.com  # Won't work!
   ```

3. **Don't add trailing slashes**
   ```bash
   CORS_ORIGINS=https://frontend.com/  # May not match!
   ```

4. **Don't forget to set FLASK_ENV**
   ```bash
   # Without FLASK_ENV=production, it defaults to development mode
   ```

5. **Don't use `supports_credentials` unnecessarily**
   ```python
   # We don't use cookies/auth headers, so keep it False
   supports_credentials=False
   ```

---

## 🆘 Debugging Steps

If you're getting CORS errors in production:

### Step 1: Verify Backend Environment

```bash
# Visit: https://ai-interviewer-reactjs.onrender.com/api/test

# Check response for:
{
  "cors": {
    "mode": "specific origins: ['https://ai-interviewer-reactjs.vercel.app']",
    ...
  }
}
```

### Step 2: Check Render Logs

Go to Render Dashboard → Your Service → Logs

Look for startup message:
```
🔒 CORS (Production): Allowing specific origins: ['https://...']
```

### Step 3: Test with cURL

```bash
./test_cors.sh
# or
curl -X OPTIONS -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
  https://ai-interviewer-reactjs.onrender.com/api/interview/create -v
```

### Step 4: Verify Environment Variables

Render Dashboard → Environment Tab

Ensure:
- `FLASK_ENV=production`
- `CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app` (no trailing slash!)

### Step 5: Force Redeploy

Sometimes environment changes don't apply:
1. Go to Render Dashboard
2. Click "Manual Deploy" → "Clear build cache & deploy"

---

## 📚 Additional Resources

- **Flask-CORS Docs**: https://flask-cors.readthedocs.io/
- **MDN CORS Guide**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- **Test CORS**: https://www.test-cors.org/

## 🎓 Understanding the Code

```python
CORS(app,
     resources={
         r"/*": {  # Apply to all routes
             "origins": ["https://frontend.com"],  # Only allow this origin
             "methods": ["GET", "POST", ...],      # Allowed HTTP methods
             "allow_headers": ["Content-Type"],     # Allowed request headers
             "expose_headers": ["Content-Type"],    # Headers browser can access
             "supports_credentials": False,         # No cookies/auth
             "max_age": 3600                       # Cache preflight for 1 hour
         }
     })
```

---

**Last Updated**: December 2025  
**Version**: 2.0 (Production-Safe)

