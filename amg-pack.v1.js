(function(){var CFG={"cid": "amirgetsjobs-fresno", "intake": ""};
var P=new URLSearchParams(location.search);
var KEYS=['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','wbraid','gbraid','msclkid'];
var ft={};try{ft=JSON.parse(localStorage.getItem('amg_ft')||'{}')}catch(e){}
var dirty=false;
KEYS.forEach(function(k){var v=P.get(k);if(v&&!ft[k]){ft[k]=v;dirty=true}});
if(!ft.landing){ft.landing=location.pathname;ft.ref=(document.referrer.split('/')[2]||'');ft.ts=Date.now();dirty=true}
if(dirty){try{localStorage.setItem('amg_ft',JSON.stringify(ft))}catch(e){}}
var m=document.cookie.match(/(?:^|; )amg_sid=([^;]+)/);
var SID=m?m[1]:(Date.now().toString(36)+Math.random().toString(36).slice(2,10));
if(!m){document.cookie='amg_sid='+SID+';path=/;max-age=2592000;SameSite=Lax'}
function fire(name,extra){
 var p={page:location.pathname,session_id:SID,landing:ft.landing||'',
  source:ft.utm_source||ft.ref||'direct',medium:ft.utm_medium||''};
 if(ft.gclid){p.gclid=ft.gclid}
 for(var k in (extra||{})){p[k]=extra[k]}
 if(window.gtag){gtag('event',name,p)}
 if(window.plausible){plausible(name,{props:p})}
 if(CFG.intake&&navigator.sendBeacon){try{navigator.sendBeacon(CFG.intake,
  JSON.stringify({client_id:CFG.cid,event:name,ts:Date.now(),props:p}))}catch(e){}}
}
document.addEventListener('click',function(e){
 var a=e.target.closest?e.target.closest('a'):null;if(!a)return;
 var h=a.getAttribute('href')||'';
 if(h.indexOf('tel:')===0){fire('phone_call_click')}
 else if(h.indexOf('sms:')===0){fire('sms_click')}
 else if(h.indexOf('calendly.com')>-1){fire('booking_click')}
},true);
document.querySelectorAll('a[href*="calendly.com"]').forEach(function(a){
 try{var u=new URL(a.href);
  u.searchParams.set('utm_source',ft.utm_source||ft.ref||'website');
  u.searchParams.set('utm_medium',ft.utm_medium||(ft.ref?'referral':'direct'));
  u.searchParams.set('utm_content',location.pathname);
  a.href=u.toString()}catch(e){}
});
document.querySelectorAll('form').forEach(function(f){
 var vals={page:location.pathname,session_id:SID,landing:ft.landing||'',
  source:ft.utm_source||ft.ref||'direct',medium:ft.utm_medium||'',gclid:ft.gclid||''};
 for(var k in vals){if(!vals[k])continue;
  var i=document.createElement('input');i.type='hidden';i.name='amg_'+k;
  i.value=vals[k];f.appendChild(i)}
 f.addEventListener('submit',function(){fire('form_submit')});
});
})();
