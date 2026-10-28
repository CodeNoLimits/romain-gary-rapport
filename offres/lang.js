(function(){var bs=document.querySelectorAll('.lang button');
function set(l){document.body.classList.remove('l-he','l-fr','l-en');document.body.classList.add('l-'+l);
document.documentElement.lang=l;document.documentElement.dir=l==='he'?'rtl':'ltr';bs.forEach(function(x){x.classList.toggle('on',x.dataset.l===l)});try{localStorage.setItem('rg-l',l)}catch(e){}}
bs.forEach(function(b){b.onclick=function(){set(b.dataset.l)}});
var q=(location.search.match(/[?&]l=(he|fr|en)/)||[])[1],s=null;try{s=localStorage.getItem('rg-l')}catch(e){}
if(q||s)set(q||s);})();
(function(){var s=document.querySelector('.sticky');if(!s)return;var c=document.querySelector('.code');
function f(){var r=c.getBoundingClientRect();s.classList.toggle('show',scrollY>320&&(r.bottom<0||r.top>innerHeight))}addEventListener('scroll',f,{passive:true});f();})();
