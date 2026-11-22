const DUR=13.5;
function draw(ctx,t){bgDark(ctx);
 const gy=1380;ctx.fillStyle='#020317';ctx.fillRect(0,gy+120,W,H);
 const run=t<9;const px=run?760+Math.sin(t*2)*30:780;const leg=Math.sin(t*16);
 if(t<9){person(ctx,px,gy,1.05,'#E8ECFF',{mood:'nerv',arms:0.5+leg*0.3,leg:leg},t);pill(ctx,'MI SUELDO',px,gy-260,32,C.green);
 [['TARJETAS',C.orange,0],['COMPRAS','#D61F4C',1],['IMPUESTOS','#8E2BD6',2]].forEach(([l,c,i])=>{const ch=eo(prog(t,0.8+i*0.6,1.6+i*0.6));const x=lerp(-260,130+i*190,ch)+Math.sin(t*9+i)*12;monster(ctx,x*1.0,gy-60,1.25-i*0.08,c,l,t+i);});}
 // pared de método
 const wall=eo(prog(t,8.6,9.2));if(wall>0&&t<11.8){ctx.save();ctx.globalAlpha=wall;ctx.fillStyle=C.navy;rr(ctx,400,gy-520+(1-wall)*300,170,650,14);ctx.fill();ctx.restore();text(ctx,'MÉTODO',485,gy-200,36,'#fff',900,'center',wall,'Inter Display');person(ctx,780,gy,1.05,'#E8ECFF',{mood:'happy',arms:1},t);pill(ctx,'MI SUELDO',780,gy-260,32,C.green,'#fff',wall);}
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.6,9));hook(ctx,['Mi',['estado financiero','o'],'cada quincena:'],300,h1,{size:86});
 const m1=eo(prog(t,9,9.5))*(1-prog(t,11.5,11.8));hook(ctx,['Deja de huir:',['ponle método','o'],'a tu dinero'],300,m1,{size:86});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
