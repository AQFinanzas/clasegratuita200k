const DUR=13.5;
function draw(ctx,t){bgDark(ctx);
 // grafico velas
 const x0=90,y0=640,w=900,h=600;ctx.fillStyle='#ffffff0d';rr(ctx,x0,y0,w,h,20);ctx.fill();
 const ent=y0+170,f1=y0+330,f2=y0+470,sl=y0+100;
 [[sl,'Stop loss','#D61F4C'],[ent,'Entrada','#fff'],[f1,'Fase 1',C.green],[f2,'Fase 2',C.green]].forEach(([yy,l,c])=>{ctx.save();ctx.strokeStyle=c;ctx.setLineDash([12,10]);ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x0+20,yy);ctx.lineTo(x0+w-150,yy);ctx.stroke();ctx.restore();text(ctx,l,x0+w-20,yy,30,c,800,'right');});
 const n=Math.floor(clamp(prog(t,0.8,5.5))*12);let p=ent-60;for(let i=0;i<n;i++){const o=p;let c=i<3?p-20+i*10:p+44;if(i==4)c=o-10;c=Math.min(c,f2+10);const hi=Math.min(o,c)-14,lo=Math.max(o,c)+14;const x=x0+50+i*55;ctx.strokeStyle=c>o?'#D61F4C':C.green;ctx.fillStyle=ctx.strokeStyle;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,hi);ctx.lineTo(x,lo);ctx.stroke();ctx.fillRect(x-14,Math.min(o,c),28,Math.max(6,Math.abs(c-o)));p=c;}
 pill(ctx,'EN CORTO',x0+120,y0+40,24,C.navy);
 const hit=prog(t,5.4,5.8);if(hit>0)stamp(ctx,'¡FASE 2!',540,f2-10,56,hit*(1-prog(t,8.7,9.1)),-0.1,C.green);
 // persona bailando + café
 if(t<9.1){const dance=t>5.6;person(ctx,300,1470,0.8,'#E8ECFF',{mood:dance?'happy':'ok',arms:dance?(Math.sin(t*10)>0?1:0.3):0.1},t);
  ctx.fillStyle='#fff';rr(ctx,690,1340,90,100,14);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=10;ctx.beginPath();ctx.arc(785,1385,24,-1.2,1.2);ctx.stroke();ctx.fillStyle='#6B3E26';ctx.fillRect(700,1350,70,16);for(let i=0;i<3;i++){ctx.save();ctx.globalAlpha=0.5;ctx.strokeStyle='#fff';ctx.lineWidth=5;ctx.beginPath();const yy=1320-((t*40+i*20)%50);ctx.moveTo(710+i*25,yy+30);ctx.quadraticCurveTo(720+i*25,yy+15,710+i*25,yy);ctx.stroke();ctx.restore();}
  text(ctx,'(todavía caliente)',735,1480,26,'#9AA0C8',600,'center',prog(t,5.8,6.2));}
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.7,9.1));hook(ctx,['Cuando tu operación',['toca Fase 2','o'],'antes del primer café'],300,h1,{size:76});
 const m1=eo(prog(t,9.1,9.6))*(1-prog(t,11.5,11.8));hook(ctx,['No es suerte:','entrada, stop loss',['y fases','o'],'Eso es método'],300,m1,{size:78});
 disclaimer(ctx,'Ejemplo ilustrativo. Resultados pasados no garantizan resultados futuros.',eo(prog(t,9.1,9.6))*(1-prog(t,11.5,11.8)));
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
