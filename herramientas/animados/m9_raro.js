const DUR=13.5;
function draw(ctx,t){bgDark(ctx);
 // sofá
 const sy=1320;ctx.fillStyle='#3B3F6B';rr(ctx,140,sy,800,170,40);ctx.fill();ctx.fillStyle='#4C5190';rr(ctx,110,sy-60,140,230,40);ctx.fill();rr(ctx,830,sy-60,140,230,40);ctx.fill();
 // persona acostada
 ctx.save();ctx.translate(600,sy-30);ctx.rotate(-Math.PI/2);stick(ctx,0,0,0.95,'#E8ECFF',{arms:0.05});ctx.restore();ctx.save();ctx.translate(560+112,sy-20);ctx.restore();
 ctx.save();ctx.translate(600-150*0.95,sy-30);ctx.rotate(-Math.PI/2);face(ctx,0,0,0.95,'ok',t);ctx.restore();
 const th=eo(prog(t,1.6,2.1))*(1-prog(t,8.6,9));if(th>0){ctx.save();ctx.globalAlpha=th;ctx.fillStyle='#fff';rr(ctx,180,720,720,340,26);ctx.fill();ctx.restore();
  text(ctx,'TARJETA DE CRÉDITO',540,775,30,'#667',800,'center',th);text(ctx,'Pago mínimo',230,870,44,C.navy,700,'left',th);text(ctx,'$45',850,870,50,C.green,900,'right',th,'Inter Display');text(ctx,'Pago total',230,970,44,C.navy,700,'left',th);text(ctx,'$1.340',850,970,50,'#D61F4C',900,'right',th,'Inter Display');
  ctx.save();ctx.globalAlpha=th;ctx.fillStyle='#fff';[[520,1100,16],[500,1150,10]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill();});ctx.restore();}
 pill(ctx,'¿Pago el mínimo y ya…?',540,1510,38,C.orange,'#fff',eo(prog(t,4.5,5))*(1-prog(t,8.6,9)));
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.6,9));hook(ctx,['— Oye, te noto raro.',['Yo:','o']],320,h1,{size:84});
 const m1=eo(prog(t,9,9.5))*(1-prog(t,11.5,11.8));hook(ctx,['El pago mínimo',['es la trampa','o'],'Paga el total y crea',['excedente','o']],300,m1,{size:78});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
