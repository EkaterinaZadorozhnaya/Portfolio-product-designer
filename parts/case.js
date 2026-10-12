<script>
/* ПОДСВЕТКА АКТИВНОГО РАЗДЕЛА — слушатель прокрутки, а не
   IntersectionObserver. Наблюдатель стоял здесь первым, и у него
   был изъян: когда ни одна секция не попадала в полосу наблюдения,
   последнее состояние замирало — на самом верху страницы оставался
   подсвечен последний раздел. Слушатель считает положение явно
   и знает края: выше первой секции активна первая, у низа страницы —
   последняя. Расчёт убран в requestAnimationFrame, поэтому на кадр
   приходится одно вычисление, а не одно на событие. */
(function(){
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  var secs  = links.map(function(a){ return document.querySelector(a.getAttribute('href')); });
  if (!secs.length || !secs[0]) return;

  function setCurrent(i){
    links.forEach(function(a, n){
      if (n === i) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }

  function recalc(){
    var y = window.scrollY + window.innerHeight * 0.18;
    var best = 0;
    for (var i = 0; i < secs.length; i++){
      if (!secs[i]) continue;
      if (secs[i].getBoundingClientRect().top + window.scrollY <= y) best = i;
    }
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight - 4) best = secs.length - 1;
    setCurrent(best);
  }

  var ticking = false;
  function onScroll(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function(){ recalc(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  recalc();

  links.forEach(function(a){
    a.addEventListener('click', function(e){
      var t = document.querySelector(a.getAttribute('href'));
      if (!t) return;
      e.preventDefault();
      t.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
      history.replaceState(null, '', a.getAttribute('href'));
    });
  });
})();
</script>


<script>
/* Шапка включается, когда колонка ушла за верхний край. Метка в конце
   колонки, а не сама колонка: наблюдение за колонкой включало бы
   шапку в самом верху страницы, когда она ещё не нужна. */
(function(){
  var bar = document.querySelector('.topbar'), rail = document.querySelector('.rail');
  if (!bar || !rail || !('IntersectionObserver' in window)) return;
  var mark = document.createElement('span');
  mark.setAttribute('aria-hidden', 'true');
  mark.style.cssText = 'position:absolute;left:0;bottom:0;width:1px;height:1px;pointer-events:none';
  rail.appendChild(mark);
  new IntersectionObserver(function(e){
    bar.classList.toggle('is-on', e[e.length - 1].boundingClientRect.top < 0);   /* последняя запись — актуальная */
  }, { threshold: 0 }).observe(mark);
})();
</script>
