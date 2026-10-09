/* Homepage interactions start after the browser has had a first paint opportunity.
   The deferred film library runs first; event handlers remain installed for later use. */
requestAnimationFrame(function(){
  setTimeout(function(){
(function(){
  var wk=document.querySelector('#chapter5 .wk');
  if(!wk)return;
  var rows=[].slice.call(wk.querySelectorAll('.wk-row'));
  var sub=wk.querySelector('.wk-subtotal');
  var total=wk.querySelector('.wk-total');
  var sumEl=wk.querySelector('.wk-sum');
  var tl=wk.querySelector('.wk-tl');
  var then=wk.querySelector('.wk-then');
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fin(){
    rows.forEach(function(r){r.classList.add('is-in','is-note');});
    if(sub)sub.classList.add('is-in');
    if(total)total.classList.add('is-in');
    if(then)then.classList.add('is-in');
    wk.classList.add('is-final');
    if(sumEl)sumEl.textContent='$330';
    if(tl)tl.textContent="What's left";
  }
  if(reduce){fin();return;}
  wk.classList.add('anim');
  if(tl)tl.textContent="What's left so far";
  if(sumEl)sumEl.textContent='$2,650';
  function money(n){return '$'+Math.round(n).toLocaleString('en-US');}
  function count(from,to,ms){
    if(!sumEl)return;
    var steps=Math.max(1,Math.round(ms/22)),i=0;
    var t=setInterval(function(){i++;var p=i/steps,e=1-Math.pow(1-p,3);
      sumEl.textContent=money(from+(to-from)*e);
      if(i>=steps){sumEl.textContent=money(to);clearInterval(t);}
    },22);
  }
  function inn(el){if(el)el.classList.add('is-in');}
  function note(el){if(el)el.classList.add('is-note');}
  function run(){
    [[200,function(){inn(rows[0]);}],
     [700,function(){note(rows[0]);}],
     [1900,function(){inn(rows[1]);}],
     [2400,function(){note(rows[1]);}],
     [3600,function(){inn(sub);}],
     [4300,function(){inn(total);}],
     [4700,function(){inn(rows[2]);}],
     [4900,function(){count(2650,2240,900);}],
     [5250,function(){note(rows[2]);}],
     [6600,function(){inn(rows[3]);}],
     [6800,function(){count(2240,2090,800);}],
     [7150,function(){note(rows[3]);}],
     [8400,function(){inn(rows[4]);}],
     [8950,function(){note(rows[4]);}],
     [9100,function(){count(2090,330,1600);}],
     [11200,function(){wk.classList.add('is-final');if(tl)tl.textContent="What's left";}],
     [11700,function(){inn(then);}]
    ].forEach(function(s){setTimeout(s[1],s[0]);});
  }
  var done=false;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&!done){done=true;run();io.disconnect();}
  });},{threshold:.4});
  io.observe(wk);
})();

mountInlineFilm(document.getElementById('filmSection'), {
    accent:'#2596BE', diveScroll:1.7, crossfade:0.2,
    sections:[
      {id:'con',label:'Contractor',still:'film/con.webp',stillFallback:'film/con.jpg',clip:'film/vid/con.mp4',clipMobile:'film/vid/con-m.mp4',accent:'#2596BE',eyebrow:'Contractor',title:"You're not going to grow by renting out your time.",body:"Lunch on your tailgate. Your quote sends itself. Your week fills in. No picking up the phone since seven."},
      {id:'law',label:'Lawyer',still:'film/law.webp',stillFallback:'film/law.jpg',clip:'film/vid/law.mp4',clipMobile:'film/vid/law-m.mp4',accent:'#2596BE',eyebrow:'Lawyer',title:'For the owner whose number one value is freedom.',body:"Your time, back in your hands."},
      {id:'cli',label:'Clinic',still:'film/cli.webp',stillFallback:'film/cli.jpg',clip:'film/vid/cli.mp4',clipMobile:'film/vid/cli-m.mp4',accent:'#2596BE',eyebrow:'Clinic',title:'A calm mind, a packed calendar, a business you remember why you loved.',body:"A real lunch, stethoscope on the hook, waiting room still full. No longer the last one out."},
      {id:'fac',label:'Factory',still:'film/fac.webp',stillFallback:'film/fac.jpg',clip:'film/vid/fac.mp4',clipMobile:'film/vid/fac-m.mp4',accent:'#2596BE',eyebrow:'Factory',title:'You built it to run without you.',body:"Your coat on. Your line still moving. No production sign-offs in months."}
    ]
  });

