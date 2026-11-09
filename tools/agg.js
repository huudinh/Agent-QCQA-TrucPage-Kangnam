/* Tính lại mọi chỉ số từ bảng hội thoại, theo đúng bộ lọc đang chọn.
 *
 * ⛔ Công thức ở đây là bản JS của tools/v2slices.py. Sửa một bên là phải sửa
 *    bên kia, rồi chạy `node tools/kiem-agg.js <ky>` để đối chiếu từng ô với
 *    số Python. Không chấm lại hội thoại — chỉ cộng lại từ dòng đã chấm.
 */
var AGG = (function () {
  'use strict';

  var DVL = [['MAT', 'Mắt'], ['MUI', 'Mũi'], ['NGUC', 'Ngực'], ['HAM_MAT', 'Hàm mặt'],
             ['BODY', 'Body / Hút mỡ'], ['DA_TRE_HOA', 'Da / Trẻ hoá'], ['KHAC', 'Khác'],
             ['KHONG_XAC_DINH', 'Chưa xếp được']];
  var MKL = [['HA_NOI', 'Hà Nội'], ['HO_CHI_MINH', 'Hồ Chí Minh'], ['TINH_KHAC', 'Các tỉnh khác'],
             ['VIET_KIEU', 'Việt kiều'], ['QUOC_TE', 'Quốc tế'], ['CHUA_RO', 'Chưa xác định']];
  var KGL = ['00-06', '06-09', '09-12', '12-14', '14-18', '18-22', '22-24'];
  var NGL = [['QC', 'Từ quảng cáo'], ['TRUC_TIEP', 'Nhắn thẳng page'], ['COMMENT', 'Từ bình luận']];
  var SHORT = {};
  DVL.forEach(function (o) { SHORT[o[0]] = o[1]; });
  SHORT.KHONG_XAC_DINH = 'Chưa rõ'; SHORT.BODY = 'Béo/Hút mỡ'; SHORT.DA_TRE_HOA = 'Da';
  var MKLAB = {};
  MKL.forEach(function (o) { MKLAB[o[0]] = o[1]; });
  var BINS = [[0, 60, '< 1 phút'], [60, 300, '1–5 phút'], [300, 900, '5–15 phút'],
              [900, 1800, '15–30 phút'], [1800, 1e9, '> 30 phút']];
  var W = [['q1', 0.30], ['q3', 0.15], ['q5', 0.20], ['q8', 0.15], ['q6', 0.10], ['q7', 0.10]];

  var C, TU, N, AI, DAYS;
  var iNgay, iNv, iDv, iKg, iNguon, iTt, iPage, iNhiet;

  /* Bản JS của round() trong Python. Hai điều phải đúng cùng lúc:
     · mốc hoà THẬT thì làm tròn về số chẵn — 81,25 → 81,2, không phải 81,3;
     · nhưng phải xét trên giá trị THẬT của double. 8109/53/60 trông là 2,55
       mà double gần nhất là 2,5499…, nên Python cho 2,5. Nhân với 10 trước
       sẽ "sửa" sai số đó thành đúng 25,5 rồi tạo ra một mốc hoà không có thật. */
  function rnd(x, nd) {
    var s = x.toFixed(20), i = s.indexOf('.');
    var du = s.slice(i + 1 + nd).replace(/0+$/, '');
    if (du === '5') {
      var nguyen = Number(s.slice(0, i) + s.slice(i + 1, i + 1 + nd));
      return ((nguyen % 2 === 0) ? nguyen : nguyen + 1) / Math.pow(10, nd);
    }
    return Number(x.toFixed(nd));
  }
  function p(a, b, nd) { return b ? rnd(a / b * 100, nd === undefined ? 1 : nd) : null; }

  function init(rows, ai) {
    C = rows.cot; TU = rows.tu; N = rows.n; AI = ai || {};
    iNgay = C.ngay; iNv = C.nv; iDv = C.dv; iKg = C.kg;
    iNguon = C.nguon; iTt = C.tt; iPage = C.page; iNhiet = C.nhiet;
    // ngày xếp theo thời gian, không theo thứ tự chữ cái của từ điển
    DAYS = TU.ngay.slice().sort(function (a, b) {
      var x = a.split('/'), y = b.split('/');
      return (x[1] - y[1]) || (x[0] - y[0]);
    });
    return DAYS;
  }

  /* ---------- khối chỉ số cho một tập dòng ---------- */
  function kpis(ix, nAll) {
    var n = ix.length, i, r;
    var d6 = 0, d24 = 0, d48 = 0, q2h = 0, q3h = 0, q4h = 0;
    var sla = 0, sla5 = 0, sla2 = 0, sla1 = 0, sla1ok = 0;
    var chua = 0, q8ah = 0, q8bh = 0, notreo = 0, treo = 0;
    var luot = 0, luotok = 0, luotok2 = 0, tongwait = 0;
    var sdt = 0, motcham = 0, nvmotcham = 0, tc = 0, tccuu = 0, hot = 0, warm = 0;

    for (i = 0; i < n; i++) {
      r = ix[i];
      var cosdt = C.co_sdt[r], g = C.gio_sdt[r];
      if (cosdt) sdt++;
      if (C.du6[r]) { d6++; if (g !== null && g <= 6) q2h++; }
      if (C.du24[r]) { d24++; if (g !== null && g <= 24) q3h++; }
      if (C.du48[r]) { d48++; if (g !== null && g <= 48) q4h++; }
      var nw = C.n_wait[r];
      if (nw > 0) { sla++; var ww = C.worst_wait[r]; if (ww <= 300) sla5++; if (ww <= 120) sla2++; }
      var fw = C.first_wait[r];
      if (fw !== null) { sla1++; if (fw <= 300) sla1ok++; }
      if (!cosdt) {
        chua++;
        if (C.cham_lai[r] >= 1) q8ah++;
        if (C.n_xin[r] >= 2) q8bh++;
        var nh = TU.nhiet[iNhiet[r]];
        if (nh === 'HOT') hot++; else if (nh === 'WARM') warm++;
      }
      if (C.treo[r]) treo++; else notreo++;
      luot += nw; luotok += C.n_wait_ok5[r]; luotok2 += C.n_wait_ok2[r]; tongwait += C.sum_wait[r];
      if (C.kh_mot_cham[r]) motcham++;
      if (C.mot_cham[r]) nvmotcham++;
      if (C.tu_choi[r]) { tc++; if (cosdt) tccuu++; }
    }

    var q8a = p(q8ah, chua), q8b = p(q8bh, chua), q8c = p(notreo, n);
    var pr = [q8a, q8b, q8c].filter(function (x) { return x !== null; });
    var q8 = pr.length ? rnd(pr.reduce(function (a, b) { return a + b; }, 0) / pr.length, 1) : null;

    return {
      n: n, tong_ht: nAll === undefined ? n : nAll, khach_cu: (nAll === undefined ? n : nAll) - n,
      sdt: sdt,
      q1: p(sdt, n),
      q2: p(q2h, d6), q2n: d6,
      q3: p(q3h, d24), q3n: d24,
      q4: p(q4h, d48), q4n: d48,
      q5: p(sla5, sla), q5n: sla,
      q5_2p: p(sla2, sla),
      q5_dau: p(sla1ok, sla1), q5_daun: sla1,
      luot: luot, luot_pc: p(luotok, luot), luot_pc2: p(luotok2, luot),
      phut_tb: luot ? rnd(tongwait / luot / 60, 1) : null,
      q8: q8, q8a: q8a, q8b: q8b, q8c: q8c, q8n: chua,
      mot_cham: p(motcham, n), mot_chamn: motcham,
      nv_mot_cham: p(nvmotcham, n),
      treo: treo,
      tu_choi: tc, tu_choi_cuu: p(tccuu, tc),
      hot_chua: hot, warm_chua: warm
    };
  }

  function slaCell(ix) {
    var s = 0, ok = 0;
    for (var i = 0; i < ix.length; i++) {
      var r = ix[i];
      if (C.n_wait[r] > 0) { s++; if (C.worst_wait[r] <= 300) ok++; }
    }
    return { v: p(ok, s), n: s };
  }

  /* Giữ THỨ TỰ GẶP ĐẦU TIÊN: Counter của Python giữ thứ tự chèn, và
     most_common() sắp xếp ổn định nên khi đồng hạng thì ai gặp trước đứng trước.
     Duyệt `for (k in obj)` trả khoá số theo thứ tự tăng dần — sai thứ tự đó. */
  function gom(ix, col) {
    var m = {}, kh = [];
    for (var i = 0; i < ix.length; i++) {
      var k = col[ix[i]];
      if (!m[k]) { m[k] = []; kh.push(k); }
      m[k].push(ix[i]);
    }
    m.__kh = kh;
    return m;
  }

  function theoSoLuong(m) {          // thứ tự của Counter.most_common()
    return m.__kh.slice().sort(function (a, b) { return m[b].length - m[a].length; });
  }

  function top3(ix, col, nhan) {
    var m = gom(ix, col);
    var out = theoSoLuong(m).map(function (k) { return [nhan(k), m[k].length]; });
    return out.slice(0, 3).map(function (o) {
      return [o[0], rnd(o[1] / ix.length * 100, 0)];
    });
  }

  /* ---------- dựng trọn bộ cho một lát ---------- */
  function build(ix, nAll, label, days) {
    var T = kpis(ix, nAll);
    var byNv = gom(ix, iNv), nvs = [], nv, sub;
    var nvKeys = theoSoLuong(byNv);

    for (var ni = 0; ni < nvKeys.length; ni++) {
      nv = nvKeys[ni]; sub = byNv[nv];
      var ten = TU.nv[nv];
      if (!ten || sub.length < 20) continue;
      var b = kpis(sub, sub.length);
      [['q2', 'q2n'], ['q3', 'q3n'], ['q4', 'q4n'], ['q5', 'q5n'], ['q8', 'q8n']]
        .forEach(function (kk) { if ((b[kk[1]] || 0) < 20) b[kk[0]] = null; });
      b.nv = ten;
      var a = AI[ten];
      b.q6 = a ? a[0] : null; b.q7 = a ? a[1] : null; b.doc = a ? a[2] : 0;
      b.mix = top3(sub, iDv, function (k) { var c = TU.dv[k]; return SHORT[c] || c; });
      b.mkt = top3(sub, iTt, function (k) { return MKLAB[TU.tt[k]] || TU.tt[k]; });
      nvs.push(b);
    }

    var ai6 = [], ai7 = [];
    nvs.forEach(function (x) {
      if (x.q6 !== null && x.q6 !== undefined) ai6.push(x.q6);
      if (x.q7 !== null && x.q7 !== undefined) ai7.push(x.q7);
    });
    var sum = function (a) { return a.reduce(function (x, y) { return x + y; }, 0); };
    var avg = { q6: ai6.length ? sum(ai6) / ai6.length : null,
                q7: ai7.length ? sum(ai7) / ai7.length : null };

    nvs.forEach(function (b) {
      var tot = 0, wsum = 0;
      W.forEach(function (kw) {
        var k = kw[0], w = kw[1];
        var v = b[k], tv = (k in avg) ? avg[k] : T[k];
        if (v === null || v === undefined || !tv) return;
        tot += w * Math.min(v / tv * 100, 160); wsum += w;
      });
      b.diem = wsum ? rnd(tot / wsum, 1) : null;
      b.hang = b.diem !== null && b.diem >= 110 ? 'A' : (b.diem !== null && b.diem >= 92 ? 'B' : 'C');
    });
    nvs.sort(function (a, b) { return (b.diem || 0) - (a.diem || 0); });

    var byDay = gom(ix, iNgay);
    var trend = [];
    days.forEach(function (d) {
      var di = TU.ngay.indexOf(d), s = byDay[di];
      if (!s || !s.length) return;
      var t = kpis(s, s.length);
      t.k = d; t.cham_lai = t.q8a;
      trend.push(t);
    });

    function theoNgay(s) {
      var row = { all: slaCell(s) }, g = gom(s, iNgay);
      days.forEach(function (d) {
        var di = TU.ngay.indexOf(d);
        row[d] = slaCell(g[di] || []);
      });
      return row;
    }

    var slaNv = [];
    for (var si = 0; si < nvKeys.length; si++) {
      nv = nvKeys[si]; sub = byNv[nv];
      if (!TU.nv[nv] || sub.length < 20) continue;
      var rn = theoNgay(sub); rn.k = TU.nv[nv]; slaNv.push(rn);
    }
    slaNv.sort(function (a, b) { return (b.all.v || 0) - (a.all.v || 0); });

    var byDv = gom(ix, iDv), slaDv = [];
    DVL.forEach(function (o) {
      var di = TU.dv.indexOf(o[0]), s = byDv[di];
      if (!s || s.length < 20) return;
      var rd = theoNgay(s); rd.k = o[1]; slaDv.push(rd);
    });
    slaDv.sort(function (a, b) { return (b.all.v || 0) - (a.all.v || 0); });

    var slaTeam = theoNgay(ix); slaTeam.k = 'Toàn đội';

    var eng = [], rsp = [];
    BINS.forEach(function (bn) {
      var s = ix.filter(function (r) {
        var f = C.first_wait[r];
        return f !== null && f >= bn[0] && f < bn[1];
      });
      var k2 = 0;
      s.forEach(function (r) { if (C.n_kh[r] >= 2) k2++; });
      eng.push({ k: bn[2], v: p(k2, s.length), n: s.length });
      var s48 = s.filter(function (r) { return C.du48[r]; });
      var h = 0;
      s48.forEach(function (r) { var g = C.gio_sdt[r]; if (g !== null && g <= 48) h++; });
      rsp.push({ k: bn[2], v: p(h, s48.length), n: s48.length });
    });

    var hand = [];
    [[1, '1 người'], [2, '2 người'], [3, '3 người'], [4, '4 người trở lên']].forEach(function (o) {
      var s = ix.filter(function (r) {
        var v = C.so_nv[r] || 0;
        return o[0] < 4 ? v === o[0] : v >= 4;
      });
      var s48 = s.filter(function (r) { return C.du48[r]; });
      var h = 0;
      s48.forEach(function (r) { var g = C.gio_sdt[r]; if (g !== null && g <= 48) h++; });
      hand.push({ k: o[1], v: p(h, s48.length), n: s48.length, ht: s.length });
    });

    var sl = {};
    [['dv', DVL, iDv, TU.dv],
     ['mkt', MKL, iTt, TU.tt],
     ['kg', KGL.map(function (k) { return [k, k.replace('-', '–') + 'h']; }), iKg, TU.kg],
     ['nguon', NGL, iNguon, TU.nguon],
     ['ngay', days.map(function (d) { return [d, d]; }), iNgay, TU.ngay]
    ].forEach(function (dim) {
      var g = gom(ix, dim[2]), out = [];
      dim[1].forEach(function (o) {
        var di = dim[3].indexOf(o[0]), s = g[di];
        if (!s || !s.length) return;
        var b = kpis(s, s.length); b.key = o[0]; b.label = o[1];
        out.push(b);
      });
      sl[dim[0]] = out;
    });

    return { label: label, team: T, nv: nvs, trend: trend, slaNv: slaNv, slaDv: slaDv,
             slaTeam: slaTeam, respEng: eng, respRs: rsp, handoff: hand, sl: sl };
  }

  /* Bản xuất Caresoft mỗi lần một phạm vi page khác nhau. Nếu số page đổi giữa
     các ngày thì đường diễn biến nhảy vì ĐỔI PHẠM VI, không phải vì đội đổi —
     trang phải nói ra điều đó chứ không vẽ như thể cùng một thước. */
  function phamVi(f) {
    f = f || {};
    var d1 = f.d1 === undefined ? 0 : f.d1;
    var d2 = f.d2 === undefined ? DAYS.length - 1 : f.d2;
    var ds = DAYS.slice(d1, d2 + 1);
    var ix = ds.map(function (d) { return TU.ngay.indexOf(d); });
    var theo = {};
    ix.forEach(function (i) { theo[i] = {}; });
    for (var r = 0; r < N; r++) {
      if (theo[iNgay[r]] !== undefined) theo[iNgay[r]][iPage[r]] = 1;
    }
    var so = ix.map(function (i) { return Object.keys(theo[i]).length; });
    var phu = {};                       // page → số ngày có mặt
    ix.forEach(function (i) {
      for (var p in theo[i]) phu[p] = (phu[p] || 0) + 1;
    });
    var chung = Object.keys(phu).filter(function (p) { return phu[p] === ds.length; }).map(Number);
    var mn = Math.min.apply(null, so), mx = Math.max.apply(null, so);
    /* Trong MỘT bản xuất liền mạch, số page vẫn chênh nhau vài đơn vị vì có page
       hôm đó không ai nhắn — đó là bình thường. Chỉ gọi là ĐỔI PHẠM VI khi chênh
       từ gấp đôi trở lên, dấu hiệu của việc gộp hai bản xuất khác tầm. Cảnh báo
       bật lên cả lúc bình thường thì người đọc sẽ quen tay bỏ qua. */
    return {
      days: ds, so: so, phu: phu, chung: chung,
      doi: so.some(function (x) { return x !== so[0]; }),
      lech: mx >= mn * 2,
      min: mn, max: mx
    };
  }

  /* ---------- lọc rồi dựng ---------- */
  function loc(f) {
    f = f || {};
    var d1 = f.d1 === undefined ? 0 : f.d1;
    var d2 = f.d2 === undefined ? DAYS.length - 1 : f.d2;
    var ngayOk = {};
    for (var i = d1; i <= d2; i++) ngayOk[TU.ngay.indexOf(DAYS[i])] = 1;

    var dim = f.dim || 'all', dimCol = null, dimIdx = -1;
    if (dim.indexOf('dv:') === 0) { dimCol = iDv; dimIdx = TU.dv.indexOf(dim.slice(3)); }
    else if (dim.indexOf('mkt:') === 0) { dimCol = iTt; dimIdx = TU.tt.indexOf(dim.slice(4)); }

    var pg = (f.page === undefined || f.page === null || f.page < 0) ? -1 : f.page;
    var kg = (f.kg === undefined || f.kg === null || f.kg < 0) ? -1 : f.kg;
    var ng = (f.nguon === undefined || f.nguon === null || f.nguon < 0) ? -1 : f.nguon;

    var all = [], moi = [];
    for (var r = 0; r < N; r++) {
      if (!ngayOk[iNgay[r]]) continue;
      if (pg >= 0 && iPage[r] !== pg) continue;
      if (kg >= 0 && iKg[r] !== kg) continue;
      if (ng >= 0 && iNguon[r] !== ng) continue;
      if (dimCol && dimCol[r] !== dimIdx) continue;
      all.push(r);
      if (!C.cu[r]) moi.push(r);
    }
    return { all: all, moi: moi };
  }

  function slice(f, label) {
    var s = loc(f);
    var d1 = (f && f.d1) || 0;
    var d2 = (f && f.d2 !== undefined) ? f.d2 : DAYS.length - 1;
    return build(s.moi, s.all.length, label || 'Tất cả', DAYS.slice(d1, d2 + 1));
  }

  return { init: init, slice: slice, loc: loc, build: build, kpis: kpis, phamVi: phamVi,
           days: function () { return DAYS; },
           tu: function () { return TU; } };
})();

if (typeof module !== 'undefined' && module.exports) module.exports = AGG;
