const DUR=13.5;
function draw(ctx,t){bgDark(ctx);
 const gy=1430;
 person(ctx,330,gy,1.25,'#E8ECFF',{mood:t>2?'nerv':'happy',sweat:t>3,arms:0.2},t);
 person(ctx,780,gy,1.1,'#9FB2FF',{mood:'happy',arms:0.4},t);
 bubble(ctx,'¿Vamos al sitio\ncaro del centro?',780,960,40,eo(prog(t,1.2,1.6))*(1-prog(t,8.8,9.2)));
 bubble(ctx,'¡Claro, de una!',330,1100,42,eo(prog(t,2.6,3))*(1-prog(t,8.8,9.2)),false,C.orange,'#fff');
 const th=eo(prog(t,4.2,4.7))*(1-prog(t,8.8,9.2));bubble(ctx,'Saldo: $12,40\nQuincena: en 9 días',330,830,38,th,true,'#ffffff');
 stamp(ctx,'TODO BIEN, TODO BIEN',540,700,44,prog(t,6,6.4)*(1-prog(t,8.8,9.2)),-0.06);
 const h1=eo(prog(t,0,0.5))*(1-prog(t,8.8,9.2));hook(ctx,['Cuando tienes',['que disimular','n'],['que no tienes problemas','o'],'económicos'],250,h1,{size:70});
 const m1=eo(prog(t,9.2,9.7))*(1-prog(t,11.5,11.8));hook(ctx,['No es el sueldo:',['es el excedente','o'],'que no estás creando'],330,m1,{size:78});
 socialBar(ctx,eo(prog(t,0.4,1)));outro(ctx,t,DUR);}