(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nav=document.getElementById('nav');
  if(nav)addEventListener('scroll',function(){nav.classList.toggle('scrolled',scrollY>40);});

  /* mobile nav */
  var burger=document.getElementById('navBurger'),navMenu=document.getElementById('navMenu');
  if(burger&&navMenu){
    burger.setAttribute('aria-expanded','false');
    burger.addEventListener('click',function(){var o=navMenu.classList.toggle('open');burger.classList.toggle('open',o);burger.setAttribute('aria-expanded',o?'true':'false');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&navMenu.classList.contains('open')){navMenu.classList.remove('open');burger.classList.remove('open');burger.setAttribute('aria-expanded','false');}});
    navMenu.querySelectorAll('.nav-trigger').forEach(function(t){
      t.addEventListener('click',function(){
        if(window.innerWidth>600&&window.matchMedia('(hover:hover)').matches) return; // desktop uses hover; hoverless tablets tap
        var item=t.closest('.nav-item');var wasOpen=item.classList.contains('open');
        navMenu.querySelectorAll('.nav-item').forEach(function(i){i.classList.remove('open');});
        if(!wasOpen) item.classList.add('open');navMenu.querySelectorAll('.nav-trigger').forEach(function(b){b.setAttribute('aria-expanded',String(b.closest('.nav-item').classList.contains('open')));});
      });
    });
    navMenu.querySelectorAll('.drop-link, .nav-cta').forEach(function(l){l.addEventListener('click',function(){navMenu.classList.remove('open');burger.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
  }

  /* turnstile logo */
  var words=['Leads','Found','Busy','Margins','Media','Booked','It','Scale'];
  var tw=document.getElementById('tword'),ti=0,cur=tw?tw.querySelector('span.in'):null;
  if(tw&&!tw.dataset.mounted){tw.dataset.mounted='1';
  var meter=document.createElement('span');meter.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font-style:italic;opacity:0;transform:none';tw.appendChild(meter);function widthOf(w){meter.textContent=w;return Math.ceil(meter.getBoundingClientRect().width)+2;}function showWord(i){var s=document.createElement('span');s.textContent=words[i];s.classList.add('in');tw.appendChild(s);if(cur){var o=cur;o.classList.remove('in');o.classList.add('out');setTimeout(function(){o.remove();},600);}cur=s;}
  var twMax=0;for(var wi=0;wi<words.length;wi++){twMax=Math.max(twMax,widthOf(words[wi]));}tw.style.width=twMax+'px';if(!cur)showWord(0); if(!reduce && words.length>1) setInterval(function(){var nm=document.getElementById('navMenu');if(document.hidden||(nm&&nm.classList.contains('open')))return;ti=(ti+1)%words.length;showWord(ti);},2400);
  function measureLogo(){var m2=0;for(var wj=0;wj<words.length;wj++){m2=Math.max(m2,widthOf(words[wj]));}tw.style.width=m2+'px';}
  if(document.fonts){document.fonts.ready.then(measureLogo);document.fonts.addEventListener('loadingdone',measureLogo);}
  }

  /* reveals */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.16,rootMargin:'0px 0px -7% 0px'});
  document.querySelectorAll('.rv:not(.in)').forEach(function(el){io.observe(el);});
  // Failsafe: IO misses on anchor jumps and some iOS scroll patterns left
  // sections invisible (blank pricing cards on mobile, 2026-08-24). Reveal
  // anything actually in the viewport, on a timer and on scroll.
  function rvSweep(){if(document.hidden)return;document.querySelectorAll('.rv:not(.in)').forEach(function(el){var r=el.getBoundingClientRect();if(r.top<window.innerHeight*.98&&r.bottom>0)el.classList.add('in');});}
  setTimeout(rvSweep,900);setTimeout(rvSweep,2500);
  var rvTick=false;function rvOnScroll(){if(rvTick)return;rvTick=true;requestAnimationFrame(function(){rvSweep();rvTick=false;});}window.addEventListener('scroll',rvOnScroll,{passive:true});document.addEventListener('scroll',rvOnScroll,{capture:true,passive:true});setInterval(rvSweep,800);

  function onPlay(el,cb){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('play');if(cb)cb();o.unobserve(e.target);}});},{threshold:.18});o.observe(el);}
  function staggerShow(ids,gap,start){ids.forEach(function(id,i){var el=document.getElementById(id);if(el)setTimeout(function(){el.style.opacity=1;},start+i*gap);});}

  /* SCENE 1: type query + reveal AI overview */
  var s1=document.getElementById('s1box');
  if(s1){
    var q="best hvac company in fresno",tEl=document.getElementById('s1type');
    onPlay(s1,function(){
      document.getElementById('s1box').classList.add('play');
      if(reduce){tEl.textContent=q;['s1card','sk1','sk2','sk3','srcLbl','src1','src2','src3','s1ghost'].forEach(function(id){var e=document.getElementById(id);if(e)e.style.opacity=1;});return;}
      var i=0;var t=setInterval(function(){tEl.textContent=q.slice(0,i+1)+(i<q.length-1?'|':'');i++;if(i>=q.length){clearInterval(t);tEl.textContent=q;
        document.getElementById('s1card').style.opacity=1;
        staggerShow(['sk1','sk2','sk3'],110,250);
        staggerShow(['srcLbl'],0,640);
        staggerShow(['src1','src2','src3'],260,760);
        setTimeout(function(){document.getElementById('s1ghost').style.opacity=1;},1900);
      }},72);
    });
  }

  /* SCENE 2: pins + listings */
  var s2=document.getElementById('s2box');
  if(s2){
    ['mp1','mp2','mp3','ml1','ml2','ml3','mdiv','mmore','myou'].forEach(function(id){var e=document.getElementById(id);if(e)e.style.transition='opacity .5s ease, transform .5s cubic-bezier(.2,1.25,.4,1)';});
    onPlay(s2,function(){
      if(reduce){['mp1','mp2','mp3','ml1','ml2','ml3','mdiv','mmore','myou'].forEach(function(id){var e=document.getElementById(id);if(e)e.style.opacity=1;});return;}
      staggerShow(['mp1','mp2','mp3'],170,120);
      staggerShow(['ml1','ml2','ml3'],200,680);
      staggerShow(['mdiv','mmore'],120,1380);
      setTimeout(function(){document.getElementById('myou').style.opacity=1;},1700);
    });
  }

  /* SCENE 3: build swiping cringe reels */
  var s3=document.getElementById('s3box');
  var strip=document.getElementById('reelStrip');
  if(strip){
    var NS='http://www.w3.org/2000/svg';
    var SX=34, SY=22, SW=232, SH=396, cx=SX+SW/2;
    // inject the CapCut text-pop transition keyframes
    var st=document.createElement('style');
    st.textContent='.rhead{transform-box:fill-box;transform-origin:center}.rhead.pop{animation:ccPop .72s cubic-bezier(.18,1.5,.3,1)}@keyframes ccPop{0%{transform:scale(1.7) translateY(10px);opacity:0}40%{opacity:1}62%{transform:scale(.9)}100%{transform:scale(1);opacity:1}}.chromeShimmer{animation:shimmer 2.6s ease-in-out infinite}@keyframes shimmer{0%,100%{opacity:.78}50%{opacity:1}}';
    document.head.appendChild(st);
    // three recognizable CapCut templates, same trend
    var reels=[
      {tpl:'A',city:'FRESNO',bg:'#6f7556',prop:'shades',shirt:'#262626',handle:'@fresno.deals',who:'Fresno business owner',cap:'📍 Fresno business owners ➡ Follow',likes:'64'},
      {tpl:'B',city:'NORTH HOLLYWOOD',bg:'#D7DCE1',prop:'hair',shirt:'#a9c4d6',handle:'@la.homepros',who:'LA home service pro',cap:'📍 North Hollywood living ➡ Follow',likes:'205'},
      {tpl:'C',city:'PHOENIX, AZ',bg:'#8C9aa6',prop:'cap',shirt:'#dbe0e5',handle:'@phx.homes',who:'Phoenix homeowner',cap:'📍 Phoenix home owners ➡ Follow',likes:'173'}
    ];
    function el(tag,attrs,parent){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);(parent||strip).appendChild(e);return e;}
    function big(parent,x,y,s,fill,fs,outline,ow,extra){var a={x:x,y:y,'text-anchor':'middle','font-family':'var(--sans)','font-weight':'900','font-size':fs,fill:fill,style:'paint-order:stroke;stroke:'+(outline||'#000')+';stroke-width:'+(ow||fs*0.15)+'px;stroke-linejoin:round'};if(extra)for(var k in extra)a[k]=extra[k];var e=el('text',a,parent);e.textContent=s;return e;}
    function person(parent,oy,prop,shirt){
      var skin='#b08d72';
      el('rect',{x:cx-50,y:oy+166,width:100,height:84,rx:24,fill:shirt||'#3a3a3a'},parent); // shirt/shoulders
      el('path',{d:'M'+(cx-14)+' '+(oy+166)+' L'+cx+' '+(oy+184)+' L'+(cx+14)+' '+(oy+166)+' Z',fill:'rgba(255,255,255,.16)'},parent); // collar
      el('rect',{x:cx-10,y:oy+150,width:20,height:22,rx:8,fill:skin},parent); // neck
      el('ellipse',{cx:cx,cy:oy+124,rx:27,ry:31,fill:skin},parent); // head
      el('circle',{cx:cx-27,cy:oy+128,r:5,fill:skin},parent);el('circle',{cx:cx+27,cy:oy+128,r:5,fill:skin},parent); // ears
      if(prop==='hair'){
        el('path',{d:'M'+(cx-31)+' '+(oy+126)+' q-2 -44 31 -44 q33 0 31 44 q-8 -24 -31 -24 q-23 0 -31 24 z',fill:'#3a2d24'},parent);
        el('rect',{x:cx-33,y:oy+114,width:12,height:78,rx:6,fill:'#3a2d24'},parent);el('rect',{x:cx+21,y:oy+114,width:12,height:78,rx:6,fill:'#3a2d24'},parent);
      } else {
        el('path',{d:'M'+(cx-28)+' '+(oy+112)+' q28 -32 56 0 q-12 -14 -28 -14 q-16 0 -28 14 z',fill:'#2a2018'},parent);
      }
      if(prop==='cap'){el('path',{d:'M'+(cx-31)+' '+(oy+106)+' q31 -20 62 0 l5 7 q-36 -9 -72 0 z',fill:'#e9ecef'},parent);}
      if(prop==='shades'){
        el('rect',{x:cx-22,y:oy+118,width:18,height:12,rx:4,fill:'#15110a'},parent);el('rect',{x:cx+4,y:oy+118,width:18,height:12,rx:4,fill:'#15110a'},parent);el('rect',{x:cx-4,y:oy+122,width:8,height:3,fill:'#15110a'},parent);
      } else {
        el('circle',{cx:cx-9,cy:oy+121,r:2.6,fill:'#2a2018'},parent);el('circle',{cx:cx+9,cy:oy+121,r:2.6,fill:'#2a2018'},parent);
      }
      el('path',{d:'M'+cx+' '+(oy+126)+' l-2 8 l4 0',fill:'none',stroke:'rgba(0,0,0,.16)','stroke-width':'1.4','stroke-linecap':'round','stroke-linejoin':'round'},parent); // nose
      el('path',{d:'M'+(cx-8)+' '+(oy+140)+' q8 6 16 0',fill:'none',stroke:'#7a5440','stroke-width':'2','stroke-linecap':'round'},parent); // mouth
      if(prop!=='hair'){el('path',{d:'M'+(cx-17)+' '+(oy+135)+' q17 24 34 0 q-17 11 -34 0 z',fill:'rgba(42,32,24,.45)'},parent);} // beard
    }
    var headGroups=[];
    function buildReel(r,oy){
      el('rect',{x:SX,y:oy,width:SW,height:SH,fill:r.bg}); // bg
      person(strip,oy,r.prop,r.shirt);
      // dark gradient-ish base under text for legibility
      el('rect',{x:SX,y:oy+SH-150,width:SW,height:150,fill:'rgba(0,0,0,.12)'});
      // headline group (animates in like a CapCut text reveal)
      var h=el('g',{class:'rhead'});headGroups.push(h);
      if(r.tpl==='A'){
        el('text',{x:cx,y:oy+176,'text-anchor':'middle','font-size':22},h).textContent='📍';
        big(h,cx,oy+216,r.city,'#FFE000',40,'#15110a',6.5);
        big(h,cx,oy+250,'BUSINESS','#fff',27,'#15110a',4.6);
        big(h,cx,oy+278,'OWNERS','#fff',27,'#15110a',4.6);
      } else if(r.tpl==='B'){
        // the iconic "This is what ___ living" chrome template
        var t1=el('text',{x:SX+24,y:oy+150,'font-family':'var(--display)','font-style':'italic','font-size':22,'font-weight':'600',fill:'#15110a'},h);t1.textContent='This is';
        big(h,cx,oy+196,'what','#D2D7DD',44,'#9aa3ad',3).setAttribute('class','chromeShimmer');
        big(h,cx,oy+228,r.city,'#fff',17,'#15110a',3);
        var lv=big(h,cx,oy+274,'living','#5FD6CB',46,'#0e6b63',3,{'font-family':'var(--display)','font-style':'italic'});lv.setAttribute('class','chromeShimmer');
      } else {
        // auto-caption stutter template
        big(h,cx,oy+196,"PHOENIX",'#fff',34,'#15110a',5.4);
        el('text',{x:cx-78,y:oy+240,'text-anchor':'middle','font-size':22},h).textContent='📍';
        big(h,cx+8,oy+241,'HOME OWNERS','#fff',22,'#15110a',4);
      }
      // handle + persona (top-left)
      el('text',{x:SX+14,y:oy+30,fill:'#fff','font-size':13,'font-weight':'800','font-family':'var(--sans)'}).textContent=r.handle;
      el('text',{x:SX+14,y:oy+45,fill:'rgba(255,255,255,.82)','font-size':10,'font-weight':'600','font-family':'var(--mono)'}).textContent=r.who;
      // explicit CapCut template sticker (the call-out)
      el('rect',{x:SX+14,y:oy+54,width:128,height:21,rx:10,fill:'rgba(0,0,0,.6)'});
      el('text',{x:SX+24,y:oy+68,fill:'#fff','font-size':9.5,'font-weight':'700','font-family':'var(--mono)'}).textContent='CapCut template';
      // follow button
      el('rect',{x:SX+SW-64,y:oy+18,width:52,height:22,rx:11,fill:'#FF2D55'});el('text',{x:SX+SW-38,y:oy+33,'text-anchor':'middle',fill:'#fff','font-size':10,'font-weight':'700','font-family':'var(--sans)'}).textContent='Follow';
      // bottom caption (recognizable format)
      el('text',{x:SX+12,y:oy+336,fill:'#fff','font-size':9.5,'font-weight':'600','font-family':'var(--sans)'}).textContent=r.cap;
      // CapCut watermark (the real tell, bottom-left)
      el('rect',{x:SX+12,y:oy+350,width:84,height:22,rx:6,fill:'rgba(0,0,0,.62)'});
      el('path',{d:'M'+(SX+23)+' '+(oy+355)+' l9 6 l-9 6 z',fill:'#fff'});
      el('text',{x:SX+37,y:oy+366,fill:'#fff','font-size':11,'font-weight':'700','font-family':'var(--sans)'}).textContent='CapCut';
      // like / comment rail
      el('text',{x:SX+SW-22,y:oy+292,'text-anchor':'middle',fill:'#fff','font-size':20}).textContent='♥';
      el('text',{x:SX+SW-22,y:oy+307,'text-anchor':'middle',fill:'#fff','font-size':10,'font-weight':'700'}).textContent=r.likes;
      el('text',{x:SX+SW-22,y:oy+330,'text-anchor':'middle',fill:'#fff','font-size':15}).textContent='💬';
      el('text',{x:SX+SW-22,y:oy+345,'text-anchor':'middle',fill:'#fff','font-size':10,'font-weight':'700'}).textContent='4';
    }
    reels.forEach(function(r,i){buildReel(r,SY+i*SH);});
    function popHead(i){var h=headGroups[i];if(!h)return;h.classList.remove('pop');void h.getBBox();h.classList.add('pop');}
    var hint=document.getElementById('swipeHint');
    onPlay(s3,function(){
      s3.classList.add('play');
      if(reduce) return;
      popHead(0);
      strip.style.transition='transform .55s cubic-bezier(.5,0,.2,1)';
      var pos=0,n=reels.length;
      setInterval(function(){
        pos=(pos+1)%n;
        strip.style.transform='translateY('+(-pos*SH)+'px)';
        if(hint){hint.style.opacity=0;hint.style.transition='opacity .3s';setTimeout(function(){hint.style.opacity=1;},600);}
        setTimeout(function(){popHead(pos);},560);
      },2200);
    });
  }

  /* SCENE 4: build iPhone recents (red missed) */
  var s4=document.getElementById('s4box');
  var rows=document.getElementById('callRows');
  if(rows){
    var NS4='http://www.w3.org/2000/svg';
    var calls=[
      {name:'(559) 221-0094',sub:'Missed · 9:42 AM',missed:true},
      {name:'Maria G. · kitchen',sub:'Missed · 9:08 AM',missed:true},
      {name:'(559) 348-7720',sub:'Missed · 8:51 AM',missed:true},
      {name:'Dave (repeat client)',sub:'Missed · Yesterday',missed:true}
    ];
    var startY=102, rh=44, x0=58, xr=270;
    calls.forEach(function(c,i){
      var y=startY+i*rh;
      var g=document.createElementNS(NS4,'g');g.setAttribute('class','an');g.setAttribute('id','call'+i);g.style.transition='opacity .45s ease';
      // phone icon (red down-arrow for missed)
      var icg=document.createElementNS(NS4,'g');icg.setAttribute('transform','translate('+(x0-3)+' '+(y-13)+') scale(0.62)');icg.setAttribute('fill',c.missed?'var(--gred)':'var(--ggreen)');
      var ph=document.createElementNS(NS4,'path');ph.setAttribute('d','M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.5.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C9.6 21 3 14.4 3 6c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.5.1.3 0 .7-.2 1z');icg.appendChild(ph);g.appendChild(icg);
      var nm=document.createElementNS(NS4,'text');nm.setAttribute('x',x0+26);nm.setAttribute('y',y);nm.setAttribute('font-family','var(--sans)');nm.setAttribute('font-size','13');nm.setAttribute('font-weight','600');nm.setAttribute('fill',c.missed?'var(--gred)':'var(--ink)');nm.textContent=c.name;g.appendChild(nm);
      var sb=document.createElementNS(NS4,'text');sb.setAttribute('x',x0+26);sb.setAttribute('y',y+14);sb.setAttribute('font-family','var(--mono)');sb.setAttribute('font-size','9');sb.setAttribute('fill','var(--faint)');sb.textContent=c.sub;g.appendChild(sb);
      var ln=document.createElementNS(NS4,'line');ln.setAttribute('x1',x0);ln.setAttribute('y1',y+24);ln.setAttribute('x2',xr-4);ln.setAttribute('y2',y+24);ln.setAttribute('stroke','var(--line-soft)');g.appendChild(ln);
      var info=document.createElementNS(NS4,'text');info.setAttribute('x',xr-2);info.setAttribute('y',y);info.setAttribute('text-anchor','end');info.setAttribute('font-family','var(--sans)');info.setAttribute('font-size','13');info.setAttribute('fill','var(--gblue)');info.textContent='ⓘ';g.appendChild(info);
      rows.appendChild(g);
    });
    onPlay(s4,function(){
      s4.classList.add('play');
      if(reduce){calls.forEach(function(_,i){document.getElementById('call'+i).style.opacity=1;});['missTab','noteMsg','noteRev'].forEach(function(id){document.getElementById(id).style.opacity=1;});return;}
      document.getElementById('missTab').style.opacity=1;
      calls.forEach(function(_,i){setTimeout(function(){document.getElementById('call'+i).style.opacity=1;},150+i*160);});
      setTimeout(function(){document.getElementById('noteMsg').style.opacity=1;},1200);
      setTimeout(function(){document.getElementById('noteRev').style.opacity=1;},1600);
    });
  }

  /* FAQ accordion */
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click',function(){
      var item=q.closest('.faq-item');var wasOpen=item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function(i){i.classList.remove('open');});
      if(!wasOpen)item.classList.add('open');
    });
  });

  /* CTA scroll */
  document.querySelectorAll('.tbtn').forEach(function(b){b.addEventListener('click',function(ev){ev.preventDefault();if(b.hasAttribute('data-cal')){window.open('https://calendar.app.google/eQvwG6TeVDq5GCG7A','_blank','noopener');}else{document.getElementById('audit').scrollIntoView({behavior:'smooth'});}});});
})();

