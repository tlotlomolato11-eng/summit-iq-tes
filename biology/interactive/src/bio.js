// "Check yourself" cards: the button reveals the answer below it.
document.querySelectorAll('.reveal').forEach(b => b.addEventListener('click', () => {
  const a = b.nextElementSibling; a.hidden = !a.hidden; b.textContent = a.hidden ? 'Show answer' : 'Hide answer';
}));
// Segmented buttons: data-group on the container; calls onSeg(group, value).
function seg(el, onChange) {
  el.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    el.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b));
    onChange(b.dataset.v);
  });
}
const svgEl = (tag, attrs) => { const e = document.createElementNS('http://www.w3.org/2000/svg', tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
