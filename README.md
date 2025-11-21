# CORS Tester untuk http://begl.saakti.id

Kumpulan script untuk testing CORS (Cross-Origin Resource Sharing) pada domain `http://begl.saakti.id`.

---

## 📋 Daftar Script

| Script             | Bahasa             | Cara Menjalankan          |
| ------------------ | ------------------ | ------------------------- |
| `cors-test.js`     | JavaScript/Node.js | `node cors-test.js`       |
| `cors-test.py`     | Python             | `python cors-test.py`     |
| `cors-advanced.py` | Python (Advanced)  | `python cors-advanced.py` |
| `cors-test.sh`     | Bash/Linux/macOS   | `bash cors-test.sh`       |
| `cors-test.bat`    | Windows CMD        | `cors-test.bat`           |
| `cors-tester.html` | Browser            | Buka di browser           |

---

## 🚀 Cara Penggunaan

Setiap script akan menanyakan 2 input:

1. **Domain/Sub-domain**: Base URL yang ingin di-test (contoh: `http://api.example.com`)
2. **URL Paths**: Endpoint paths yang ingin di-test, dipisahkan koma (contoh: `/api,/api/data,/v1/users`)

### Python (Rekomendasi)

```bash
pip install requests
python cors-advanced.py

# Akan diminta input:
# Masukkan domain/sub-domain (contoh: http://api.example.com): http://begl.saakti.id
# Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): /api,/api/data,/health
```

### JavaScript/Node.js

```bash
node cors-test.js

# Akan diminta input:
# Masukkan domain/sub-domain (contoh: http://api.example.com):
# Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users):
```

### Bash/Linux/macOS

```bash
bash cors-test.sh
chmod +x cors-test.sh  # Buat executable

# Akan diminta input untuk domain dan URL paths
```

### Windows

```cmd
cors-test.bat

# Akan diminta input untuk domain dan URL paths
```

### Browser (Web UI)

Buka file `cors-tester.html` dengan browser - tidak perlu command line, langsung input di form

---

## 📊 Hasil yang Diharapkan

Setiap script akan menampilkan:

1. **Status HTTP Response**

   - Status code dan message

2. **CORS Headers yang Ditemukan**

   - `Access-Control-Allow-Origin`
   - `Access-Control-Allow-Methods`
   - `Access-Control-Allow-Headers`
   - `Access-Control-Max-Age`
   - `Access-Control-Allow-Credentials`

3. **Analisis Keamanan**
   - ✓ CORS dikonfigurasi atau tidak
   - ✓ Apakah allow semua origin
   - ✓ Apakah credentials diizinkan

### Contoh Output

```
======================================================================
Tool Pengujian CORS Advanced
Asal Origin: http://begl.saakti.id
URL paths: /api, /api/data, /health
======================================================================


========================================================================
Testing: http://begl.saakti.id
========================================================================

[PERMINTAAN PREFLIGHT]

URL: http://begl.saakti.id
Request Type: OPTIONS (preflight for GET)
Status Code: 204

CORS Headers Found:
  (None)

Analysis:
  CORS Configured: No
  Allow All Origins: No
  Allow Credentials: No

⚠️ Issues:
  ✗ CORS headers not found - may require credentials or be disabled
```

---

## 🔍 Header CORS Dijelaskan

| Header                             | Fungsi                                     |
| ---------------------------------- | ------------------------------------------ |
| `Access-Control-Allow-Origin`      | Menentukan origin mana yang boleh akses    |
| `Access-Control-Allow-Methods`     | HTTP method mana saja yang diizinkan       |
| `Access-Control-Allow-Headers`     | Header mana saja yang client boleh gunakan |
| `Access-Control-Max-Age`           | Berapa lama preflight cache (detik)        |
| `Access-Control-Allow-Credentials` | Apakah credentials (cookies) diizinkan     |

---

## 🔧 Konfigurasi CORS

### Permisif (Allow Semua)

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
```

### Terbatas (Spesifik Domain)

```
Access-Control-Allow-Origin: http://example.com
Access-Control-Allow-Methods: GET, POST
```

### Dengan Credentials

```
Access-Control-Allow-Origin: http://example.com
Access-Control-Allow-Credentials: true
```

---

## ⚠️ Catatan Penting

- Hindari kombinasi `Allow-Origin: *` dengan `Allow-Credentials: true`
- Selalu spesifikasi origin yang diperlukan
- Batasi methods dan headers sesuai kebutuhan

---

**Dibuat untuk:** Testing CORS untuk berbagai BE domains  
**Versi:** 3.0 (Dynamic URL Paths)  
**Terakhir diupdate:** 2025