/* Before/after business dashboard: revenue, pipeline influence, lead quality, acquisition cost */
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS='http://www.w3.org/2000/svg';
  var svg=document.getElementById('baDash'); if(!svg) return;
  function E(t,a,p){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e;}
  E('rect',{x:0,y:0,width:1000,height:540,rx:18,fill:'var(--paper)'});
  function card(ox,oy,title,sub){
    E('rect',{x:ox,y:oy,width:476,height:246,rx:16,fill:'#fff',stroke:'var(--line-soft)'});
    E('text',{x:ox+28,y:oy+36,'font-family':'var(--mono)','font-size':12,'letter-spacing':'.12em',fill:'var(--faint)'}).textContent=title;
    if(sub)E('text',{x:ox+28,y:oy+56,'font-family':'var(--sans)','font-size':13,fill:'var(--ink-soft)'}).textContent=sub;
  }
  var anims=[], resets=[];

  /* Q1 REVENUE: rising area chart */
  (function(){
    var ox=16,oy=16,x0=ox+30,x1=ox+448,base=oy+214;
    card(ox,oy,'REVENUE',null);
    var defs=E('defs',{}),cp=E('clipPath',{id:'revClip'},defs);
    var cr=E('rect',{x:x0,y:oy+62,width:0,height:base-(oy+62)+6},cp);
    E('line',{x1:x0,y1:base,x2:x1,y2:base,stroke:'var(--line-soft)'});
    var xs=[x0,x0+(x1-x0)*0.2,x0+(x1-x0)*0.4,x0+(x1-x0)*0.6,x0+(x1-x0)*0.8,x1];
    var bef=[base-18,base-14,base-20,base-13,base-18,base-12], aft=[base-20,base-42,base-60,base-86,base-110,base-134];
    var bp='M'+xs[0]+' '+bef[0]; for(var i=1;i<6;i++)bp+=' L'+xs[i]+' '+bef[i];
    E('path',{d:bp,fill:'none',stroke:'#cfc7b6','stroke-width':2,'stroke-dasharray':'5 5'});
    E('text',{x:x1,y:bef[5]-7,'text-anchor':'end','font-family':'var(--mono)','font-size':10,fill:'#b3a997'}).textContent='before';
    var ap='M'+xs[0]+' '+aft[0]; for(var j=1;j<6;j++)ap+=' L'+xs[j]+' '+aft[j];
    E('path',{d:ap+' L'+x1+' '+base+' L'+x0+' '+base+' Z',fill:'rgba(255,77,28,.12)','clip-path':'url(#revClip)'});
    E('path',{d:ap,fill:'none',stroke:'var(--accent)','stroke-width':3,'stroke-linecap':'round','stroke-linejoin':'round','clip-path':'url(#revClip)'});
    var up=E('text',{x:x1,y:oy+36,'text-anchor':'end','font-family':'var(--sans)','font-size':13,'font-weight':800,fill:'var(--good)',opacity:0});up.textContent='▲ growing';
    anims.push(function(){cr.style.transition='width 1.1s cubic-bezier(.2,.7,.2,1)';cr.setAttribute('width',x1-x0);setTimeout(function(){up.style.transition='opacity .4s';up.setAttribute('opacity',1);},900);});
    resets.push(function(){cr.style.transition='none';cr.setAttribute('width',0);up.setAttribute('opacity',0);});
  })();

  /* Q2 PIPELINE INFLUENCE: growing bars */
  (function(){
    var ox=508,oy=16,base=oy+214,n=7,bw=32,x0=ox+34,gap=((ox+448)-x0-bw)/(n-1);
    card(ox,oy,'PIPELINE INFLUENCE',null);
    var bef=[16,20,18,24,20,26,22], aft=[28,42,54,70,88,106,122], bars=[];
    for(var i=0;i<n;i++){
      var x=x0+i*gap;
      E('rect',{x:x,y:base-bef[i],width:bw,height:bef[i],rx:3,fill:'#e7ddc8'});
      var r=E('rect',{x:x,y:base-aft[i],width:bw,height:aft[i],rx:3,fill:'var(--accent)'});
      r.style.transformBox='fill-box';r.style.transformOrigin='bottom';r.style.transform='scaleY(0)';
      bars.push(r);
    }
    E('line',{x1:ox+28,y1:base,x2:ox+448,y2:base,stroke:'var(--line-soft)'});
    var up=E('text',{x:ox+448,y:oy+36,'text-anchor':'end','font-family':'var(--sans)','font-size':13,'font-weight':800,fill:'var(--good)',opacity:0});up.textContent='▲ fuller';
    anims.push(function(){bars.forEach(function(r,i){setTimeout(function(){r.style.transition='transform .6s cubic-bezier(.2,1,.3,1)';r.style.transform='scaleY(1)';},i*80);});setTimeout(function(){up.style.transition='opacity .4s';up.setAttribute('opacity',1);},n*80+300);});
    resets.push(function(){bars.forEach(function(r){r.style.transition='none';r.style.transform='scaleY(0)';});up.setAttribute('opacity',0);});
  })();

  /* Q3 LEAD QUALITY: score climbing */
  (function(){
    var ox=16,oy=278;
    card(ox,oy,'LEAD QUALITY','junk leads, to ready to buy');
    var score=E('text',{x:ox+28,y:oy+150,'font-family':'var(--display)','font-weight':500,'font-size':66,fill:'var(--ink)','letter-spacing':'-.02em'});score.textContent='38';
    E('text',{x:ox+30,y:oy+174,'font-family':'var(--mono)','font-size':11,fill:'var(--faint)'}).textContent='quality score / 100';
    var tx=ox+28,tw=420,ty=oy+196;
    E('rect',{x:tx,y:ty,width:tw,height:12,rx:6,fill:'#efe7d6'});
    E('rect',{x:tx,y:ty,width:tw*0.38,height:12,rx:6,fill:'#cfc7b6'});
    var fill=E('rect',{x:tx,y:ty,width:tw*0.38,height:12,rx:6,fill:'var(--good)'});
    anims.push(function(){fill.style.transition='width 1.1s ease';fill.setAttribute('width',tw*0.86);var s=38,t=86,st=setInterval(function(){s+=Math.ceil((t-s)/6);if(s>=t){s=t;clearInterval(st);}score.textContent=s;},90);});
    resets.push(function(){fill.style.transition='none';fill.setAttribute('width',tw*0.38);score.textContent='38';});
  })();

  /* Q4 CUSTOMER ACQUISITION: cost to win drops */
  (function(){
    var ox=508,oy=278,base=oy+208,bx=ox+300;
    card(ox,oy,'CUSTOMER ACQUISITION','cost to win one customer');
    var cost=E('text',{x:ox+28,y:oy+150,'font-family':'var(--display)','font-weight':500,'font-size':62,fill:'var(--ink)','letter-spacing':'-.02em'});cost.textContent='$195';
    var dn=E('text',{x:ox+30,y:oy+178,'font-family':'var(--sans)','font-size':14,'font-weight':800,fill:'var(--good)',opacity:0});dn.textContent='▼ 39% cheaper';
    E('rect',{x:bx,y:base-118,width:46,height:118,rx:5,fill:'#e7ddc8'});
    E('text',{x:bx+23,y:base+16,'text-anchor':'middle','font-family':'var(--mono)','font-size':9,fill:'var(--faint)'}).textContent='before';
    var ab=E('rect',{x:bx+74,y:base-72,width:46,height:72,rx:5,fill:'var(--good)'});
    ab.style.transformBox='fill-box';ab.style.transformOrigin='bottom';ab.style.transform='scaleY(0)';
    E('text',{x:bx+97,y:base+16,'text-anchor':'middle','font-family':'var(--mono)','font-size':9,fill:'var(--good)'}).textContent='after';
    anims.push(function(){ab.style.transition='transform .7s cubic-bezier(.2,1,.3,1)';ab.style.transform='scaleY(1)';var c=195,t=118,st=setInterval(function(){c-=Math.ceil((c-t)/6);if(c<=t){c=t;clearInterval(st);}cost.textContent='$'+c;},90);setTimeout(function(){dn.style.transition='opacity .4s';dn.setAttribute('opacity',1);},700);});
    resets.push(function(){ab.style.transition='none';ab.style.transform='scaleY(0)';cost.textContent='$195';dn.setAttribute('opacity',0);});
  })();

  function play(){anims.forEach(function(f){f();});setTimeout(function(){resets.forEach(function(f){f();});setTimeout(play,800);},4400);}
  if(reduce){anims.forEach(function(f){f();});}
  else{
    var started=false;
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!started){started=true;play();io2.disconnect();}});},{threshold:.25});
    io2.observe(svg);
  }
})();

