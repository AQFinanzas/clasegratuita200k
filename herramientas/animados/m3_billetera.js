const DUR=13.5;
function draw(ctx,t){bgDark(ctx);
 const cx=540,cy=1050;ctx.save();ctx.translate(cx,cy);ctx.scale(1.5,1.5);ctx.translate(-cx,-cy);
 // billetera
 ctx.fillStyle='#7A4A2A';rr(ctx,cx-150,cy-100,300,200,26);ctx.fill();ctx.fillStyle='#5E3720';rr(ctx,cx+40,cy-40,120,80,18);ctx.fill();ctx.fillStyle='#E0B04A';ctx.beginPath();ctx.arc(cx+95,cy,14,0,7);ctx.fill();
 // nivel de la billetera
 const lvl=t<9?1-0.85*prog(t,1.5,8.5):0.15;ctx.fillStyle='#ffffff22';rr(ctx,cx-150,cy+130,300,22,11);ctx.fill();ctx.fillStyle=lvl>0.4?C.green:C.orange;rr(ctx,cx-150,cy+130,300*lvl,22,11);ctx.fill();ctx.restore();
 // ingresos: monedas caminando lento desde la izquierda
 for(let i=0;i<4;i++){const ph=((t*0.07)+i*0.25)%1;const x=lerp(-40,cx-240,ph),y=cy+90;coin(ctx,x,y,30);ctx.save();ctx.strokeStyle='#FFC233';ctx.lineWidth=5;const st=Math.sin(t*6+i)*8;ctx.beginPath();ctx.moveTo(x-8,y+22);ctx.lineTo(x-8+st,y+40);ctx.moveTo(x+8,y+22);ctx.lineTo(x+8-st,y+40);ctx.stroke();ctx.restore();}
 pill(ctx,'INGRESOS',190,cy+290,38,C.green);
 // gastos: billetes volando rápido a la derecha
 for(let i=0;i<7;i++){const ph=((t*0.55)+i/7)%1;if(t<1.5)continue;const x=lerp(cx+100,W+120,ph),y=cy-80-ph*480+Math.sin(ph*12+i)*40;bill(ctx,x,y,140,1-ph*0.3,Math.sin(t*5+i)*0.5);ctx.save();ctx.fillStyle='#ffffffcc';const fl=Math.sin(t*30+i)*16;ctx.beginPath();ctx.ellipse(x-20,y-30,26,10+fl*0.3,-0.6,0,7);ctx.ellipse(x+20,y-30,26,10-fl*0.3,0.6,0,7);ctx.fill();ctx.restore();}
 pill(ctx,'GASTOS',870,cy+290,38,C.orange);
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.8,9.2));hook(ctx,['El dinero entra',['caminando…','b'],'y sale',['volando','o']],300,h1,{size:86});
 const m1=eo(prog(t,9.1,9.6))*(1-prog(t,11.5,11.8));hook(ctx,['No es solo ganar más:',['frena la salida','o'],'e invierte lo que queda'],330,m1,{size:72});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
