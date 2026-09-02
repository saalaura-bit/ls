(function () {
  function bloquea(e) {
    e.preventDefault();
    return false;
  }
  document.addEventListener('contextmenu', bloquea);
  document.addEventListener('copy', bloquea);
  document.addEventListener('cut', bloquea);
  document.addEventListener('selectstart', function (e) { e.preventDefault(); return false; });
  document.addEventListener('dragstart', function (e) { e.preventDefault(); return false; });
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey && (e.key === 'u' || e.key === 'c' || e.key === 'p' || e.key === 's' || e.key === 'a')) || e.key === 'F12') {
      e.preventDefault();
      return false;
    }
  });
})();
