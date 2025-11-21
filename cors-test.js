const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function tanyaDomain() {
  return new Promise(resolve => {
    rl.question('Masukkan domain/sub-domain (contoh: http://api.example.com): ', (domain) => {
      resolve(domain.trim());
    });
  });
}

function tanyaPath() {
  return new Promise(resolve => {
    rl.question('Masukkan URL paths yang ingin di-test, dipisahkan koma (contoh: /api,/api/data,/v1/users): ', (paths) => {
      const listPath = paths.split(',').map(p => p.trim()).filter(p => p.length > 0);
      resolve(listPath);
    });
  });
}

async function ujiCORS(url, asalOrigin) {
  console.log('\n' + '='.repeat(60));
  console.log(`Testing CORS untuk: ${url}`);
  console.log('='.repeat(60));

  try {
    const respon = await fetch(url, {
      method: 'OPTIONS',
      headers: {
        'Origin': asalOrigin,
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type',
      },
    });

    console.log(`\nStatus Code: ${respon.status} ${respon.statusText}`);
    console.log('\nCORS Headers:');
    console.log(`  Access-Control-Allow-Origin: ${respon.headers.get('Access-Control-Allow-Origin') || 'NOT SET'}`);
    console.log(`  Access-Control-Allow-Methods: ${respon.headers.get('Access-Control-Allow-Methods') || 'NOT SET'}`);
    console.log(`  Access-Control-Allow-Headers: ${respon.headers.get('Access-Control-Allow-Headers') || 'NOT SET'}`);
    console.log(`  Access-Control-Max-Age: ${respon.headers.get('Access-Control-Max-Age') || 'NOT SET'}`);
    console.log(`  Access-Control-Allow-Credentials: ${respon.headers.get('Access-Control-Allow-Credentials') || 'NOT SET'}`);

    console.log('\nSemua Headers:');
    respon.headers.forEach((nilai, nama) => {
      console.log(`  ${nama}: ${nilai}`);
    });

  } catch (error) {
    console.error(`\n❌ Error testing ${url}:`);
    console.error(`   ${error.message}`);
  }
}

async function jalankanUji() {
  const asalOrigin = await tanyaDomain();
  
  if (!asalOrigin) {
    console.error('Domain tidak boleh kosong!');
    rl.close();
    return;
  }

  const listPath = await tanyaPath();
  
  if (listPath.length === 0) {
    console.error('Minimal satu path harus diinput!');
    rl.close();
    return;
  }

  console.log(`\nMenggunakan domain: ${asalOrigin}`);
  console.log(`URL paths yang akan di-test: ${listPath.join(', ')}\n`);

  const titikAkhir = [
    asalOrigin,
    ...listPath.map(path => `${asalOrigin}${path}`)
  ];

  for (const endpoint of titikAkhir) {
    await ujiCORS(endpoint, asalOrigin);
  }

  console.log('\n' + '='.repeat(60));
  console.log('CORS Testing Selesai');
  console.log('='.repeat(60) + '\n');
  
  rl.close();
}

jalankanUji().catch(console.error);
