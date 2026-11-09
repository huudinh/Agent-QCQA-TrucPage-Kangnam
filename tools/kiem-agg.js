/* Đối chiếu tools/agg.js với số do Python tính, từng ô một.
 *
 *   node tools/kiem-agg.js [<ky>]
 *
 * Đây là thứ giữ cho hai bản không trôi khỏi nhau. Chạy lại sau MỌI thay đổi
 * ở agg.js hoặc ở v2slices.py / v2agg.py.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const BASE = path.dirname(__dirname);
const OUT = path.join(BASE, 'out');
const ky = process.argv[2] ||
  fs.readdirSync(OUT).filter(d => fs.statSync(path.join(OUT, d)).isDirectory()).sort().pop();
const SP = path.join(OUT, ky);

const doc = f => JSON.parse(fs.readFileSync(path.join(SP, f), 'utf8'));
const PY = doc('v2slices.json');

// nạp gói dòng như trang vẫn nạp
const src = fs.readFileSync(path.join(BASE, 'tools', 'data', 'rows.js'), 'utf8');
global.ROWS = JSON.parse(src.replace(/^var ROWS = /, '').replace(/;\s*$/, ''));
const AGG = require('./agg.js');
AGG.init(global.ROWS, PY.ai);

let oSo = 0, oLech = 0;
const lech = [];

function so(duong, a, b) {
  oSo++;
  const bang = (a === null || a === undefined) && (b === null || b === undefined)
    ? true
    : (typeof a === 'number' && typeof b === 'number'
        ? Math.abs(a - b) < 1e-9
        : JSON.stringify(a) === JSON.stringify(b));
  if (!bang) { oLech++; if (lech.length < 25) lech.push(`${duong}: JS=${JSON.stringify(a)} PY=${JSON.stringify(b)}`); }
}

function soKhoi(duong, a, b) {
  if (b === null || b === undefined) return;
  Object.keys(b).forEach(k => {
    if (k === 'label' || k === 'key') return;
    so(`${duong}.${k}`, a ? a[k] : undefined, b[k]);
  });
}

function soDanhSach(duong, a, b, khoaTen) {
  a = a || []; b = b || [];
  so(`${duong}.length`, a.length, b.length);
  const ma = {}; a.forEach(x => { ma[x[khoaTen]] = x; });
  b.forEach(x => soKhoi(`${duong}[${x[khoaTen]}]`, ma[x[khoaTen]], x));
}

// mọi lát mà Python đã dựng
Object.keys(PY.slices).forEach(key => {
  const py = PY.slices[key];
  const f = key === 'all' ? { dim: 'all' } : { dim: key.replace('dv:', 'dv:').replace('mkt:', 'mkt:') };
  const js = AGG.slice(f, py.label);

  soKhoi(`${key}.team`, js.team, py.team);
  soDanhSach(`${key}.nv`, js.nv, py.nv, 'nv');
  soDanhSach(`${key}.trend`, js.trend, py.trend, 'k');
  soDanhSach(`${key}.slaNv`, js.slaNv, py.slaNv, 'k');
  soDanhSach(`${key}.slaDv`, js.slaDv, py.slaDv, 'k');
  soKhoi(`${key}.slaTeam`, js.slaTeam, py.slaTeam);
  soDanhSach(`${key}.respEng`, js.respEng, py.respEng, 'k');
  soDanhSach(`${key}.respRs`, js.respRs, py.respRs, 'k');
  soDanhSach(`${key}.handoff`, js.handoff, py.handoff, 'k');
  Object.keys(py.sl).forEach(dim => soDanhSach(`${key}.sl.${dim}`, js.sl[dim], py.sl[dim], 'key'));

  // thứ tự xếp hạng phải giống hệt, không chỉ giá trị
  so(`${key}.nv.thu_tu`, (js.nv || []).map(x => x.nv).join('>'),
                          (py.nv || []).map(x => x.nv).join('>'));
});

// V2.json: khối đội dùng ngưỡng nhân viên ≥30, kiểm riêng
const V2 = doc('v2.json');
const jsAll = AGG.slice({ dim: 'all' }, 'Tất cả');
['n', 'sdt', 'q1', 'q2', 'q2n', 'q3', 'q3n', 'q4', 'q4n', 'q5', 'q5n', 'q5_2p', 'q5_dau',
 'q5_daun', 'q8', 'q8a', 'q8b', 'q8c', 'q8n', 'treo', 'tu_choi', 'tu_choi_cuu',
 'hot_chua', 'warm_chua', 'tong_ht', 'khach_cu'].forEach(k => {
  so(`v2.team.${k}`, jsAll.team[k], V2.team[k]);
});

console.log(`kỳ        : ${ky}`);
console.log(`dòng      : ${global.ROWS.n.toLocaleString('vi-VN')}`);
console.log(`lát kiểm  : ${Object.keys(PY.slices).length}`);
console.log(`ô so sánh : ${oSo.toLocaleString('vi-VN')}`);
console.log(oLech ? `\n⛔ LỆCH ${oLech} ô:` : `\n✓ KHỚP TOÀN BỘ — không ô nào lệch`);
lech.forEach(l => console.log('   ' + l));
process.exit(oLech ? 1 : 0);
