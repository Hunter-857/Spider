import glob
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os
import requests
from tqdm import tqdm
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

## 直接在页面上用js 拿的，哈哈,与通过python取读也是一样的
## data-index=0,1,2,3,4 代表了中，日，韩，英  语言
## var target = $("[data-target='voiceTab.attr']").find("[data-index=0]").find("audio source")
## for( var i = 0 ; i < target.length-1 ;i++){console.log(target.eq(i).attr('src'));}
zh_mp3_list = [
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/fe8b5bd9329ae1399e5984ee5cd9de99_7848448826929376815.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b6adc8389cd9f3f6cdbd416bf4cc03c0_6064238623771334434.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6ce18dfa781fe15ec6aa47225a3ba216_3939279418926927457.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/f5549f859816c6a0e7bf0f92d10e9499_7709768556050530100.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e3bc40db79aa56a925e1d70cc172a974_7989796550324583004.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2c15e3352485e4f7ee5fb582cefbe158_11186185574132003.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/73584e4521f41ae15fe2df5befcf1afa_4356493069943290008.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/85696d83c782ccabf51fc36fad044402_4242826447148106852.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/f77493754dd9814a2c9e64d3ca646a3c_6780107601225328272.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1e1f3ce9027393ff08b15a114e5948b3_6766022127049307307.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b7a740c52c79c5eae972ab543d0ef951_3729056806816794728.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1e919bd93e215af968d34ac5af9586d8_3916392181016248860.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2929c2c81f59c7e0ea745229ff03bc3a_5998359451960569180.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cad4ac91c60114b41daba4c7159df594_4289535403995370918.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ae2a6308fc5f914d474917467dd01d30_8226331531067774390.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a08ba307194eb18bc666507765d0e8bb_5457526947507974254.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0dd45b98f619066074943bd87a2edfde_3553945194355498681.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/81cfcc4abda04c913c72842aa6454038_1824208618123747537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3fe81aa348e57a0c23720bd3963ffe37_3433445732403361078.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/449f9bc319cf85d90a596bfe93a7e33d_2885409805946478233.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2db0f44899683f6bdf339b55d2887705_4420817664031824024.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b42e95eb3f22b3f23e05264c38ca2a7d_1777957379330932478.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/889235b5c4572a9f156ee19558ec925a_1335559807021155554.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2778e7187abb29adfd44ac50af9d218f_8388885537911757272.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c0dec4877c2cb949079a41f0c2562fb4_7588884094730996032.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/86b0b8d0803f4de1b95ead8806c6dd6e_6519231628321236410.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c62029e46d0d42d543daaaf75597569a_4536078134500909848.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d85988dea0e08b7bff513f4723b14019_5106709064373883250.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b3018d44728df4e35fa85d448ddede26_8507963744359503086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d322e793ce76c926077aa8ea405dacc7_6524391434724661113.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a3d58d54c8d7385e09fbb8cae7bd4f8b_1462921672171268074.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ea76b640ab6c95175536842ad1a0f173_4328282964578907488.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2501cfd9b73339ef5b3937eb199461a9_2009226641029781437.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/03e24becc0e797ebf5972d02702d876c_5074114084214301565.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4b05ce4a3dc86a215665b6a0f91b99c2_3556239774233070980.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/60f56821ffe99a3ec6bc40a0d46f5d17_6628239331417330464.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/38d8163da59df703df9c54b9d02d46e7_1531380864392418527.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/869f3a71d80e7bc3aad66dab82a9da29_5486655718485100942.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9e4b2dc9a2e975f9ef7897ab1b036858_4416287275136132061.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2e176e35f185670751a51a860069db06_7843351009704007102.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/846bb91ba8c09acc7f9ae7ac15a4de04_4974644072636020086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/2ba140443fb277d50de033fde1badd2b_60778181544643847.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/b6a816d9519edad8b4b0d268c1cfa269_6189111629106157891.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/aacb1c5a801bf8e8e41a7fc839b48bd7_7291547550386226990.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d8b1965ab09962b4f1c4468b33436333_4172892663956403399.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/512c7996cc12090a1d97c5b2793892d8_4836188757891463067.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b12d5d044ad66c4ced021d2a01b2dcfa_5712530839744219759.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9554951c6213a8cf311951f4773d0ca1_7835411794877196119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6f755af151fcb9e76c310c08ee2bb679_9111779409578450184.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d5b227301aacdb8af02ce646093eaaac_848992464529059570.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e06a3c8481c6de8bf7229c18b79c8518_8786857834608305737.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/386e46a863a1adc0c3ffc9757f20d650_614519737191344280.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/daccf2409882a9946522300a535374fe_6864841098234753803.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e43c69a4a9e81f47a8c0e95c82e7aaf6_7897077687475534115.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/16186f48d721ecf249ff909e78b2fab5_570657167150484295.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/36fa6104d73b4c92ea89b38e96422d3c_3922258150748659505.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/58bd0422a20aa7ea65ed0723fdc592e8_7378373347408481762.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/042b1172427a8e96418b013229d2da13_7415599374133483491.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4e45023c40399bb3c15d752ef82d3864_4077697815252108972.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8420f99059c5cdaf1a43b668769e0fc2_7222815634438768540.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a968247e03f332ff3fa35049776251dc_1632237442608110071.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/bb2bb11deaff13cdcfcde395a295ee9d_2035212544242143958.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/efa91d3079704b47bf38c72a910a7574_6893355103999759145.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cb99ad83ca7392485e11e265ba801610_7083299720400850868.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/84475eff931cbe47662a5e3056ebe32e_4268324471262249660.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d564e6ed9886803bb2d7aef6773f6790_5710284996583982468.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/26e85faab35cfe811d9fa766e0050faf_3393518729850465587.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/92e19fba43c556ca6bd144347d896446_7253879706152136181.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/95d14321c2851776a80926eaab927d17_8032458670337828840.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6e48afd0ee0197898394497ddb014559_8424232015811054282.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ac765da974fe727f1c1af71a8f2497ad_9082233353230634105.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/fe8b5bd9329ae1399e5984ee5cd9de99_7848448826929376815.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b6adc8389cd9f3f6cdbd416bf4cc03c0_6064238623771334434.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6ce18dfa781fe15ec6aa47225a3ba216_3939279418926927457.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/f5549f859816c6a0e7bf0f92d10e9499_7709768556050530100.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e3bc40db79aa56a925e1d70cc172a974_7989796550324583004.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2c15e3352485e4f7ee5fb582cefbe158_11186185574132003.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/73584e4521f41ae15fe2df5befcf1afa_4356493069943290008.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/85696d83c782ccabf51fc36fad044402_4242826447148106852.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/f77493754dd9814a2c9e64d3ca646a3c_6780107601225328272.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1e1f3ce9027393ff08b15a114e5948b3_6766022127049307307.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b7a740c52c79c5eae972ab543d0ef951_3729056806816794728.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1e919bd93e215af968d34ac5af9586d8_3916392181016248860.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2929c2c81f59c7e0ea745229ff03bc3a_5998359451960569180.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cad4ac91c60114b41daba4c7159df594_4289535403995370918.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ae2a6308fc5f914d474917467dd01d30_8226331531067774390.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a08ba307194eb18bc666507765d0e8bb_5457526947507974254.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0dd45b98f619066074943bd87a2edfde_3553945194355498681.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/81cfcc4abda04c913c72842aa6454038_1824208618123747537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3fe81aa348e57a0c23720bd3963ffe37_3433445732403361078.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/449f9bc319cf85d90a596bfe93a7e33d_2885409805946478233.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2db0f44899683f6bdf339b55d2887705_4420817664031824024.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b42e95eb3f22b3f23e05264c38ca2a7d_1777957379330932478.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/889235b5c4572a9f156ee19558ec925a_1335559807021155554.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2778e7187abb29adfd44ac50af9d218f_8388885537911757272.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c0dec4877c2cb949079a41f0c2562fb4_7588884094730996032.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/86b0b8d0803f4de1b95ead8806c6dd6e_6519231628321236410.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c62029e46d0d42d543daaaf75597569a_4536078134500909848.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d85988dea0e08b7bff513f4723b14019_5106709064373883250.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b3018d44728df4e35fa85d448ddede26_8507963744359503086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d322e793ce76c926077aa8ea405dacc7_6524391434724661113.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a3d58d54c8d7385e09fbb8cae7bd4f8b_1462921672171268074.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ea76b640ab6c95175536842ad1a0f173_4328282964578907488.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2501cfd9b73339ef5b3937eb199461a9_2009226641029781437.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/03e24becc0e797ebf5972d02702d876c_5074114084214301565.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4b05ce4a3dc86a215665b6a0f91b99c2_3556239774233070980.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/60f56821ffe99a3ec6bc40a0d46f5d17_6628239331417330464.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/38d8163da59df703df9c54b9d02d46e7_1531380864392418527.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/869f3a71d80e7bc3aad66dab82a9da29_5486655718485100942.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9e4b2dc9a2e975f9ef7897ab1b036858_4416287275136132061.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/2e176e35f185670751a51a860069db06_7843351009704007102.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/846bb91ba8c09acc7f9ae7ac15a4de04_4974644072636020086.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/2ba140443fb277d50de033fde1badd2b_60778181544643847.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/b6a816d9519edad8b4b0d268c1cfa269_6189111629106157891.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/aacb1c5a801bf8e8e41a7fc839b48bd7_7291547550386226990.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d8b1965ab09962b4f1c4468b33436333_4172892663956403399.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/512c7996cc12090a1d97c5b2793892d8_4836188757891463067.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b12d5d044ad66c4ced021d2a01b2dcfa_5712530839744219759.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9554951c6213a8cf311951f4773d0ca1_7835411794877196119.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6f755af151fcb9e76c310c08ee2bb679_9111779409578450184.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d5b227301aacdb8af02ce646093eaaac_848992464529059570.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e06a3c8481c6de8bf7229c18b79c8518_8786857834608305737.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/386e46a863a1adc0c3ffc9757f20d650_614519737191344280.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/daccf2409882a9946522300a535374fe_6864841098234753803.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e43c69a4a9e81f47a8c0e95c82e7aaf6_7897077687475534115.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/16186f48d721ecf249ff909e78b2fab5_570657167150484295.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/36fa6104d73b4c92ea89b38e96422d3c_3922258150748659505.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/58bd0422a20aa7ea65ed0723fdc592e8_7378373347408481762.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/042b1172427a8e96418b013229d2da13_7415599374133483491.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4e45023c40399bb3c15d752ef82d3864_4077697815252108972.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8420f99059c5cdaf1a43b668769e0fc2_7222815634438768540.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a968247e03f332ff3fa35049776251dc_1632237442608110071.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/bb2bb11deaff13cdcfcde395a295ee9d_2035212544242143958.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/efa91d3079704b47bf38c72a910a7574_6893355103999759145.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cb99ad83ca7392485e11e265ba801610_7083299720400850868.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/84475eff931cbe47662a5e3056ebe32e_4268324471262249660.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d564e6ed9886803bb2d7aef6773f6790_5710284996583982468.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/26e85faab35cfe811d9fa766e0050faf_3393518729850465587.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/92e19fba43c556ca6bd144347d896446_7253879706152136181.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/95d14321c2851776a80926eaab927d17_8032458670337828840.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6e48afd0ee0197898394497ddb014559_8424232015811054282.mp3",

]
en_map_list = [
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0865558d4728fb8ba87d94107ab6fb6e_3155507132713631937.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/981f6be0c8ac6232dec40936ab3e6e80_7465165546797634676.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8f9bb1f5e3204705fb19fb820078e451_1261156312059032850.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4472f14df9331332fd33f736081d50f0_8796073073854389378.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e40231d4de9e0fc5b08a0f7ad5bdb4ca_7987986885260032570.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bb2afd6d731f0526bba7d5bfdc0b6ac4_2641089421584693379.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e28684061baffb0517aeff8069f27008_7460221098745301804.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0b1f899af99611e7ac4d09734336d858_8403124817914724466.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/44984eaff52247a93eb6ba5b87ab535b_6581312300152422632.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/649b98902b37c111d534da5bcaf6b81c_9047422454941126606.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a058dbc80ab8ade25d36f2fb589e9143_7143408208714046784.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a646184f4fd4aa566530f94da9fdbf46_8098692029554067003.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d4f967cf1b3c35e0aee0752d8946d4d1_198982722099725346.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1eaba3138f05159bb99770c3eca4c173_2517337472414657981.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/eb406db50013f2cd119162285fce6696_4035624984886403060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d20d99f686fde2e17c53d5cdc9a69513_3198044247897153204.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a008d5117714afe0753904590006545f_8137685301566311309.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cf7a8f9a1e4981c30049973552d3fc9a_7529289890257386143.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/485f975d5b4b2fae4bef77b4fb721120_3194713410741155221.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/67720c3e269c073f8e54e74b1463e0ea_5703660440296589319.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/523d0efe08e482800947f4193baf6f1b_3681978285517167524.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9d7b7eb3bfa97baa6d38e3c1a6f5ee45_2673149619806753459.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a6ff2be0650135eeee071c5dc361551a_6835031663531069937.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/272773c06df8feac1f6451f2b29426f2_6555653143369795588.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3984b392ebc29edcd50a1e3d31ac109c_1095817901721117604.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a135173060b934451c3404cccd1a0c8b_587932686121215171.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/196c59480ff1605aebb2fdbb853a71f8_1052968958271080752.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9edaef99be75884eefd7c4407344b5b5_1357135928228335563.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/71d660a12ae5c03f2eb86092dadcd370_8571325279076970709.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bdf8eae6e875d794c44b96ce132663aa_2181018006853594694.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/83af91946f70dd1e015d29760e761b88_6911981417313265075.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b40a55db3da3e400e8f2381ec75ef8d9_7243675129307821812.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6095d637ce8c1cae95e92392c73b4791_4544641704885033671.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c08a107c374f7d463d04dc0d3deea2a2_3705347957734668296.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/613df165bdd81e53938c1a6331f7cbd1_5293908330011866195.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9e4f497a26f2ae85eed3dc8ef4eeacf5_7480332650962357593.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1fa71fd52823d258ecb79bcdd9dcab3c_2611927337820165945.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a67302b11a50aded648040f133710c8b_9109374647834458933.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7749c19ef9e79be4616cd5e98b394044_4010010596743213900.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/00b04e768650dfa400a1d49efd8ebd50_3720674565742603626.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a39513d453a8695658e7a8fce4c6a4b4_789521186903078212.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/234c35535d102ee7febedc72ba43aadb_896384797634191506.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/63db1545e0110d07eda9a916e258735b_5930593629754498604.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/9b52e010c5b6fdcd4bdc8f09bf7bd5d3_954165581271306013.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bf5eb08dc696f252cf4f6313ac145bb7_2870429553578804147.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3b0d5a6bb7686afcecf05a95bbee64e3_1249121324176567013.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6a163ab5a7860c198bf484b49b62ad34_7392069433573833005.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/135b9dd536d19557f0e32e2f5b7e5c70_2761403656100030790.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3c738274fa4c6496b14f1aee0ccd40ab_815456782100426691.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4820f040e5eff74f7a120c6968a42eb2_4633165990862327337.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7b569c3c1a9e84fc77b09611fbf474b0_4276207400539604804.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1d03292701f4be8c872e3a43fa7bd4f7_5652236186503022622.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/528a0b9728000eeb402fcd86f5f801bd_6710067672025316125.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7024e2251ba71d6cd83ab669c3ed2dd3_5583604986014813572.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/050190bbfbddd83581df0a6080cccfc6_6764949306111365543.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8e77edb05650579ad672ef862dd25198_3811022350908947321.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/25fb0618279c322977b50402208fac29_920479044843790034.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/31b5f96180d4d6d05a0349346bdaaa94_6142046050144821537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e3e3cf17fcd628a46eca48dd85ea92bc_5309405645505859939.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/eefc91e1f87973bafd47ce3f55b09c8d_2883751834929450969.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/78975ff90c3be8670f614182b8e3cb5d_7827862092571821653.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/0a19e3dba949e9ae6eb1813110283722_11519351677228748.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/c931354544a1154c306dcd113bc8a8f0_6524900771178805645.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/54db6fa6cf5879c9292b191a116f163e_8470086927424771769.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/78e0afa43d065bfd93d9a2717c5ee5f0_682852251438452995.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b492bdd929db3413ecb690e6f6ce4993_791176618910928292.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a2155cd824bed9ae022dff168f918013_3049832716991009079.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/de91bd3afd2f78dd73d7ec1350870247_6781451437074642890.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ff92e538432f2c5a3525bbd1a7f68b7a_7803199077113370710.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/63e2e19c2f4bb729ee9cd5945c75e67f_7226140574590156344.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/589c37284ec5502a6c04fd7338a8e5f9_6876778821279864578.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0865558d4728fb8ba87d94107ab6fb6e_3155507132713631937.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/981f6be0c8ac6232dec40936ab3e6e80_7465165546797634676.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8f9bb1f5e3204705fb19fb820078e451_1261156312059032850.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4472f14df9331332fd33f736081d50f0_8796073073854389378.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e40231d4de9e0fc5b08a0f7ad5bdb4ca_7987986885260032570.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bb2afd6d731f0526bba7d5bfdc0b6ac4_2641089421584693379.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e28684061baffb0517aeff8069f27008_7460221098745301804.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/0b1f899af99611e7ac4d09734336d858_8403124817914724466.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/44984eaff52247a93eb6ba5b87ab535b_6581312300152422632.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/649b98902b37c111d534da5bcaf6b81c_9047422454941126606.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a058dbc80ab8ade25d36f2fb589e9143_7143408208714046784.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a646184f4fd4aa566530f94da9fdbf46_8098692029554067003.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d4f967cf1b3c35e0aee0752d8946d4d1_198982722099725346.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1eaba3138f05159bb99770c3eca4c173_2517337472414657981.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/eb406db50013f2cd119162285fce6696_4035624984886403060.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/d20d99f686fde2e17c53d5cdc9a69513_3198044247897153204.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a008d5117714afe0753904590006545f_8137685301566311309.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/cf7a8f9a1e4981c30049973552d3fc9a_7529289890257386143.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/485f975d5b4b2fae4bef77b4fb721120_3194713410741155221.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/67720c3e269c073f8e54e74b1463e0ea_5703660440296589319.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/523d0efe08e482800947f4193baf6f1b_3681978285517167524.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9d7b7eb3bfa97baa6d38e3c1a6f5ee45_2673149619806753459.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a6ff2be0650135eeee071c5dc361551a_6835031663531069937.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/272773c06df8feac1f6451f2b29426f2_6555653143369795588.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3984b392ebc29edcd50a1e3d31ac109c_1095817901721117604.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a135173060b934451c3404cccd1a0c8b_587932686121215171.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/196c59480ff1605aebb2fdbb853a71f8_1052968958271080752.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9edaef99be75884eefd7c4407344b5b5_1357135928228335563.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/71d660a12ae5c03f2eb86092dadcd370_8571325279076970709.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bdf8eae6e875d794c44b96ce132663aa_2181018006853594694.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/83af91946f70dd1e015d29760e761b88_6911981417313265075.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b40a55db3da3e400e8f2381ec75ef8d9_7243675129307821812.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6095d637ce8c1cae95e92392c73b4791_4544641704885033671.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/c08a107c374f7d463d04dc0d3deea2a2_3705347957734668296.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/613df165bdd81e53938c1a6331f7cbd1_5293908330011866195.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/9e4f497a26f2ae85eed3dc8ef4eeacf5_7480332650962357593.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1fa71fd52823d258ecb79bcdd9dcab3c_2611927337820165945.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a67302b11a50aded648040f133710c8b_9109374647834458933.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7749c19ef9e79be4616cd5e98b394044_4010010596743213900.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/00b04e768650dfa400a1d49efd8ebd50_3720674565742603626.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a39513d453a8695658e7a8fce4c6a4b4_789521186903078212.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/234c35535d102ee7febedc72ba43aadb_896384797634191506.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/10/31/16576950/63db1545e0110d07eda9a916e258735b_5930593629754498604.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/9b52e010c5b6fdcd4bdc8f09bf7bd5d3_954165581271306013.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/bf5eb08dc696f252cf4f6313ac145bb7_2870429553578804147.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3b0d5a6bb7686afcecf05a95bbee64e3_1249121324176567013.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/6a163ab5a7860c198bf484b49b62ad34_7392069433573833005.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/135b9dd536d19557f0e32e2f5b7e5c70_2761403656100030790.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/3c738274fa4c6496b14f1aee0ccd40ab_815456782100426691.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/4820f040e5eff74f7a120c6968a42eb2_4633165990862327337.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7b569c3c1a9e84fc77b09611fbf474b0_4276207400539604804.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/1d03292701f4be8c872e3a43fa7bd4f7_5652236186503022622.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/528a0b9728000eeb402fcd86f5f801bd_6710067672025316125.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/7024e2251ba71d6cd83ab669c3ed2dd3_5583604986014813572.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/050190bbfbddd83581df0a6080cccfc6_6764949306111365543.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/8e77edb05650579ad672ef862dd25198_3811022350908947321.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/25fb0618279c322977b50402208fac29_920479044843790034.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/31b5f96180d4d6d05a0349346bdaaa94_6142046050144821537.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/e3e3cf17fcd628a46eca48dd85ea92bc_5309405645505859939.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/eefc91e1f87973bafd47ce3f55b09c8d_2883751834929450969.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/78975ff90c3be8670f614182b8e3cb5d_7827862092571821653.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/0a19e3dba949e9ae6eb1813110283722_11519351677228748.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/11/04/16576950/c931354544a1154c306dcd113bc8a8f0_6524900771178805645.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/54db6fa6cf5879c9292b191a116f163e_8470086927424771769.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/78e0afa43d065bfd93d9a2717c5ee5f0_682852251438452995.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/b492bdd929db3413ecb690e6f6ce4993_791176618910928292.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/a2155cd824bed9ae022dff168f918013_3049832716991009079.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/de91bd3afd2f78dd73d7ec1350870247_6781451437074642890.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/ff92e538432f2c5a3525bbd1a7f68b7a_7803199077113370710.mp3",
"https://uploadstatic.mihoyo.com/ys-obc/2022/05/12/6276411/63e2e19c2f4bb729ee9cd5945c75e67f_7226140574590156344.mp3",

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
def get_map3(mp3_list, out_path,out_file_name = None):
    '''

    :param mp3_list:
    :param out_path: MP3_NAME_FORMATE_{:03d}
    :param out_file_name: if file name is None , file name will use out file last folder name
    :return: null ,check file in path
    '''
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    if out_file_name is None:
        out_file_name = out_path.split("/")[-1]
    for i in range(0, len(mp3_list)):
        response = requests.request("GET", mp3_list[i], headers=headers)
        data = response.content
        with open("/".join([out_path, out_file_name+"_{:03d}".format(i)+".mp3"]), 'ab+') as f:
            f.write(data)
            f.flush()
            print("写入第{}文件成功".format(i))


def write_all_map3_into(input_path, output_file, out_file_name: str):

    '''
        :param input_path:   '/path/to/mp3/folder'
        :param output_file: '/path/to/mp3/out'
        :param out_file_name:   'output.mp3'
        :return:
    '''
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
    assert out_file_name.endswith(".mp3")
    print("start write to file")
    combined_audio.export(output_file + out_file_name, format='mp3')
    print("writing end")

def mp3_to_some_wav(input_file, output_folder, file_name ,segment_length=10):
    '''

    :param 输入的文件名:
    :param 输出文件名:
    :param 长度: 长MP3车切分的长度
    :return:
    '''
    # 设置输入
    # 读取MP3 文件把它按照一定的长度分解
    # 使用pydub载入mp3文件
    audio = AudioSegment.from_file(input_file, format='mp3')

    # 将长度转换为毫秒
    length_ms = len(audio)
    # 计算每个音频片段的开始和结束位置
    start = 0
    end = start + segment_length * 1000
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # 切割音频，并输出到文件
    while end < length_ms:
        # 从原始音频中获取当前音频片段
        segment = audio[start:end]
        print("auto write {} to end".format(start,end))
        # 计算输出文件名
        output_file = os.path.join(output_folder, file_name+f'_{start}_{end}.wav')
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
     多个mp3 文件转化为 wav ,mp3 一对一 对应的转换为，wav，但是不能均分
    :param file_path:
    :return:
    '''
    path_list = glob.glob(os.path.join(file_path, '*.mp3'))
    file_index = 0
    for i in tqdm(range(0, len(path_list))):
        print(path_list[i])
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
    # 拿到 map3
    # total_list = zh_mp3_list + en_map_list
    # get_map3(total_list, out_path="../out/shen_li")
    # 合并成为长的MP3
    # write_all_map3_into(input_path="../out/shen_li/mp3",
    #                   output_file="../out/shen_li/",
    #                   out_file_name="shen_li_long.mp3")
    # 把长的MP3等分成为多个wav
    mp3_to_some_wav("../out/shen_li/shen_li_long.mp3", "../out/shen_li/wav", "shen_li", segment_length=20)

    # flac_to_wav("C:\\Users\\admin\\Desktop\\xiaochou.flac", "./out/new")