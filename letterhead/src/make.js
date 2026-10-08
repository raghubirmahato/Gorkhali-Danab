// Gorkhali Danab letterhead (A4) — node make.js <assets-dir> <out.docx>
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, VerticalAlign, ShadingType, HorizontalPositionRelativeFrom,
  VerticalPositionRelativeFrom, HorizontalPositionAlign, VerticalPositionAlign, TextWrappingType,
  LineRuleType, TableLayoutType, Tab, TabStopType,
} = require('docx');

const [assets, out] = process.argv.slice(2);
const img = (f) => fs.readFileSync(path.join(assets, f));

const CRIMSON = 'C8102E';
const BLUE = '003893';
const INK = '1E2230';
const MUTED = '5A6070';
const FONT = { ascii: 'Calibri', hAnsi: 'Calibri', cs: 'Nirmala UI', eastAsia: 'Calibri' };

// A4, 0.85" side margins
const PAGE_W = 11906, PAGE_H = 16838, SIDE = 1224;
const CONTENT_W = PAGE_W - 2 * SIDE; // 9458
const COLS = [1560, 4818, 3080];      // logo | wordmark | contact

const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
const cellNoBorders = { top: none, bottom: none, left: none, right: none };

const run = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 22, sizeComplexScript: o.size || 22, ...o });

// ---------------------------------------------------------------- header
const watermark = new Paragraph({
  children: [new ImageRun({
    type: 'png', data: img('watermark.png'),
    transformation: { width: 470, height: 510 },
    floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, align: HorizontalPositionAlign.CENTER },
      verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, align: VerticalPositionAlign.CENTER },
      behindDocument: true,
      wrap: { type: TextWrappingType.NONE },
    },
    altText: { title: 'Watermark', description: 'Gorkhali Danab badge watermark', name: 'watermark' },
  })],
  spacing: { after: 0 },
});

const contactLine = (label, value) => new Paragraph({
  alignment: AlignmentType.RIGHT,
  spacing: { after: 30 },
  children: [
    run(label + '  ', { size: 15, bold: true, color: CRIMSON }),
    run(value, { size: 16, color: INK }),
  ],
});

const headerTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: COLS,
  layout: TableLayoutType.FIXED,
  borders: noBorders,
  rows: [new TableRow({
    children: [
      new TableCell({
        width: { size: COLS[0], type: WidthType.DXA },
        borders: cellNoBorders,
        verticalAlign: VerticalAlign.CENTER,
        margins: { left: 0, right: 80, top: 0, bottom: 0 },
        children: [new Paragraph({
          spacing: { after: 0 },
          children: [new ImageRun({
            type: 'png', data: img('logo.png'),
            transformation: { width: 98, height: 106 },
            altText: { title: 'Gorkhali Danab', description: 'Gorkhali Danab badge logo', name: 'logo' },
          })],
        })],
      }),
      new TableCell({
        width: { size: COLS[1], type: WidthType.DXA },
        borders: cellNoBorders,
        verticalAlign: VerticalAlign.CENTER,
        margins: { left: 60, right: 120, top: 0, bottom: 0 },
        children: [new Paragraph({
          spacing: { after: 0 },
          children: [new ImageRun({
            type: 'png', data: img('wordmark.png'),
            transformation: { width: 300, height: 50 },
            altText: { title: 'Gorkhali Danab', description: 'GORKHALI DANAB wordmark with गोर्खाली दानव', name: 'wordmark' },
          })],
        })],
      }),
      new TableCell({
        width: { size: COLS[2], type: WidthType.DXA },
        borders: cellNoBorders,
        verticalAlign: VerticalAlign.CENTER,
        margins: { left: 120, right: 0, top: 0, bottom: 0 },
        children: [
          contactLine('ADDRESS', '[Street / Ward No.], [City], Nepal'),
          contactLine('PHONE', '+977 [phone number]'),
          contactLine('EMAIL', '[email address]'),
          contactLine('WEB', '[website]'),
        ],
      }),
    ],
  })],
});

// Flag-colour double rule: thick crimson over thin blue
const rule = (color, size, before) => new Paragraph({
  spacing: { before, after: 0, line: 40, lineRule: LineRuleType.EXACT },
  border: { bottom: { style: BorderStyle.SINGLE, size, color, space: 0 } },
  children: [],
});

const header = new Header({
  children: [watermark, headerTable, rule(CRIMSON, 24, 120), rule(BLUE, 8, 30)],
});

// ---------------------------------------------------------------- footer
const footer = new Footer({
  children: [
    new Paragraph({
      spacing: { after: 60, line: 40, lineRule: LineRuleType.EXACT },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 0 } },
      children: [],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 20 },
      children: [
        run('GORKHALI DANAB', { size: 15, bold: true, color: CRIMSON, characterSpacing: 20 }),
        run('   •   ', { size: 15, color: MUTED }),
        run('गोर्खाली दानव', { size: 15, color: BLUE }),
      ],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 0 },
      children: [
        run('Regd. No.: [            ]', { size: 15, color: MUTED }),
        run('     |     ', { size: 15, color: 'B0B4BE' }),
        run('PAN No.: [            ]', { size: 15, color: MUTED }),
        run('     |     ', { size: 15, color: 'B0B4BE' }),
        run('[website]', { size: 15, color: MUTED }),
      ],
    }),
  ],
});

// ---------------------------------------------------------------- body (ready-to-type letter)
const p = (children, o = {}) => new Paragraph({ spacing: { after: o.after ?? 0, before: o.before ?? 0, line: 276 }, alignment: o.align, children });
const label = (np, en) => [run(np + ' / ', { color: MUTED, size: 20 }), run(en + ': ', { bold: true, color: INK, size: 20 })];

const body = [
  new Paragraph({
    spacing: { after: 0, line: 276 },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
    children: [...label('पत्र संख्या', 'Ref. No.'), run('[        ]', { size: 20 }),
      new TextRun({ children: [new Tab()] }),
      ...label('मिति', 'Date'), run('[DD Month YYYY]', { size: 20 })],
  }),
  p([...label('चलानी नं.', 'Dispatch No.'), run('[        ]', { size: 20 })], { after: 360 }),

  p([run('To,')]),
  p([run('[Recipient Name]')]),
  p([run('[Designation / Organisation]')]),
  p([run('[Address]')], { after: 300 }),

  p([run('विषय / ', { color: MUTED }), run('Subject: ', { bold: true }), run('[Subject of the letter]', { bold: true, underline: {} })],
    { after: 300 }),

  p([run('Dear [Sir / Madam],')], { after: 200 }),
  p([run('[Begin typing your letter here. This page already carries the Gorkhali Danab header, footer and watermark, and every page you add will carry them too.]')],
    { after: 200 }),
  p([run('[Second paragraph.]')], { after: 480 }),

  p([run('Sincerely,')], { after: 900 }),
  new Paragraph({
    spacing: { after: 40 },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
    indent: { right: CONTENT_W - 3200 },
    children: [run('[Full Name]', { bold: true })],
  }),
  p([run('[Designation]', { color: MUTED })]),
  p([run('Gorkhali Danab', { color: CRIMSON, bold: true })]),
];

const doc = new Document({
  creator: 'Gorkhali Danab',
  title: 'Gorkhali Danab Letterhead',
  description: 'Official A4 letterhead for Gorkhali Danab',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 22 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: 2700, bottom: 1500, left: SIDE, right: SIDE, header: 500, footer: 450 },
      },
    },
    headers: { default: header },
    footers: { default: footer },
    children: body,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log('wrote', out, buf.length); });
