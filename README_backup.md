# CORS Testing Scripts for http://begl.saakti.id

Comprehensive collection of CORS (Cross-Origin Resource Sharing) testing tools for the domain `http://begl.saakti.id`.

## 📋 Scripts Included

### 1. **cors-test.js** - JavaScript/Node.js

Simple CORS testing using Fetch API

- Tests OPTIONS preflight requests
- Checks CORS response headers
- Tests multiple endpoints
- **Run with:** `node cors-test.js`

### 2. **cors-test.py** - Python

Basic CORS testing with requests library

- Tests preflight (OPTIONS) and actual requests
- Displays all response headers
- **Requirements:** `pip install requests`
- **Run with:** `python cors-test.py`

### 3. **cors-advanced.py** - Python Advanced

Comprehensive CORS analysis with detailed reporting

- Multiple HTTP methods testing (GET, POST, PUT, DELETE)
- CORS configuration analysis
- Security issue detection
- Recommendations for improvements
- **Requirements:** `pip install requests`
- **Run with:** `python cors-advanced.py`

### 4. **cors-test.sh** - Bash/Linux

Shell script for CORS testing using curl

- Color-coded output for easy reading
- Tests preflight and simple requests
- Cross-platform compatible
- **Run with:** `bash cors-test.sh`
- **Make executable:** `chmod +x cors-test.sh`

### 5. **cors-test.bat** - Windows Batch

Batch script for Windows systems

- Uses curl for HTTP requests
- Tests multiple endpoints
- **Run with:** Double-click or `cors-test.bat` in command prompt

### 6. **cors-tester.html** - Interactive Web UI

Beautiful browser-based CORS testing tool

- User-friendly interface
- Test custom URLs
- Choose HTTP methods
- View detailed response headers
- Real-time CORS analysis
- **Run with:** Open in any web browser

## 🚀 Quick Start

### Python (Recommended for detailed analysis)

```bash
pip install requests
python cors-advanced.py
```

### JavaScript/Node.js

```bash
node cors-test.js
```

### Bash/Linux/macOS

```bash
bash cors-test.sh
```

### Windows

```cmd
cors-test.bat
```

### Web Browser

Simply open `cors-tester.html` in your browser

## 📊 What Gets Tested

Each script tests the following:

1. **CORS Preflight Request (OPTIONS)**
   - Checks if server responds to OPTIONS requests
   - Validates CORS headers presence
2. **CORS Response Headers**

   - `Access-Control-Allow-Origin`
   - `Access-Control-Allow-Methods`
   - `Access-Control-Allow-Headers`
   - `Access-Control-Max-Age`
   - `Access-Control-Allow-Credentials`

3. **Multiple Endpoints**

   - `http://begl.saakti.id`
   - `http://begl.saakti.id/api`
   - `http://begl.saakti.id/api/data`

4. **Security Analysis** (in advanced-py)
   - Checks for overly permissive CORS settings
   - Validates credentials + wildcard origin combination
   - Provides security recommendations

## 🔍 CORS Headers Explained

| Header                             | Purpose                                            |
| ---------------------------------- | -------------------------------------------------- |
| `Access-Control-Allow-Origin`      | Specifies which origins can access the resource    |
| `Access-Control-Allow-Methods`     | Specifies which HTTP methods are allowed           |
| `Access-Control-Allow-Headers`     | Specifies which headers clients can use            |
| `Access-Control-Max-Age`           | How long preflight results can be cached (seconds) |
| `Access-Control-Allow-Credentials` | Whether credentials (cookies, auth) are allowed    |

## ✅ Common CORS Configurations

### Permissive (Allow All)

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

### Restrictive (Specific Domain)

```
Access-Control-Allow-Origin: http://example.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Content-Type, Authorization
```

### Credentials Enabled

```
Access-Control-Allow-Origin: http://example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST
```

## 🛡️ Security Notes

- ⚠️ **Avoid** using `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
- 🔒 Always specify exact origins when possible
- 📝 Limit allowed methods and headers to what's necessary
- 🕐 Set reasonable `Max-Age` values for preflight caching

## 💡 Troubleshooting

### Getting connection refused?

- Check if the server is running
- Verify the domain/IP is correct
- Check network connectivity

### No CORS headers found?

- CORS might not be configured
- Server might require authentication
- Check firewall/proxy settings

### CORS preflight fails but simple GET works?

- Server might not handle OPTIONS requests
- Check server's HTTP verb support
- Review server's CORS middleware configuration

## 📝 Example Output

```
============================================================
Testing CORS for: http://begl.saakti.id
============================================================

Status Code: 200 OK

CORS Headers:
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  Access-Control-Allow-Headers: Content-Type, Authorization
  Access-Control-Max-Age: 86400

Analysis:
  ✓ CORS enabled for ALL origins
```

## 🔧 Customization

### Add More Endpoints

Edit the `endpoints` array in any script:

**Python:**

```python
endpoints = [
    'http://begl.saakti.id',
    'http://begl.saakti.id/custom-api',
    # Add more...
]
```

### Test with Custom Headers

Edit the request headers in scripts:

```python
headers = {
    'Origin': TARGET_ORIGIN,
    'Access-Control-Request-Headers': 'Authorization, X-Custom-Header',
}
```

## 📚 Resources

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [CORS Tester Tool](https://www.test-cors.org/)
- [HTTP Headers Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

---

**Created for:** begl.saakti.id CORS Testing
**Version:** 1.0
**Last Updated:** 2024
