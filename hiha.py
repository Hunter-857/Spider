import glob
from pydub import AudioSegment
from pydub.  exceptions import CouldntDecodeError
import os
import requests
#from bs4 import BeautifulSoup
import re
#from requests_html import HTMLSession

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    "accept": 'application/json, text/plain, */*',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'zh-CN,zh;q=0.9',
    "origin": 'https://bbs.mihoyo.com',
    "referer": 'https://bbs.mihoyo.com',
    'sec-ch-ua': 'Chromiumv=110, Not A(Brand;v=24, Google Chrome;v=110',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
}

## 直接在页面上用js 拿的，哈哈
## for( var i = 0 ; i < $("[data-index=1]").find("audio source").length ;i++){console.log($("[data-index=1]").find("audio source").eq(i).attr('src'));}
mp3_list = [
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9f88cb449642a6c75632eda02d2c2c03_6266030872702151196.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/da75e7fcf23a314f9a75d0d7bbf11306_1090607682706726377.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0669bfc8a33cae0b42c7c9055ce0e2c2_4733061096502627238.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c342c3f006fdd380497d34fa7960d4e9_7617084460699555501.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/85ebd25d90316f670de4f7531bcc72d8_5446665584779561774.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/cf894e1f9388ee51c738a486f02cb6ec_819781155720925341.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c7745267c867b009c9af878b7c3d046b_169924931344397886.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0b74ebf3802c39ebf0322c1c7e99a948_5182758143619435548.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/7839be6f25b08bf1bd8c6c36cbfe0031_7229071090323951342.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d77bbfb20e9d05b00450598ff8f531e0_8838063994496325962.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/fb7482ab9a071c2f59eb9cd701c9eedb_2715103572842019573.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ca4269019eb7487e6d0add5c51c36f9a_6599915116316422319.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/51cde450bb45a6f9b9b34ac65b652a8f_5932027430173758234.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4216ce4fc473b68bffbe4bf11c1d0598_4543434772361027242.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e76786c38fee38e6e527488b36c4dd5a_7068831072213022441.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dbb21b73bd20c4850d49f2e26d17786f_4615966368697215404.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6d3b8aafea01e7224b2eed199acd6d3c_963087837134895203.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ae38c240ea68c1ccc200a291835d444d_4999550022678888552.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c39889c91cd3796053cc6ae3b4d81420_782746513971350614.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/10dfb209d12a86a70a2f10ed3d5505e5_2251299937627957520.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f12c311c213c6f302ced47ca4d945594_9147142430390185096.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9b1bec0e0b84bf57ff50c599c19d23e6_2446326612910358007.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/98c955a49dc28a34e4696fa22033f732_168060378706046472.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2771e2359aa990eabf6e54228468ecad_7733906721836127849.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/68cf80066bd6450a16129a3cb348339b_5768355460862294396.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/59cf2ee7fc9335502ba58fe955d8e302_2633294220037979060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/007f60047bd67c4285ef6998b35b1232_2010401963867632431.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e7d2ebc63b06d91d498acfc228172188_4260547276335573315.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/738d6900e971a03c51f891e5bfc86f5d_79369201909278822.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a656961b22ee9571222cc19bb78030f0_8508629951637820958.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/47869cbb60174f0868d003dfae63044d_2882514374733253862.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/98f70f35314c8376e4a29223cbe7d623_1304418544709684294.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4a98e7776ea0231bed6fbf7ff6783206_5120943557142207318.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5a149ffb7ba34b277b68e37a36db6c64_4588758667855773513.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f392afec320ce7678cbe76a9ac9cf51b_1431729407402312815.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/455e0912e2d9de9d87fd9cdaecaf95c4_4592858504780805086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e90c2ae7b5fb857741b372a22c42e567_3252648119425596391.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/74659e37ec483e3929c57a8f1263da3f_5178135561460858640.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/97ed928c4e1635411aca4f4f37785e4e_3165762718458269772.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/978617513d0e9e747cbe72ea14dd4e47_5789643296752008374.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0a1d4d0c3562f2462ebad246a282ef79_6967587928779149120.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8364bfaf9d2d8df4d4dc1ec83990934b_2098110397247075835.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e0c9e86a3995bcd59fdbe7ae63e76c24_5404598826705504744.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ab4117992bd040d6908ea9a0e4998c0d_2751933678237403872.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/804b243d9bee26b7fe21e512a122d590_8379555976435788423.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/757106c11d530ba0d42f99c2ba71a061_3816474257498776007.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8160dc55ce2cecc371df4dbe9a84cf02_8626620992207742475.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b93d2415df77756244b94859461aa645_3925012666693998759.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/178d618bbe358ef32c89f4826aacbb97_8779302875037059808.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/bf146781cb24681c81ab756af9b34daa_5376771438446890822.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6bf5ab3e906464f4daa1a146d1563202_5885159335856366158.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/23cae140f7e2aa364575efe74e6d9839_3621855845272175119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/669767be418c007d5b2dbf4b7083cf48_474646943793305031.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8906a40c63e496af4ac82b4ae1e2e6fc_3702663097818481229.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ba129d009fc2eca5bd1e6b8585a571fa_5934895226062488864.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/aa1eda7863372fa01ac4381c7514a9a5_6586703930122365610.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/50eee1248083eb97721f88095cae2fd5_7892842461541601309.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/78fa73e6fd60f95e73bee5af09378609_2516719370237170095.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/af34f5646151804a086492e999d3bff1_8121268277800575888.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f8e11570e02126c2704e2a24a8f95228_5790172030867739362.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a67bdfbffc4842a17f447cfb22339ed5_1440050648068138883.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4bc561059b1a0ed03a6de84e10f7c200_5669329393881775320.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ac36820526cec159b2eae14edbc8cbb2_6243900655177865005.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/49d04d95c4842e8dfeb7ddded8225f86_3657987300051219746.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dcd0805b1d9b02ca6c684d6fb307ac3d_2622461242190631105.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6aa6d8c163f44907ca2adb37593f9328_3147195060552103985.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d635f564aaa4d3e97d8202b9eb54abdb_2494005338180229056.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0071121d38c0966a974ec9bf585cde98_8669909603843465315.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4a8141236b743de2d38aefa81d73fd21_5714216922338222114.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9f88cb449642a6c75632eda02d2c2c03_6266030872702151196.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/da75e7fcf23a314f9a75d0d7bbf11306_1090607682706726377.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0669bfc8a33cae0b42c7c9055ce0e2c2_4733061096502627238.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c342c3f006fdd380497d34fa7960d4e9_7617084460699555501.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/85ebd25d90316f670de4f7531bcc72d8_5446665584779561774.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/cf894e1f9388ee51c738a486f02cb6ec_819781155720925341.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c7745267c867b009c9af878b7c3d046b_169924931344397886.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0b74ebf3802c39ebf0322c1c7e99a948_5182758143619435548.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/7839be6f25b08bf1bd8c6c36cbfe0031_7229071090323951342.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d77bbfb20e9d05b00450598ff8f531e0_8838063994496325962.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/fb7482ab9a071c2f59eb9cd701c9eedb_2715103572842019573.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ca4269019eb7487e6d0add5c51c36f9a_6599915116316422319.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/51cde450bb45a6f9b9b34ac65b652a8f_5932027430173758234.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4216ce4fc473b68bffbe4bf11c1d0598_4543434772361027242.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e76786c38fee38e6e527488b36c4dd5a_7068831072213022441.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dbb21b73bd20c4850d49f2e26d17786f_4615966368697215404.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6d3b8aafea01e7224b2eed199acd6d3c_963087837134895203.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ae38c240ea68c1ccc200a291835d444d_4999550022678888552.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c39889c91cd3796053cc6ae3b4d81420_782746513971350614.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f12c311c213c6f302ced47ca4d945594_9147142430390185096.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9b1bec0e0b84bf57ff50c599c19d23e6_2446326612910358007.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/98c955a49dc28a34e4696fa22033f732_168060378706046472.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2771e2359aa990eabf6e54228468ecad_7733906721836127849.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/68cf80066bd6450a16129a3cb348339b_5768355460862294396.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/59cf2ee7fc9335502ba58fe955d8e302_2633294220037979060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/007f60047bd67c4285ef6998b35b1232_2010401963867632431.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e7d2ebc63b06d91d498acfc228172188_4260547276335573315.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/738d6900e971a03c51f891e5bfc86f5d_79369201909278822.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a656961b22ee9571222cc19bb78030f0_8508629951637820958.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/47869cbb60174f0868d003dfae63044d_2882514374733253862.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/98f70f35314c8376e4a29223cbe7d623_1304418544709684294.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4a98e7776ea0231bed6fbf7ff6783206_5120943557142207318.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5a149ffb7ba34b277b68e37a36db6c64_4588758667855773513.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f392afec320ce7678cbe76a9ac9cf51b_1431729407402312815.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/455e0912e2d9de9d87fd9cdaecaf95c4_4592858504780805086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e90c2ae7b5fb857741b372a22c42e567_3252648119425596391.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/74659e37ec483e3929c57a8f1263da3f_5178135561460858640.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/97ed928c4e1635411aca4f4f37785e4e_3165762718458269772.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/978617513d0e9e747cbe72ea14dd4e47_5789643296752008374.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0a1d4d0c3562f2462ebad246a282ef79_6967587928779149120.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8364bfaf9d2d8df4d4dc1ec83990934b_2098110397247075835.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e0c9e86a3995bcd59fdbe7ae63e76c24_5404598826705504744.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ab4117992bd040d6908ea9a0e4998c0d_2751933678237403872.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/804b243d9bee26b7fe21e512a122d590_8379555976435788423.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/757106c11d530ba0d42f99c2ba71a061_3816474257498776007.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8160dc55ce2cecc371df4dbe9a84cf02_8626620992207742475.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b93d2415df77756244b94859461aa645_3925012666693998759.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/178d618bbe358ef32c89f4826aacbb97_8779302875037059808.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/bf146781cb24681c81ab756af9b34daa_5376771438446890822.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6bf5ab3e906464f4daa1a146d1563202_5885159335856366158.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/23cae140f7e2aa364575efe74e6d9839_3621855845272175119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/669767be418c007d5b2dbf4b7083cf48_474646943793305031.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/8906a40c63e496af4ac82b4ae1e2e6fc_3702663097818481229.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ba129d009fc2eca5bd1e6b8585a571fa_5934895226062488864.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/aa1eda7863372fa01ac4381c7514a9a5_6586703930122365610.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/50eee1248083eb97721f88095cae2fd5_7892842461541601309.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/78fa73e6fd60f95e73bee5af09378609_2516719370237170095.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/af34f5646151804a086492e999d3bff1_8121268277800575888.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f8e11570e02126c2704e2a24a8f95228_5790172030867739362.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a67bdfbffc4842a17f447cfb22339ed5_1440050648068138883.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4bc561059b1a0ed03a6de84e10f7c200_5669329393881775320.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ac36820526cec159b2eae14edbc8cbb2_6243900655177865005.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/49d04d95c4842e8dfeb7ddded8225f86_3657987300051219746.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dcd0805b1d9b02ca6c684d6fb307ac3d_2622461242190631105.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/6aa6d8c163f44907ca2adb37593f9328_3147195060552103985.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d635f564aaa4d3e97d8202b9eb54abdb_2494005338180229056.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0071121d38c0966a974ec9bf585cde98_8669909603843465315.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4a8141236b743de2d38aefa81d73fd21_5714216922338222114.mp3",
]
en_map_list = [
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/395ea76132aec9dff9da59c02942b15f_8615111570710127805.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/da7892ac861e0275e346dd2c39dbe824_1983472339302079098.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/52db3124c7050ce5bec10a5d4359a4c4_4001052847950906531.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/126282a0026d028b2c06f2ead62927a0_4293383431180720244.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ebceb39495d1e3fe51762aa5e155e622_490853373157953592.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4f78d122dc546974a43a3cf33b7b5d5c_7394068183099004034.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c482c4f381b6485bbd3a052af3165e2d_4841457828994574576.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/1dee73dad7dba4a7fccbaa5682d66343_3588362787370628288.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2022f28f230496e8348e4b2d27b4e6d6_7554466538539868119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2c00b6746813816abad67435af84fb06_2619256832489762749.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5afc36eb0ef84a504a714cb00a36345c_4637421398590344811.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/64aa206a1312d7eaefb77fef64786288_8898503917498062322.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/761ee166910751158f06fff30b4b0911_3401174823158566813.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/519be6c024ca1004774a39a94b32bf03_3167173298573844252.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e84fff3d09ea7d03d8460a868f92a946_2380236533103104374.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9b84a8e1d89ab7cb21fc2115421ca334_8703495711335839055.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/bd3fcf822eecec07f2bce9400f28ef43_2934189543451517972.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b8e81381b5d9a41a20fa96473f20b27f_4179223396361501876.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2e57b8ac4f8fb66a1b39063c76d0c26e_2438417375655649762.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5893a7a87e4d45b4b30a59bde985ee20_7750138232628432448.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a1c78128494ea0e2f182c4ee935fa946_5147988569528254482.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b0f060f283692a2058bd118da47e475e_304534637682701921.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0d2b54d0d00d4fbd6bfab7865602d95a_7953000570600154825.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/716937de450742ece5266a21b7b0252a_2224032351282111116.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ede15546f85d1f9c2a27447f805450db_6974117509834612027.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/07e9fb32f4ce107a23a80d662900c449_6974226946987215955.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/3e5ec0c2824188c0a8d4721aa56c344c_5303128749733806139.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/3bee5941e9fd0243dad50a09e98af198_5566488677057611417.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a466faba3426974120c5fd2f800309d9_7942102098489112329.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0cc7be72a718e820412c5d63c65cdea0_3040176738187680730.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/658e0fe4e4eef1b6e7d1571c08211bb0_2970390698594369244.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ebfa6ec894580d6ec3a33045ce812ec7_5793671769147955548.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e6be9c1b702818a433a7135343743107_4644336692919945306.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/be5c30617abdfe9dde882e262e0f8db2_7262772692583270060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5ea24b42589d4d4545740ef01118427c_8840386186646081888.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/34c9e4ea64c6123c64d86250209e490e_3393059240761697567.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/90e473cad0ead2eb7c9d9b8d963ea3c8_3245960199065794563.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5c88b1d6aa67a8e2315835aa3f432636_1845363438224682490.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a9565ff64110d472ee81cb45a707acdb_6895076301352146982.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b458460ed763117e4a19894d1e9bd554_3278601193680606950.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2d2ee2fa068b38ce47a300a4bec8c409_6074258635010723600.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2b0ecf26c563c4dc81a992bb86152f2b_3151559545962664049.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/97c3c0d01bda827d159a3d38085ad606_5355668104927755041.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d6fbb386cc777c2052a2ee4b9158a02a_8282648145155187208.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c05503d7b86bcd53d7ba6e2aa523c781_40924606793733412.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/148b454d0b8b70394a2de221bb351725_6891044266184565731.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b6d2de6555e307d7d1adf3cfa1af08ae_3823580149112451036.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/94096f08b757531b725380d840d440b3_6504663814794516704.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/66f91144330c856f37eb8ca92572167a_8479017490914405352.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dde2c1fc29333def989a85f892824ac2_5505600719668794918.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/80bfaacf3da43d406e4aa2dd2b14e166_4308475852647508543.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d2baa7f43f02f036c5f0b8bee3c3115e_8166276341753157537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9ca2672fed4ff1dda71bc53dab8ceba7_4995153191438801547.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/87400e1079954503e038be38d4c10cb7_1588505792756333175.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d56cb815be888f12d9036324ff2107da_8316000355146214281.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/25ee82111e8884230e9552ede2d368c6_6198235604543470181.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/cbded55de3a3ce85abf4bc4396f89867_6124459688129916707.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/1de995cea4ab4d76500e6d6c8359c603_5927178282321608322.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b973241f3fc1eff41ce6b3c407e92d45_3279960572218756337.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/35ba4c9cc9e608bb28fe9d58520b6ec9_4298332480013089523.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/de0465daeeec568609cf4fc8924ad71d_8410302742122689233.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/282a3a578899c9e48924e34b7a4d50b6_4035205636396201262.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5bfabcce4f3352382cf8191bba1ecd1b_875302201386469055.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f01a324af8b516a4796e9c4ab93daf83_5451956667663594193.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/225b533cac8e5911734e507d46ffeb21_2617544834328568984.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/49799a5b511961b5f4dfa145ecda4962_1623486877873571692.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/69e4c8bc2b317b926afe11367fbc7775_2623784017790331473.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/7e8a5e03fe815fe7fb6d71aabb97b2ec_3042993190577607149.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/402b882c4e43aa855acd78a1e4061581_1477966994640726942.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/395ea76132aec9dff9da59c02942b15f_8615111570710127805.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/da7892ac861e0275e346dd2c39dbe824_1983472339302079098.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/52db3124c7050ce5bec10a5d4359a4c4_4001052847950906531.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/126282a0026d028b2c06f2ead62927a0_4293383431180720244.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ebceb39495d1e3fe51762aa5e155e622_490853373157953592.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/4f78d122dc546974a43a3cf33b7b5d5c_7394068183099004034.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c482c4f381b6485bbd3a052af3165e2d_4841457828994574576.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/1dee73dad7dba4a7fccbaa5682d66343_3588362787370628288.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2022f28f230496e8348e4b2d27b4e6d6_7554466538539868119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2c00b6746813816abad67435af84fb06_2619256832489762749.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5afc36eb0ef84a504a714cb00a36345c_4637421398590344811.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/64aa206a1312d7eaefb77fef64786288_8898503917498062322.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/761ee166910751158f06fff30b4b0911_3401174823158566813.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/519be6c024ca1004774a39a94b32bf03_3167173298573844252.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e84fff3d09ea7d03d8460a868f92a946_2380236533103104374.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9b84a8e1d89ab7cb21fc2115421ca334_8703495711335839055.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/bd3fcf822eecec07f2bce9400f28ef43_2934189543451517972.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b8e81381b5d9a41a20fa96473f20b27f_4179223396361501876.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2e57b8ac4f8fb66a1b39063c76d0c26e_2438417375655649762.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5893a7a87e4d45b4b30a59bde985ee20_7750138232628432448.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a1c78128494ea0e2f182c4ee935fa946_5147988569528254482.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b0f060f283692a2058bd118da47e475e_304534637682701921.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0d2b54d0d00d4fbd6bfab7865602d95a_7953000570600154825.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/716937de450742ece5266a21b7b0252a_2224032351282111116.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ede15546f85d1f9c2a27447f805450db_6974117509834612027.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/07e9fb32f4ce107a23a80d662900c449_6974226946987215955.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/3e5ec0c2824188c0a8d4721aa56c344c_5303128749733806139.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/3bee5941e9fd0243dad50a09e98af198_5566488677057611417.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a466faba3426974120c5fd2f800309d9_7942102098489112329.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/0cc7be72a718e820412c5d63c65cdea0_3040176738187680730.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/658e0fe4e4eef1b6e7d1571c08211bb0_2970390698594369244.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/ebfa6ec894580d6ec3a33045ce812ec7_5793671769147955548.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/e6be9c1b702818a433a7135343743107_4644336692919945306.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/be5c30617abdfe9dde882e262e0f8db2_7262772692583270060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5ea24b42589d4d4545740ef01118427c_8840386186646081888.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/34c9e4ea64c6123c64d86250209e490e_3393059240761697567.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/90e473cad0ead2eb7c9d9b8d963ea3c8_3245960199065794563.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5c88b1d6aa67a8e2315835aa3f432636_1845363438224682490.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/a9565ff64110d472ee81cb45a707acdb_6895076301352146982.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b458460ed763117e4a19894d1e9bd554_3278601193680606950.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2d2ee2fa068b38ce47a300a4bec8c409_6074258635010723600.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/2b0ecf26c563c4dc81a992bb86152f2b_3151559545962664049.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/97c3c0d01bda827d159a3d38085ad606_5355668104927755041.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d6fbb386cc777c2052a2ee4b9158a02a_8282648145155187208.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/c05503d7b86bcd53d7ba6e2aa523c781_40924606793733412.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/148b454d0b8b70394a2de221bb351725_6891044266184565731.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b6d2de6555e307d7d1adf3cfa1af08ae_3823580149112451036.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/94096f08b757531b725380d840d440b3_6504663814794516704.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/66f91144330c856f37eb8ca92572167a_8479017490914405352.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/dde2c1fc29333def989a85f892824ac2_5505600719668794918.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/80bfaacf3da43d406e4aa2dd2b14e166_4308475852647508543.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d2baa7f43f02f036c5f0b8bee3c3115e_8166276341753157537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/9ca2672fed4ff1dda71bc53dab8ceba7_4995153191438801547.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/87400e1079954503e038be38d4c10cb7_1588505792756333175.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/d56cb815be888f12d9036324ff2107da_8316000355146214281.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/25ee82111e8884230e9552ede2d368c6_6198235604543470181.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/cbded55de3a3ce85abf4bc4396f89867_6124459688129916707.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/1de995cea4ab4d76500e6d6c8359c603_5927178282321608322.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/b973241f3fc1eff41ce6b3c407e92d45_3279960572218756337.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/35ba4c9cc9e608bb28fe9d58520b6ec9_4298332480013089523.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/de0465daeeec568609cf4fc8924ad71d_8410302742122689233.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/282a3a578899c9e48924e34b7a4d50b6_4035205636396201262.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/5bfabcce4f3352382cf8191bba1ecd1b_875302201386469055.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/f01a324af8b516a4796e9c4ab93daf83_5451956667663594193.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/225b533cac8e5911734e507d46ffeb21_2617544834328568984.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/49799a5b511961b5f4dfa145ecda4962_1623486877873571692.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/69e4c8bc2b317b926afe11367fbc7775_2623784017790331473.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/7e8a5e03fe815fe7fb6d71aabb97b2ec_3042993190577607149.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2023/01/18/16576950/402b882c4e43aa855acd78a1e4061581_1477966994640726942.mp3",
]

