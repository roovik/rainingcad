(function(){var p=document.querySelector('.pin'),b=p&&p.querySelector('.mb'),m=document.getElementById('mpanel');if(!b||!m)return;
function set(o){m.hidden=!o;b.setAttribute('aria-expanded',o?'true':'false');if(o)document.documentElement.style.setProperty('--pinh',p.offsetHeight+'px')}
b.addEventListener('click',function(e){e.stopPropagation();set(m.hidden)});
document.addEventListener('click',function(e){if(!m.hidden&&!m.contains(e.target))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden){set(false);b.focus()}});
window.addEventListener('resize',function(){if(!m.hidden)set(false)});
})();
