(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeBtn');
  const isDark = () => root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  const label = () => { if (btn) btn.textContent = isDark() ? '☀ Light' : '☾ Dark'; };
  if (btn) btn.addEventListener('click', () => { root.dataset.theme = isDark() ? 'light' : 'dark'; label(); });
  try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', label); } catch (e) {}
  label();
})();
// Convert a pointer event into the SVG's own coordinate system.
function svgPoint(svg, e) {
  const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
  return p.matrixTransform(svg.getScreenCTM().inverse());
}
// Make an SVG element draggable; onMove receives {x, y} in SVG units.
function draggable(svg, el, onMove) {
  let on = false;
  el.addEventListener('pointerdown', e => { on = true; el.setPointerCapture(e.pointerId); onMove(svgPoint(svg, e)); e.preventDefault(); });
  el.addEventListener('pointermove', e => { if (on) onMove(svgPoint(svg, e)); });
  el.addEventListener('pointerup', () => { on = false; });
  el.addEventListener('pointercancel', () => { on = false; });
}
const $ = id => document.getElementById(id);
function setChip(el, state, text) { el.dataset.state = state; el.textContent = text; }
function sig(x, n) { return Number(x.toPrecision(n)); }
