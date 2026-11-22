const DUR=13.5;
const P=[{x:100,l:'MI SUELDO'},{x:280,l:'DOMICILIOS'},{x:460,l:'NETFLIX'},{x:640,l:'PAPITAS'},{x:820,l:'SALIDAS'}];
function draw(ctx,t){bgDark(ctx);
 const WY=1300;
 // pilares
 P.forEach((p,i)=>{ctx.fillStyle='#3B3F6B';rr(ctx,p.x-62,WY-110,124,600,12);ctx.fill();ctx.fillStyle='#5A5F96';ctx.fillRect(p.x-62,WY-110,124,16);});
 // ultimo pilar vacio
 pill(ctx,'DÍA 15',1000,WY+40,26,C.orange,'#fff',prog(t,6.5,7));
 // persona saltando
 let x,y,mood='happy';const hopT=1.4,dt=1.15;let k=Math.min(4,Math.max(0,Math.floor((t-hopT)/dt)));let f=clamp((t-hopT-k*dt)/0.75);
 if(t<hopT){x=P[0].x;y=WY-110;}else if(t<hopT+4*dt){const a=P[k],b=P[Math.min(4,k+1)];x=lerp(a.x,b.x,ease(f));y=WY-110-Math.sin(f*Math.PI)*170;}
 else{const g=clamp((t-(hopT+4*dt))/1.4);x=lerp(P[4].x,1000,g);y=WY-110-Math.sin(Math.min(g,0.5)*Math.PI)*170+ (g>0.5?(g-0.5)*2*420:0);mood=g>0.4?'sad':'happy';}
 if(t<9.6) person(ctx,x,y,0.85,'#E8ECFF',{mood,arms:t>hopT&&t<hopT+5.5?0.6:0.1},t);
 // splash
 const sp=prog(t,8.3,9.2);if(sp>0&&sp<1){ctx.save();ctx.globalAlpha=1-sp;ctx.fillStyle='#8FD3FF';for(let i=0;i<9;i++){const a=-Math.PI*(0.1+0.8*i/8);ctx.beginPath();ctx.arc(1000+Math.cos(a)*sp*160,WY-Math.abs(Math.sin(a))*sp*190+sp*sp*120,10,0,7);ctx.fill();}ctx.restore();}
 // agua
 ctx.save();ctx.globalAlpha=0.9;const wg=ctx.createLinearGradient(0,WY,0,H);wg.addColorStop(0,'#2A94F8');wg.addColorStop(1,'#0F3FC4');ctx.fillStyle=wg;ctx.beginPath();ctx.moveTo(0,H);ctx.lineTo(0,WY);for(let xx=0;xx<=W;xx+=20)ctx.lineTo(xx,WY+Math.sin(xx/60+t*3)*9);ctx.lineTo(W,H);ctx.fill();ctx.restore();
 P.forEach((p,i)=>pill(ctx,p.l,p.x,WY+40+(i%2)*70,24,i==0?C.green:C.navy));pill(ctx,'FIN DE MES',540,WY+230,34,'#ffffff22','#fff',1);
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.9,9.3));hook(ctx,['“Este mes voy','a ahorrar”',['Yo:','o']],330,h1,{size:88});
 const m1=eo(prog(t,9.2,9.7))*(1-prog(t,11.5,11.8));hook(ctx,['El ahorro no se hace','con lo que sobra…',['se separa primero','o']],330,m1,{size:74});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
