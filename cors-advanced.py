#!/usr/bin/env python3

import requests
import json
from typing import Dict, Tuple
from urllib.parse import urlparse
import sys

class PengujianCORS:
    def __init__(self, asal):
        self.asal = asal
        requests.packages.urllib3.disable_warnings()
    
    def permintaan_preflight(self, url: str, metode: str = 'GET', header: list = None) -> Tuple[int, Dict]:
        if header is None:
            header = ['Content-Type']
        
        header_permintaan = {
            'Origin': self.asal,
            'Access-Control-Request-Method': metode,
            'Access-Control-Request-Headers': ', '.join(header),
        }
        
        try:
            respon = requests.options(url, headers=header_permintaan, timeout=5, verify=False)
            return respon.status_code, dict(respon.headers)
        except Exception as e:
            return None, {'error': str(e)}
    
    def permintaan_sederhana(self, url: str, metode: str = 'GET', data: dict = None) -> Tuple[int, Dict]:
        header_permintaan = {
            'Origin': self.asal,
        }
        
        try:
            if metode == 'GET':
                respon = requests.get(url, headers=header_permintaan, timeout=5, verify=False)
            elif metode == 'POST':
                respon = requests.post(url, headers=header_permintaan, json=data, timeout=5, verify=False)
            elif metode == 'HEAD':
                respon = requests.head(url, headers=header_permintaan, timeout=5, verify=False)
            else:
                respon = requests.request(metode, url, headers=header_permintaan, json=data, timeout=5, verify=False)
            
            return respon.status_code, dict(respon.headers)
        except Exception as e:
            return None, {'error': str(e)}
    
    def ekstrak_header_cors(self, header: Dict) -> Dict:
        header_cors = {}
        kunci_cors = [
            'access-control-allow-origin',
            'access-control-allow-credentials',
            'access-control-allow-methods',
            'access-control-allow-headers',
            'access-control-max-age',
            'access-control-expose-headers',
            'access-control-request-method',
            'access-control-request-headers',
        ]
        
        for kunci in kunci_cors:
            if kunci in header:
                header_cors[kunci] = header[kunci]
        
        return header_cors
    
    def analisis_cors(self, header: Dict) -> Dict:
        header_cors = self.ekstrak_header_cors(header)
        analisis = {
            'cors_dikonfigurasi': False,
            'izin_semua_origin': False,
            'izin_kredensial': False,
            'metode_diizinkan': [],
            'header_diizinkan': [],
            'max_age': None,
            'masalah': [],
            'rekomendasi': []
        }
        
        izin_origin = header_cors.get('access-control-allow-origin')
        
        if izin_origin:
            analisis['cors_dikonfigurasi'] = True
            
            if izin_origin == '*':
                analisis['izin_semua_origin'] = True
                if header_cors.get('access-control-allow-credentials') == 'true':
                    analisis['masalah'].append('⚠️  CORS allow semua origins AND credentials (potensi masalah keamanan)')
            else:
                analisis['rekomendasi'].append(f'✓ CORS dibatasi untuk: {izin_origin}')
        else:
            analisis['masalah'].append('✗ CORS headers tidak ditemukan - mungkin memerlukan kredensial atau dinonaktifkan')
        
        if header_cors.get('access-control-allow-credentials') == 'true':
            analisis['izin_kredensial'] = True
        
        metode = header_cors.get('access-control-allow-methods', '')
        if metode:
            analisis['metode_diizinkan'] = [m.strip() for m in metode.split(',')]
        
        header_izin = header_cors.get('access-control-allow-headers', '')
        if header_izin:
            analisis['header_diizinkan'] = [h.strip() for h in header_izin.split(',')]
        
        max_age = header_cors.get('access-control-max-age')
        if max_age:
            analisis['max_age'] = int(max_age)
        
        return analisis, header_cors
    
    def cetak_hasil(self, url: str, jenis_permintaan: str, status: int, analisis: Dict, header_cors: Dict):
        print(f'\n{"-"*70}')
        print(f'URL: {url}')
        print(f'Jenis Permintaan: {jenis_permintaan}')
        print(f'Status Code: {status}' if status else f'Status: ERROR')
        print(f'{"-"*70}')
        
        if 'error' in header_cors:
            print(f'❌ Error: {header_cors["error"]}')
            return
        
        print('\nCORS Headers Ditemukan:')
        if header_cors:
            for kunci, nilai in header_cors.items():
                print(f'  {kunci}: {nilai}')
        else:
            print('  (Tidak ada)')
        
        print('\nAnalisis:')
        print(f'  CORS Dikonfigurasi: {"Ya" if analisis["cors_dikonfigurasi"] else "Tidak"}')
        print(f'  Izin Semua Origin: {"Ya (*)" if analisis["izin_semua_origin"] else "Tidak"}')
        print(f'  Izin Kredensial: {"Ya" if analisis["izin_kredensial"] else "Tidak"}')
        
        if analisis['metode_diizinkan']:
            print(f'  Metode Diizinkan: {", ".join(analisis["metode_diizinkan"])}')
        
        if analisis['header_diizinkan']:
            print(f'  Header Diizinkan: {", ".join(analisis["header_diizinkan"])}')
        
        if analisis['max_age']:
            print(f'  Preflight Cache (Max-Age): {analisis["max_age"]} detik')
        
        if analisis['masalah']:
            print('\n⚠️  Masalah:')
            for masalah in analisis['masalah']:
                print(f'  {masalah}')
        
        if analisis['rekomendasi']:
            print('\n✓ Rekomendasi:')
            for rekomendasi in analisis['rekomendasi']:
                print(f'  {rekomendasi}')

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
    
    print('='*70)
    print('Tool Pengujian CORS Advanced')
    print(f'Asal Origin: {asal_origin}')
    print(f'URL paths: {", ".join(list_path)}')
    print('='*70)
    
    pengujian = PengujianCORS(asal_origin)
    
    titik_akhir = [
        asal_origin,
        *[f'{asal_origin}{path}' for path in list_path]
    ]
    
    metode_uji = ['GET', 'POST', 'PUT', 'DELETE']
    
    for endpoint in titik_akhir:
        print(f'\n\n{"="*70}')
        print(f'Testing: {endpoint}')
        print('='*70)
        
        print('\n[PERMINTAAN PREFLIGHT]')
        for metode in metode_uji:
            status, header = pengujian.permintaan_preflight(endpoint, metode)
            analisis, header_cors = pengujian.analisis_cors(header)
            pengujian.cetak_hasil(endpoint, f'OPTIONS (preflight untuk {metode})', status, analisis, header_cors)
        
        print('\n[PERMINTAAN SEDERHANA]')
        for metode in ['GET', 'POST']:
            status, header = pengujian.permintaan_sederhana(endpoint, metode)
            analisis, header_cors = pengujian.analisis_cors(header)
            pengujian.cetak_hasil(endpoint, f'Permintaan {metode}', status, analisis, header_cors)
    
    print('\n\n' + '='*70)
    print('Pengujian Selesai')
    print('='*70 + '\n')

if __name__ == '__main__':
    main()
