// static/js/app.js
// Utility to render a plan (rooms) into a given element as SVG.
// options: target pixel size and style options for wall/floor/wallpaper
function renderPlanSVG(plan, elementId, maxWidth=300, style={}) {
  const el = document.getElementById(elementId);
  if (!el) return;
  // compute scale so plan fits maxWidth
  const pad = 8;
  const planW = plan.width;
  const planH = plan.height;
  const scale = Math.min((maxWidth - pad*2) / planW, (maxWidth*0.7 - pad*2) / planH);
  const svgW = Math.round(planW * scale) + pad*2;
  const svgH = Math.round(planH * scale) + pad*2;
  const wallColor = style.wallColor || '#e8e8e8';
  const floorColor = style.floorColor || '#d0c0a8';
  const wallpaper = style.wallpaper || '';

  // SVG building
  let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${svgW}" height="${svgH}" viewBox="0 0 ${svgW} ${svgH}">`;
  // background floor
  svg += `<rect x="0" y="0" width="${svgW}" height="${svgH}" fill="${floorColor}"/>`;
  // optionally add wallpaper patterns as simple stripes/dots
  plan.rooms.forEach((room, idx) => {
    const x = Math.round(room.x * scale) + pad;
    const y = Math.round(room.y * scale) + pad;
    const w = Math.max(2, Math.round(room.w * scale));
    const h = Math.max(2, Math.round(room.h * scale));
    // wallpaper patterns via simple fill patterns
    let fill = '#ffffff00';
    if (wallpaper === 'stripes') fill = 'url(#stripes)';
    if (wallpaper === 'dots') fill = 'url(#dots)';
    if (wallpaper === 'wood') fill = 'url(#wood)';
    // draw room background
    svg += `<g class="room" data-idx="${idx}">
      <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${wallColor}" stroke-width="2"/>
      <text x="${x+6}" y="${y+16}" font-size="12" fill="#333">${room.type || 'room'}</text>
    </g>`;
  });

  // add defs for patterns if needed
  svg += `<defs>
    <pattern id="stripes" patternUnits="userSpaceOnUse" width="10" height="10">
      <rect width="10" height="10" fill="#fff"/>
      <path d="M0 0 L10 0" stroke="#f3f3f3" stroke-width="6" />
    </pattern>
    <pattern id="dots" patternUnits="userSpaceOnUse" width="12" height="12">
      <rect width="12" height="12" fill="#fff"/>
      <circle cx="6" cy="6" r="2" fill="#eee" />
    </pattern>
    <pattern id="wood" patternUnits="userSpaceOnUse" width="30" height="30">
      <rect width="30" height="30" fill="#f6efe0"/>
      <path d="M0 10 Q15 0 30 10" stroke="#e6d9b8" stroke-width="4" fill="none" />
    </pattern>
  </defs>`;

  svg += `</svg>`;
  el.innerHTML = svg;
}