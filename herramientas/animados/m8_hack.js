const DUR=13.5;
function card(ctx,x,y,s,rot){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(s,s);const g=ctx.createLinearGradient(-170,-105,170,105);g.addColorStop(0,'#2A94F8');g.addColorStop(1,'#01005A');ctx.fillStyle=g;rr(ctx,-170,-105,340,210,22);ctx.fill();ctx.fillStyle='#FFC233';rr(ctx,-130,-45,60,44,8);ctx.fill();ctx.fillStyle='#fff';ctx.font="700 26px Inter";ctx.fillText('•••• •••• •••• 4417',-130,50);ctx.restore();}
function draw(ctx,t){bgDark(ctx);
 const sw=Math.sin(t*5)*0.15;if(t<9)card(ctx,540,840,1.6,sw);
 ['Mercado','Gasolina','Ropa','Restaurante','Regalos'].forEach((n,i)=>{const t0=1.4+i*0.7;const a=eo(prog(t,t0,t0+0.3))*(1-prog(t,8.6,9));pill(ctx,'✔ '+n,i%2?760:320,1100+i*72,34,'#ffffff22','#fff',a);});
 const it=prog(t,5.2,8.4);if(it>0&&t<9){const v=Math.round(lerp(0,1340,ease(it)));pill(ctx,'Deuda: $'+v.toLocaleString('es-CO'),540,1470,42,'#D61F4C','#fff',Math.min(1,it*4));text(ctx,'+ intereses de ~28 % al año',540,1545,30,'#FFB4C2',700,'center',Math.min(1,it*4)*(1-prog(t,8.6,9)));}
 stamp(ctx,'NO ES UN HACK',540,840,70,prog(t,7.4,7.8)*(1-prog(t,8.6,9)),-0.15,'#D61F4C');
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.6,9));hook(ctx,['Pagar todo con tarjeta','y abonar después:',['“el verdadero hack”','o']],280,h1,{size:74});
 const m1=eo(prog(t,9,9.5))*(1-prog(t,11.5,11.8));hook(ctx,['El hack real:',['gasta menos','o'],['de lo que ganas','o'],'e invierte la diferencia'],300,m1,{size:76});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