(function(){
  if(!/[?&]amgdebug=1/.test(location.search)) return;window.__amgErrs=[];window.addEventListener('error',function(e){window.__amgErrs.push((e.message||'?')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno);});window.addEventListener('unhandledrejection',function(e){window.__amgErrs.push('promise: '+((e.reason&&e.reason.message)||e.reason||'?'));});
  function line(k,v){return '<div><b>'+k+':</b> '+v+'</div>';}
  var d=document.createElement('div');
  d.style.cssText='position:fixed;left:8px;bottom:8px;z-index:99999;background:#000;color:#0f0;font:11px/1.6 monospace;padding:10px 12px;border-radius:8px;max-width:90vw;opacity:.95';
  document.body.appendChild(d);
  function render(){
    var fs=document.getElementById('filmSection');
    var branch='none';
    if(fs){ if(fs.querySelector('.ifilm-pin')) branch='DESKTOP pin'; else if(fs.querySelector('.ifilm-m')) branch='MOBILE stacked'; }
    var revealed=document.querySelectorAll('.ifilm-mscene.in').length, total=document.querySelectorAll('.ifilm-mscene').length;
    var rv=document.querySelectorAll('.rv').length, rvin=document.querySelectorAll('.rv.in').length;
    d.innerHTML=line('innerW x innerH',window.innerWidth+' x '+window.innerHeight)
      +line('dpr',window.devicePixelRatio)
      +line('vv scale/width',(window.visualViewport?window.visualViewport.scale.toFixed(2)+' / '+Math.round(window.visualViewport.width):'n/a'))
      +line('scrollY',Math.round(window.scrollY||window.pageYOffset||0))
      +line('mq max-860',window.matchMedia('(max-width:860px)').matches)
      +line('mq coarse',window.matchMedia('(hover:none) and (pointer:coarse)').matches)
      +line('film branch',branch)
      +line('mscenes in/total',revealed+'/'+total)
      +line('rv in/total',rvin+'/'+rv)
      +line('build','HARDEN-1')+line('errors',(window.__amgErrs&&window.__amgErrs.length?window.__amgErrs.slice(0,3).join(' | '):'none'))+line('UA',navigator.userAgent.slice(0,60));
  }
  setTimeout(render,250);setInterval(render,1000);
})();
  },0);
});