# def get_page(url):
#     session = HTMLSession()
#     response = session.get(url, timeout=15)
#     response.html.render()
#     # 解析渲染后的HTML内容
#     soup = BeautifulSoup(response.html.html, 'html.parser')
#     # response.content
#     with open("out/web.html","ab") as f:
#         f.write(response.html.html.encode('utf-8'))
#     # xpath = '//div[contains(@class,"obc-tmpl-character__voice-btn")]/audio/source'
def get_map3():
    total_list = mp3_list+en_map_list
    for i in range(0, len(total_list)):
        response = requests.request("GET", total_list[i], headers=headers)
        data = response.content
        if not os.path.exists("out\yaoyao"):
            os.mkdir("out/yaoyao")
        with open("out\yaoyao\yaoyao_{:03d}".format(i) + ".mp3", 'ab+') as f:
            f.write(data)
            f.flush()
            print("写入第{}文件成功".format(i))

def write_all_map3_into(input_path, output_file):
    # 设置文件夹路径和输出文件名
    # folder_path = '/path/to/mp3/folder'
    # output_file = 'output.mp3'
    # 获取文件夹下所有的mp3文件
    mp3_files = glob.glob(os.path.join(input_path, '*.mp3'))
    if not os.path.exists(output_file):
        os.path.exists(output_file)
    # 创建一个空的音频片段
    combined_audio = AudioSegment.silent(duration=0)

    # 遍历所有mp3文件，将它们添加到音频片段中
    for mp3_file in mp3_files:
        # 使用pydub库载入mp3文件
        print("reading file {}".format(mp3_file))
        audio = AudioSegment.from_file(mp3_file, format='mp3')
        combined_audio += audio

    # 将组合音频输出到文件
    combined_audio.export(output_file+"/log.mp3", format='mp3')


