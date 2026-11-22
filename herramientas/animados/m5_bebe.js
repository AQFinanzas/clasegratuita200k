const DUR=13.5;
const OPT=['a) Se me olvidó pagar algo','b) Mis finanzas están mejorando','c) Me están poniendo a prueba'];
function baby(ctx,x,y,t,look){ctx.save();ctx.translate(x,y);ctx.fillStyle='#F2C9A6';ctx.beginPath();ctx.ellipse(0,0,150,140,0,0,7);ctx.fill();ctx.beginPath();ctx.arc(-150,10,30,0,7);ctx.arc(150,10,30,0,7);ctx.fill();ctx.strokeStyle='#C9895E';ctx.lineWidth=6;ctx.beginPath();ctx.arc(0,-150,22,0.2,2.6);ctx.stroke();
 const bl=(t%2.4)<0.12?0.15:1;ctx.fillStyle='#1d1d2b';[-55,55].forEach(ex=>{ctx.beginPath();ctx.ellipse(ex+look*14,-10,20,26*bl,0,0,7);ctx.fill();ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(ex+look*14+6,-18,6*bl,0,7);ctx.fill();ctx.fillStyle='#1d1d2b';});
 ctx.fillStyle='#E9A07E';ctx.beginPath();ctx.arc(-95,40,20,0,7);ctx.arc(95,40,20,0,7);ctx.fill();ctx.strokeStyle='#7a3b2a';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(-16,68);ctx.lineTo(16,68);ctx.stroke();
 ctx.fillStyle='#F2C9A6';ctx.beginPath();ctx.ellipse(-40,170,34,26,0,0,7);ctx.ellipse(40,170,34,26,0,0,7);ctx.fill();ctx.restore();}
function draw(ctx,t){bgDark(ctx);
 const look=t<3?0:Math.sin(t*1.6);ctx.save();ctx.translate(540,800);ctx.scale(1.25,1.25);baby(ctx,0,0,t,look);ctx.restore();
 // celular con saldo
 const pa=eo(prog(t,0.8,1.3))*(1-prog(t,9,9.4));ctx.save();ctx.globalAlpha=pa;ctx.fillStyle='#111';rr(ctx,410,1020,260,170,24);ctx.fill();ctx.fillStyle='#fff';rr(ctx,425,1035,230,140,16);ctx.fill();ctx.restore();text(ctx,'Saldo disponible',540,1075,22,'#667',700,'center',pa);text(ctx,'$1.250',540,1130,52,C.green,900,'center',pa,'Inter Display');
 OPT.forEach((o,i)=>{const a=eo(prog(t,2.6+i*1.4,3+i*1.4))*(1-prog(t,9,9.4));pill(ctx,o,540,1250+i*92,34,'#ffffffdd',C.navy,a);});
 const d=eo(prog(t,7,7.4))*(1-prog(t,9,9.4));pill(ctx,'d) Es mi excedente: ¡a invertirlo!',540,1250+3*92+8,36,C.orange,'#fff',d);
 const h1=eo(prog(t,0,0.5))*(1-prog(t,9,9.4));hook(ctx,['Cuando veo dinero','en mi cuenta',['y no sé si…','o']],280,h1,{size:82});
 const m1=eo(prog(t,9.4,9.9))*(1-prog(t,11.5,11.8));hook(ctx,['Si te sobra dinero',['no es un error:','n'],['es tu excedente','o'],'Ponlo a trabajar'],330,m1,{size:76});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
