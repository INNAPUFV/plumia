// node cifrar-uno.js entrada.json PALABRA  → imprime {clave, bloque}
const fs=require('fs'); const {webcrypto:wc}=require('crypto'); const subtle=wc.subtle;
const ALF='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const rnd=n=>[...wc.getRandomValues(new Uint8Array(n))].map(x=>ALF[x%ALF.length]).join('');
const norm=k=>k.toUpperCase().replace(/[^A-Z0-9]/g,''); const b64=u=>Buffer.from(u).toString('base64');
(async()=>{ const obj=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); const clave=process.argv[3]+'-'+rnd(4);
 const salt=wc.getRandomValues(new Uint8Array(16)), iv=wc.getRandomValues(new Uint8Array(12));
 const base=await subtle.importKey('raw',new TextEncoder().encode(norm(clave)),'PBKDF2',false,['deriveKey']);
 const key=await subtle.deriveKey({name:'PBKDF2',salt,iterations:150000,hash:'SHA-256'},base,{name:'AES-GCM',length:256},false,['encrypt']);
 const ct=new Uint8Array(await subtle.encrypt({name:'AES-GCM',iv},key,new TextEncoder().encode(JSON.stringify(obj))));
 console.log(JSON.stringify({clave,bloque:{s:b64(salt),i:b64(iv),d:b64(ct)}}));
})();
