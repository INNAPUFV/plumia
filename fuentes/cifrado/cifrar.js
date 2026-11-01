// Uso: node cifrar.js <archivo-app.html> <salida.json>  → extrae TELETIPOS_CLASE, genera claves y cifra
const fs=require('fs'); const {webcrypto:wc}=require('crypto'); const subtle=wc.subtle;
const src=fs.readFileSync(process.argv[2],'utf8');
const a=src.indexOf('const TELETIPOS_CLASE = ['), b=src.indexOf('function loadStory(d, origen){');
const T=eval('('+src.slice(a,b).replace('const TELETIPOS_CLASE =','').trim().replace(/;$/,'')+')');
const ALF='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const WORDS=['TINTA','ROTATIVA','GALERADA','LINOTIPIA','TITULAR','CRONICA','PORTADA','TELETIPO'];
const rnd=n=>[...wc.getRandomValues(new Uint8Array(n))].map(x=>ALF[x%ALF.length]).join('');
const norm=k=>k.toUpperCase().replace(/[^A-Z0-9]/g,'');
const b64=u=>Buffer.from(u).toString('base64');
(async()=>{
 const out=[], claves=[];
 for(let i=0;i<T.length;i++){
  const t=T[i]; const clave=WORDS[i%WORDS.length]+'-'+rnd(4);
  const salt=wc.getRandomValues(new Uint8Array(16)), iv=wc.getRandomValues(new Uint8Array(12));
  const base=await subtle.importKey('raw',new TextEncoder().encode(norm(clave)),'PBKDF2',false,['deriveKey']);
  const key=await subtle.deriveKey({name:'PBKDF2',salt,iterations:150000,hash:'SHA-256'},base,{name:'AES-GCM',length:256},false,['encrypt']);
  const ct=new Uint8Array(await subtle.encrypt({name:'AES-GCM',iv},key,new TextEncoder().encode(JSON.stringify(t))));
  out.push({s:b64(salt),i:b64(iv),d:b64(ct)}); claves.push({id:t.id,titulo:t.titulo,clave});
 }
 fs.writeFileSync(process.argv[3],JSON.stringify({cifrados:out,claves,plano:T},null,1));
 console.log(claves);
})();
