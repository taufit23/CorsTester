#!/usr/bin/env python3

import subprocess
import json
import re
import sys
from typing import Dict, Tuple

class PengujianCORSdenganCurl:
    def __init__(self, asal: str):
        self.asal = asal
    
    def curl_preflight(self, url: str, metode: str = 'GET') -> Tuple[int, str]:
        cmd = [
            'curl',
            '-s',
            '-i',
            '-X', 'OPTIONS',
            url,
            '-H', f'Origin: {self.asal}',
            '-H', f'Access-Control-Request-Method: {metode}',
            '-H', 'Access-Control-Request-Headers: Content-Type',
        ]
        
        try:
            hasil = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return 0, hasil.stdout + hasil.stderr
        except subprocess.TimeoutExpired:
            return -1, 'Request timeout'
        except Exception as e:
            return -1, f'Error: {str(e)}'
    
    def curl_permintaan(self, url: str, metode: str = 'GET') -> Tuple[int, str]:
        cmd = [
            'curl',
            '-s',
            '-i',
            '-X', metode,
            url,
            '-H', f'Origin: {self.asal}',
            '-H', 'Content-Type: application/json',
        ]
        
        try:
            hasil = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return 0, hasil.stdout + hasil.stderr
        except subprocess.TimeoutExpired:
            return -1, 'Request timeout'
        except Exception as e:
            return -1, f'Error: {str(e)}'
    
    def parse_header(self, teks_respon: str) -> Tuple[str, Dict]:
        baris = teks_respon.split('\n')
        header = {}
        baris_status = ''
        
        for i, baris_item in enumerate(baris):
            baris_item = baris_item.strip()
            if i == 0:
                baris_status = baris_item
            elif ':' in baris_item:
                kunci, nilai = baris_item.split(':', 1)
                header[kunci.strip().lower()] = nilai.strip()
            elif not baris_item:
                break
        
        return baris_status, header
    
    def cetak_hasil_uji(self, url: str, jenis_permintaan: str, teks_respon: str):
        baris_status, header = self.parse_header(teks_respon)
        
        print(f'\n{"="*70}')
        print(f'URL: {url}')
        print(f'Jenis: {jenis_permintaan}')
        print(f'Status: {baris_status}')
        print(f'{"="*70}')
        
        header_cors = {k: v for k, v in header.items() if 'access-control' in k}
        
        if header_cors:
            print('\nCORS Headers:')
            for kunci, nilai in header_cors.items():
                print(f'  {kunci}: {nilai}')
        else:
            print('\nTidak ada CORS headers')
        
        izin_origin = header.get('access-control-allow-origin')
        if izin_origin:
            if izin_origin == '*':
                print('\n✓ CORS diizinkan untuk SEMUA origin')
            else:
                print(f'\n✓ CORS diizinkan untuk: {izin_origin}')
        else:
            print('\n✗ CORS tidak dikonfigurasi atau headers hilang')

def main():
    asal_origin = input('Masukkan domain/sub-domain (contoh: http://api.example.com): ').strip()
    
    if not asal_origin:
        print('Domain tidak boleh kosong!')
        return
    
    paths = input('Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): ').strip()
    list_path = [p.strip() for p in paths.split(',') if p.strip()]
    
    if not list_path:
        print('Minimal satu path harus diinput!')
        return
    
    print('Pengujian CORS dengan cURL Wrapper')
    print(f'Target: {asal_origin}')
    print(f'URL paths: {", ".join(list_path)}')
    print('='*70)
    
    pengujian = PengujianCORSdenganCurl(asal_origin)
    
    titik_akhir = [
        asal_origin,
        *[f'{asal_origin}{path}' for path in list_path]
    ]
    
    for endpoint in titik_akhir:
        print(f'\n\nTesting: {endpoint}')
        print('='*70)
        
        status, respon = pengujian.curl_preflight(endpoint)
        if status == 0:
            pengujian.cetak_hasil_uji(endpoint, 'OPTIONS (Preflight)', respon)
        else:
            print(f'Error: {respon}')
        
        status, respon = pengujian.curl_permintaan(endpoint, 'GET')
        if status == 0:
            pengujian.cetak_hasil_uji(endpoint, 'Permintaan GET', respon)
        else:
            print(f'Error: {respon}')
    
    print('\n' + '='*70)
    print('Pengujian Selesai')
    print('='*70)

if __name__ == '__main__':
    main()
