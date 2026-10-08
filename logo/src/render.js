// Rasterise an SVG with headless Chromium (Playwright).
// Usage: node render.js in.svg out.png <width> [background]
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const [inp, out, w = '1024', bg = 'transparent'] = process.argv.slice(2);
  const svg = fs.readFileSync(inp, 'utf8');
  const vb = svg.match(/viewBox="([^"]+)"/)[1].split(/[\s,]+/).map(Number);
  const W = +w, H = Math.round(W * vb[3] / vb[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.setContent(`<html><body style="margin:0;background:${bg}">` +
    svg.replace('<svg', `<svg width="${W}" height="${H}"`) + '</body></html>');
  await page.screenshot({ path: out, omitBackground: bg === 'transparent' });
  await browser.close();
})();