def mp3_to_some_wav(input_file, output_folder, segment_length=10):
    # 设置输入输出文件名和长度
    # 读取MP3 文件把它按照一定的长度分解
    # 使用pydub载入mp3文件
    audio = AudioSegment.from_file(input_file, format='mp3')

    # 将长度转换为毫秒
    length_ms = len(audio)
    # 计算每个音频片段的开始和结束位置
    start = 0
    end = start + segment_length * 1000

    # 切割音频，并输出到文件
    while end < length_ms:
        # 从原始音频中获取当前音频片段
        segment = audio[start:end]
        # 计算输出文件名
        output_file = os.path.join(output_folder, f'yaoyao_{start}_{end}.wav')
        # 输出到文件
        segment.export(output_file, format='wav')
        # 移动到下一个音频片段 秒为单位标记
        start += segment_length * 1000
        end += segment_length * 1000

    # 切割最后一个音频片段
    if start < length_ms:
        segment = audio[start:]

        output_file = os.path.join(output_folder, f'segment_{start/1000}_{length_ms/1000}.wav')
        segment.export(output_file, format='wav')
def multi_mp3_to_wav(file_path):
    '''
     多个mp3 文件转化为 wav
    :param file_path:
    :return:
    '''
    path_list = glob.glob(os.path.join(file_path, '*.mp3'))
    file_index = 0
    for i in range(0, len(path_list)):
        print(path_list[i])
        print("=======================")
        mp3_file = AudioSegment.from_file(path_list[i], format="mp3")
        file_name =path_list[i].split("\\")[1]
        print("writing " + file_name[:-3])
        # 将MP3文件转换为WAV格式
        try:
            wav_file = mp3_file.export("/".join([file_path, "yaoyao_wav_{:03d}".format(i) + ".wav"]), format="wav")
            file_index +=1
        except Exception as e:
            print(file_name[:-3] + "failed")
        except CouldntDecodeError as err:
            print(err)


def flac_to_wav(file_path,out_path):
    flac_file = AudioSegment.from_file(file_path, format="flac")
    file_name = file_path.split("\\")[-1]
    print("writing " + file_name)
    # 将MP3文件转换为WAV格式
    wav_file = flac_file.export("/".join([out_path, 'test.wav']), format="wav")
    print("finished")



if __name__ == '__main__':
    #get_page(page_url)
    # get_map3()
    # write_all_map3_into(input_path="out/yaoyao", output_file="D:\codespace\Python-Chatroom\out\yaoyao")
    # multi_mp3_to_wav("./out/yaoyao/wav")
    # mp3_to_some_wav("out/yaoyao/wav/log.mp3", "out/yaoyao/wav", segment_length=20)
    flac_to_wav("C:\\Users\\admin\\Desktop\\xiaochou.flac", "./out/new")