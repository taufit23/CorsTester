#!/bin/bash

read -p "Masukkan domain/sub-domain (contoh: http://api.example.com): " ASAL_ORIGIN

if [ -z "$ASAL_ORIGIN" ]; then
    echo "Domain tidak boleh kosong!"
    exit 1
fi

read -p "Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): " PATHS_INPUT

IFS=',' read -ra ARRAY_PATHS <<< "$PATHS_INPUT"
TITIK_AKHIR=("$ASAL_ORIGIN")

for path in "${ARRAY_PATHS[@]}"; do
    path=$(echo "$path" | xargs)
    if [ -n "$path" ]; then
        TITIK_AKHIR+=("${ASAL_ORIGIN}${path}")
    fi
done

if [ ${#TITIK_AKHIR[@]} -lt 2 ]; then
    echo "Minimal satu path harus diinput!"
    exit 1
fi

MERAH='\033[0;31m'
HIJAU='\033[0;32m'
KUNING='\033[1;33m'
BIRU='\033[0;34m'
NORMAL='\033[0m'

uji_cors() {
    local url=$1
    
    echo ""
    echo "============================================================"
    echo -e "${BIRU}Testing CORS untuk: $url${NORMAL}"
    echo "============================================================"
    
    respon=$(curl -s -i -X OPTIONS "$url" \
        -H "Origin: $ASAL_ORIGIN" \
        -H "Access-Control-Request-Method: GET" \
        -H "Access-Control-Request-Headers: Content-Type" \
        2>&1)
    
    if [ $? -ne 0 ]; then
        echo -e "${MERAH}❌ Error testing $url${NORMAL}"
        echo "$respon"
        return
    fi
    
    status=$(echo "$respon" | head -n1)
    echo -e "${KUNING}Status: $status${NORMAL}"
    
    echo ""
    echo "CORS Headers:"
    echo "$respon" | grep -i "Access-Control-Allow" | sed 's/^/  /'
    
    echo ""
    echo "Semua Headers:"
    echo "$respon" | grep "^[A-Z-]*:" | sed 's/^/  /'
    
    echo ""
    echo "Analisis:"
    
    izin_origin=$(echo "$respon" | grep -i "^Access-Control-Allow-Origin:" | cut -d' ' -f2- | tr -d '\r')
    if [ -n "$izin_origin" ]; then
        if [ "$izin_origin" = "*" ]; then
            echo -e "  ${HIJAU}✓ CORS diizinkan untuk SEMUA origin${NORMAL}"
        else
            echo -e "  ${HIJAU}✓ CORS diizinkan untuk: $izin_origin${NORMAL}"
        fi
    else
        echo -e "  ${MERAH}✗ CORS headers tidak ditemukan${NORMAL}"
    fi
}

uji_permintaan() {
    local url=$1
    
    echo ""
    echo "------------------------------------------------------------"
    echo -e "${BIRU}Testing GET request ke: $url${NORMAL}"
    echo "------------------------------------------------------------"
    
    respon=$(curl -s -i -X GET "$url" \
        -H "Origin: $ASAL_ORIGIN" \
        2>&1)
    
    status=$(echo "$respon" | head -n1)
    echo -e "${KUNING}Status: $status${NORMAL}"
    
    echo ""
    echo "Response Headers:"
    echo "$respon" | grep "^[A-Z-]*:" | head -10 | sed 's/^/  /'
    
    header_cors=$(echo "$respon" | grep -i "^Access-Control-Allow-Origin:" | cut -d' ' -f2- | tr -d '\r')
    echo ""
    if [ -n "$header_cors" ]; then
        echo -e "  ${HIJAU}✓ Access-Control-Allow-Origin: $header_cors${NORMAL}"
    else
        echo -e "  ${MERAH}✗ Tidak ada CORS header pada response${NORMAL}"
    fi
}

main() {
    echo "Tool Pengujian CORS"
    echo "Asal Origin: $ASAL_ORIGIN"
    echo "Paths: $(IFS=, ; echo "${TITIK_AKHIR[*]:1}")"
    echo "============================================================"
    
    for endpoint in "${TITIK_AKHIR[@]}"; do
        uji_cors "$endpoint"
        uji_permintaan "$endpoint"
    done
    
    echo ""
    echo "============================================================"
    echo -e "${HIJAU}CORS Testing Selesai${NORMAL}"
    echo "============================================================"
    echo ""
}

main
