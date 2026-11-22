const DUR=13.5;
const ITEMS=[['Tenis nuevos','$120',2.0],['Cena por delivery','$45',3.4],['Otro celular','$900',4.8],['Suscripción #7','$15',6.2]];
function draw(ctx,t){bgDark(ctx);
 person(ctx,200,1460,1.05,'#E8ECFF',{glasses:true,mood:'happy',arms:Math.sin(t*3)>0?0.7:0.4},t);
 ITEMS.forEach(([n,p,t0],i)=>{const a=eo(prog(t,t0,t0+0.4))*(1-prog(t,8.6,9));if(a<=0)return;const y=760+i*150;ctx.save();ctx.globalAlpha=a;ctx.fillStyle='#fff';rr(ctx,400,y-65,620,135,22);ctx.fill();ctx.restore();text(ctx,n,430,y-28,40,C.navy,800,'left',a);text(ctx,p,995,y-28,46,C.orange,900,'right',a,'Inter Display');stamp(ctx,'PARA ESO TRABAJO',710,y+30,26,prog(t,t0+0.5,t0+0.8)*(1-prog(t,8.6,9)),-0.03);});
 const tot=eo(prog(t,7.4,7.9))*(1-prog(t,8.6,9));pill(ctx,'Total: $1.080 = 3 semanas de trabajo',600,1380,34,C.orange,'#fff',tot);
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.6,9));hook(ctx,['Yo, después de cada','gasto innecesario:',['“Para eso trabajo”','o']],300,h1,{size:76});
 const m1=eo(prog(t,9,9.5))*(1-prog(t,11.5,11.8));hook(ctx,['¿Trabajas para pagar','cuotas… o para que',['tu dinero trabaje','o'],['para ti?','o']],330,m1,{size:74});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
