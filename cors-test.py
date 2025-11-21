#!/usr/bin/env python3

import requests
import sys
from urllib.parse import urljoin

def tanya_domain():
    domain = input('Masukkan domain/sub-domain (contoh: http://api.example.com): ').strip()
    return domain

def tanya_path():
    paths = input('Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): ').strip()
    list_path = [p.strip() for p in paths.split(',') if p.strip()]
    return list_path

def uji_cors(url, asal_origin):
    print('\n' + '='*60)
    print(f'Testing CORS untuk: {url}')
    print('='*60)
    
    try:
        header = {
            'Origin': asal_origin,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type',
        }
        
        respon = requests.options(url, headers=header, timeout=5, verify=False)
        
        print(f'\nStatus Code: {respon.status_code} {respon.reason}')
        print('\nCORS Headers:')
        print(f'  Access-Control-Allow-Origin: {respon.headers.get("Access-Control-Allow-Origin", "NOT SET")}')
        print(f'  Access-Control-Allow-Methods: {respon.headers.get("Access-Control-Allow-Methods", "NOT SET")}')
        print(f'  Access-Control-Allow-Headers: {respon.headers.get("Access-Control-Allow-Headers", "NOT SET")}')
        print(f'  Access-Control-Max-Age: {respon.headers.get("Access-Control-Max-Age", "NOT SET")}')
        print(f'  Access-Control-Allow-Credentials: {respon.headers.get("Access-Control-Allow-Credentials", "NOT SET")}')
        
        print('\nSemua Headers:')
        for nama_header, nilai in respon.headers.items():
            print(f'  {nama_header}: {nilai}')
        
        print('\nAnalisis CORS:')
        izin_origin = respon.headers.get('Access-Control-Allow-Origin')
        if izin_origin == '*':
            print('  ✓ CORS diizinkan untuk SEMUA origin')
        elif izin_origin:
            print(f'  ✓ CORS diizinkan untuk origin spesifik: {izin_origin}')
        else:
            print('  ✗ CORS headers tidak ditemukan - CORS mungkin tidak dikonfigurasi')
            
    except requests.exceptions.RequestException as e:
        print(f'\n❌ Error testing {url}:')
        print(f'   {str(e)}')
    except Exception as e:
        print(f'\n❌ Error tidak terduga:')
        print(f'   {str(e)}')

def uji_permintaan_sebenarnya(url, asal_origin):
    print('\n' + '-'*60)
    print(f'Testing GET request ke: {url}')
    print('-'*60)
    
    try:
        header = {
            'Origin': asal_origin,
        }
        
        respon = requests.get(url, headers=header, timeout=5, verify=False)
        
        print(f'\nStatus Code: {respon.status_code}')
        print(f'Response Size: {len(respon.content)} bytes')
        print(f'Content-Type: {respon.headers.get("Content-Type", "NOT SET")}')
        print(f'Access-Control-Allow-Origin: {respon.headers.get("Access-Control-Allow-Origin", "NOT SET")}')
        
    except requests.exceptions.RequestException as e:
        print(f'\n❌ Error: {str(e)}')

def main():
    asal_origin = tanya_domain()
    
    if not asal_origin:
        print('Domain tidak boleh kosong!')
        return
    
    list_path = tanya_path()
    
    if not list_path:
        print('Minimal satu path harus diinput!')
        return
    
    print(f'\nMenggunakan domain: {asal_origin}')
    print(f'URL paths yang akan di-test: {", ".join(list_path)}')
    print('='*60)
    
    requests.packages.urllib3.disable_warnings()
    
    titik_akhir = [
        asal_origin,
        *[f'{asal_origin}{path}' for path in list_path]
    ]
    
    for endpoint in titik_akhir:
        uji_cors(endpoint, asal_origin)
        uji_permintaan_sebenarnya(endpoint, asal_origin)
    
    print('\n' + '='*60)
    print('CORS Testing Selesai')
    print('='*60 + '\n')

if __name__ == '__main__':
    main()
