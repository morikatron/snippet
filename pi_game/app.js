"use strict";

/* π — 円周率100万桁を「足して10」で消していくゲーム
 *
 * ルールと自動テストは、『タシテン ＋たして10にする物語＋』(ニンテンドーDS, 2007) の
 * 原型となった 2006年3月の Mac 用試作の仕様を再実装したもの:
 *   - 窓には残っている数字のうち先頭の10桁が見える
 *   - 窓の中の連続した並びで、合計が10の倍数なら消せる（合計0も含む）
 *   - 消えたぶんは後ろから詰まる
 *   - 自動テストは解を「開始位置の昇順→終了位置の昇順」で数え、いつも0番から試す。
 *     行き止まりなら一手戻し、直前に選んだ解番号の次を試す（深さ優先の総当たり）
 */

const W = 10; // 窓に見える桁数
const TOTAL_DIGITS = 1000000; // 持っている桁数（整数部の3を含む）
const GOAL = 999998; // 合計が10の倍数になる最大の接頭辞（100万桁全部だと合計が10の倍数にならず消しきれない）

const SPEEDS = [2, 6, 30, 120, 1200, 12000, Infinity];
const SPEED_LABELS = [
	"2 手/秒",
	"6 手/秒",
	"30 手/秒",
	"120 手/秒",
	"1,200 手/秒",
	"12,000 手/秒",
	"最速",
];
const MAX_STEPS_PER_FRAME = 40000;
const SLOW_LIMIT = 6; // これ以下の速さでは「選択を見せてから消す」二拍子にする
const SAVE_KEY = "pi-game-v1";
const THEME_KEY = "pi-game-theme";

/* ---- 状態 ---- */
let digits = null; // Uint8Array(TOTAL_DIGITS)
let win = new Int32Array(W); // 窓: 元の桁番号（0始まり）。GOAL 以上は空き
let cleared = 0; // 消した桁数
let nextKai = 0; // 次に試す解番号（自動テスト用）
let nUndo = 0; // アンドゥ回数
let moves = 0; // 実行した手数（アンドゥで捨てた手も含む）

/* 履歴: 1手 = 12 int32 (cleared, choosing, win[10]) */
let hist = new Int32Array(12 * 4096);
let histLen = 0;

const auto = {
	running: false,
	raf: 0,
	lastT: 0,
	budget: 0,
	pending: null,
	startedAt: 0,
	rate: 0,
};
let sel = null; // 手動選択 {a, b}（窓の位置）
let selecting = false;

/* ---- DOM ---- */
const $ = (id) => document.getElementById(id);
const elBoard = $("board");
const elStatus = $("statusline");
const elBadge = $("sumbadge");
const elFill = $("progressfill");
const elPCap = $("progresscaption");
const elBtnAuto = $("btn-auto");
const elBtnStop = $("btn-stop");
const elBtnUndo = $("btn-undo");
const elBtnReset = $("btn-reset");
const elSpeed = $("speed");
const elSpeedLabel = $("speedlabel");
const elOverlay = $("overlay");
const elOverlayCard = $("overlaycard");
const elBtnTheme = $("btn-theme");

const fmt = (n) => n.toLocaleString("ja-JP");

/* ---- 盤面の基本操作 ---- */

function nVisible() {
	for (let i = 0; i < W; i++) if (win[i] >= GOAL) return i;
	return W;
}

/* 解番号 k の並び [i, j] を返す。無ければ null（列挙順は開始位置昇順→終了位置昇順） */
function findSolution(k) {
	const n = nVisible();
	let counter = 0;
	for (let i = 0; i < n; i++) {
		let s = 0;
		for (let j = i; j < n; j++) {
			s += digits[win[j]];
			if (s % 10 === 0) {
				if (counter === k) return [i, j];
				counter++;
			}
		}
	}
	return null;
}

function countSolutions() {
	const n = nVisible();
	let counter = 0;
	for (let i = 0; i < n; i++) {
		let s = 0;
		for (let j = i; j < n; j++) {
			s += digits[win[j]];
			if (s % 10 === 0) counter++;
		}
	}
	return counter;
}

/* 選択 [i, j] が解なら、その解番号を返す。解でなければ -1 */
function solutionIndexOf(a, b) {
	const n = nVisible();
	let counter = 0;
	for (let i = 0; i < n; i++) {
		let s = 0;
		for (let j = i; j < n; j++) {
			s += digits[win[j]];
			if (s % 10 === 0) {
				if (i === a && j === b) return counter;
				counter++;
			}
		}
	}
	return -1;
}

function pushHist(choosing) {
	if (histLen * 12 >= hist.length) {
		const bigger = new Int32Array(hist.length * 2);
		bigger.set(hist);
		hist = bigger;
	}
	const base = histLen * 12;
	hist[base] = cleared;
	hist[base + 1] = choosing;
	hist.set(win, base + 2);
	histLen++;
}

function popHist() {
	histLen--;
	const base = histLen * 12;
	cleared = hist[base];
	nextKai = hist[base + 1] + 1; // 直前に選んだ解の「次」から探し直す
	win.set(hist.subarray(base + 2, base + 12));
	nUndo++;
}

/* [i, j] を消して左に詰め、後ろから補充する */
function applyMove(i, j) {
	const nDel = j - i + 1;
	let base = win[W - 1] + 1;
	let dst = i;
	for (let src = j + 1; src < W; src++) win[dst++] = win[src];
	while (dst < W) win[dst++] = base++;
	cleared += nDel;
	nextKai = 0;
}

/* 自動テストの1歩。"moved" | "undone" | "done" | "stuck" を返す */
function autoStep() {
	const sol = findSolution(nextKai);
	if (sol) {
		pushHist(nextKai);
		applyMove(sol[0], sol[1]);
		moves++;
		return cleared >= GOAL ? "done" : "moved";
	}
	if (histLen === 0) {
		nextKai = 0;
		return "stuck";
	}
	popHist();
	return "undone";
}

function resetState() {
	for (let i = 0; i < W; i++) win[i] = i;
	cleared = 0;
	nextKai = 0;
	nUndo = 0;
	moves = 0;
	histLen = 0;
	sel = null;
	auto.pending = null;
}

/* ---- 保存（この端末のブラウザ内のみ。履歴は保存しないのでアンドゥは復元されない） ---- */

function saveState() {
	try {
		localStorage.setItem(
			SAVE_KEY,
			JSON.stringify({
				cleared,
				nUndo,
				moves,
				nextKai,
				win: Array.from(win),
			}),
		);
	} catch (e) {
		/* プライベートモード等では保存できなくてよい */
	}
}

function loadState() {
	try {
		const raw = localStorage.getItem(SAVE_KEY);
		if (!raw) return;
		const s = JSON.parse(raw);
		if (!s || !Array.isArray(s.win) || s.win.length !== W) return;
		if (s.goal !== undefined && s.goal !== GOAL) return; // 旧版の保存は捨てる
		cleared = s.cleared | 0;
		nUndo = s.nUndo | 0;
		moves = s.moves | 0;
		nextKai = s.nextKai | 0;
		for (let i = 0; i < W; i++) win[i] = s.win[i] | 0;
	} catch (e) {
		/* 壊れた保存は無視して最初から */
	}
}

/* ---- 描画 ---- */

function renderBoard(enterFrom) {
	const n = nVisible();
	elBoard.replaceChildren();
	for (let i = 0; i < W; i++) {
		const slot = document.createElement("div");
		slot.className = "slot";
		slot.dataset.ix = i;
		if (i >= n) slot.classList.add("empty");
		if (sel && i >= sel.a && i <= sel.b) slot.classList.add("sel");
		if (enterFrom !== undefined && i >= enterFrom) slot.classList.add("enter");
		const tile = document.createElement("div");
		tile.className = "tile";
		tile.textContent = i < n ? String(digits[win[i]]) : "・";
		const pos = document.createElement("div");
		pos.className = "pos";
		pos.textContent = i < n ? fmt(win[i] + 1) : "";
		slot.append(tile, pos);
		elBoard.append(slot);
	}
	if (enterFrom !== undefined) {
		requestAnimationFrame(() => {
			for (const s of elBoard.querySelectorAll(".slot.enter"))
				s.classList.remove("enter");
		});
	}
}

function renderBadge() {
	if (!sel) {
		elBadge.hidden = true;
		return;
	}
	let s = 0;
	for (let i = sel.a; i <= sel.b; i++) s += digits[win[i]];
	elBadge.hidden = false;
	elBadge.textContent = `合計 ${s}`;
	elBadge.classList.toggle("ok", s % 10 === 0);
}

function renderInfo() {
	const remain = GOAL - cleared;
	const parts = [
		`消した ${fmt(cleared)} 桁`,
		`残り ${fmt(remain)} 桁`,
		`アンドゥ ${fmt(nUndo)} 回`,
		`見えている解 ${countSolutions()} 個`,
	];
	if (auto.running && auto.rate > 0)
		parts.push(`${fmt(Math.round(auto.rate))} 手/秒`);
	elStatus.textContent = parts.join(" ／ ");
	elFill.style.width = `${(cleared / GOAL) * 100}%`;
	const n = nVisible();
	elPCap.textContent =
		n > 0
			? `いま 第${fmt(win[0] + 1)}〜${fmt(win[n - 1] + 1)}桁 を見ています（全 ${fmt(GOAL)} 桁）`
			: "全部消えました";
}

function renderButtons() {
	elBtnAuto.disabled = auto.running || !digits;
	elBtnStop.disabled = !auto.running;
	elBtnUndo.disabled = auto.running || histLen === 0 || !digits;
	elBtnReset.disabled = auto.running || !digits;
}

function renderAll(enterFrom) {
	renderBoard(enterFrom);
	renderBadge();
	renderInfo();
	renderButtons();
}

/* ---- 手動プレイ ---- */

function slotFromEvent(e) {
	const el = document.elementFromPoint(e.clientX, e.clientY);
	const slot = el && el.closest ? el.closest(".slot") : null;
	if (!slot || slot.classList.contains("empty")) return -1;
	return Number(slot.dataset.ix);
}

function onPointerDown(e) {
	if (auto.running || !digits) return;
	const ix = slotFromEvent(e);
	if (ix < 0) return;
	selecting = true;
	sel = { a: ix, b: ix, anchor: ix };
	try {
		elBoard.setPointerCapture(e.pointerId);
	} catch (err) {
		/* 取れなくても選択は成立する */
	}
	renderBoard();
	renderBadge();
}

function onPointerMove(e) {
	if (!selecting) return;
	const ix = slotFromEvent(e);
	if (ix < 0) return;
	const a = Math.min(sel.anchor, ix);
	const b = Math.max(sel.anchor, ix);
	if (a !== sel.a || b !== sel.b) {
		sel = { a, b, anchor: sel.anchor };
		renderBoard();
		renderBadge();
	}
}

function onPointerUp() {
	if (!selecting) return;
	selecting = false;
	const { a, b } = sel;
	let s = 0;
	for (let i = a; i <= b; i++) s += digits[win[i]];
	if (s % 10 !== 0) {
		// 消せない並び: バッジを少し残してから選択解除
		setTimeout(() => {
			sel = null;
			renderAll();
		}, 350);
		return;
	}
	const choosing = solutionIndexOf(a, b);
	sel = null;
	// 縮小消去 → 詰めて補充（試作と同じ二拍子）
	const slots = elBoard.querySelectorAll(".slot");
	for (let i = a; i <= b; i++) slots[i].classList.add("erasing");
	const finish = () => {
		pushHist(choosing);
		applyMove(a, b);
		moves++;
		saveState();
		if (cleared >= GOAL) {
			renderAll();
			showClearOverlay("manual");
		} else {
			renderAll(a);
		}
	};
	if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) finish();
	else setTimeout(finish, 170);
}

function onUndo() {
	if (auto.running || histLen === 0) return;
	popHist();
	saveState();
	renderAll();
}

/* ---- 自動テスト ---- */

function startAuto(fromScratch) {
	if (fromScratch) resetState();
	sel = null;
	auto.running = true;
	auto.lastT = performance.now();
	auto.budget = 0;
	auto.pending = null;
	auto.startedAt = performance.now();
	auto.rate = 0;
	renderAll();
	auto.raf = requestAnimationFrame(autoFrame);
}

function stopAuto() {
	auto.running = false;
	cancelAnimationFrame(auto.raf);
	sel = null;
	auto.pending = null;
	saveState();
	renderAll();
}

function autoFrame(t) {
	if (!auto.running) return;
	const dt = Math.min(0.25, (t - auto.lastT) / 1000);
	auto.lastT = t;
	const sp = SPEEDS[Number(elSpeed.value)];
	let steps;
	if (sp === Infinity) {
		steps = MAX_STEPS_PER_FRAME;
	} else {
		auto.budget += sp * dt;
		steps = Math.min(Math.floor(auto.budget), MAX_STEPS_PER_FRAME);
		auto.budget -= steps;
	}
	const slow = sp <= SLOW_LIMIT;
	let result = "";
	let did = 0;
	for (let k = 0; k < steps; k++) {
		if (slow) {
			// 二拍子: まず選択を見せて、次の拍で消す
			if (!auto.pending) {
				const sol = findSolution(nextKai);
				if (sol) {
					auto.pending = sol;
					sel = { a: sol[0], b: sol[1] };
					did++;
					continue;
				}
				// 解が無い: その場でアンドゥ
				result = autoStep();
				sel = null;
				did++;
				if (result === "stuck") break;
				continue;
			}
			result = autoStep(); // pending と同じ解が選ばれる（決定的なので一致する）
			auto.pending = null;
			sel = null;
			did++;
			if (result === "done" || result === "stuck") break;
		} else {
			result = autoStep();
			did++;
			if (result === "done" || result === "stuck") break;
		}
	}
	if (did > 0) {
		const elapsed = (performance.now() - auto.startedAt) / 1000;
		if (elapsed > 0.5) auto.rate = moves / elapsed;
	}
	renderAll();
	if (result === "done") {
		auto.running = false;
		saveState();
		renderAll();
		showClearOverlay("auto");
		return;
	}
	if (result === "stuck") {
		stopAuto();
		elStatus.textContent = "行き止まり: 最初の局面まで戻ってしまいました";
		return;
	}
	auto.raf = requestAnimationFrame(autoFrame);
}

/* ---- ダイアログ ---- */

function showOverlay(html) {
	elOverlayCard.innerHTML = html;
	elOverlay.hidden = false;
}

function hideOverlay() {
	elOverlay.hidden = true;
}

function showAutoDialog() {
	if (cleared === 0 && histLen === 0) {
		startAuto(true);
		return;
	}
	showOverlay(`
    <h2>自動テスト</h2>
    <p>いまの状態から続けますか？</p>
    <div class="ovl-buttons">
      <button class="btn btn-primary" data-act="resume">続きから</button>
      <button class="btn" data-act="fresh">最初から</button>
      <button class="btn" data-act="cancel">やめる</button>
    </div>`);
}

function showClearOverlay(how) {
	const sec = auto.startedAt ? (performance.now() - auto.startedAt) / 1000 : 0;
	const lines = [
		`<h2>全部クリアしました！</h2>`,
		`<p>${fmt(GOAL)}桁、ぜんぶ消えました。<br>` +
			`手数 ${fmt(moves)} ／ アンドゥ ${fmt(nUndo)} 回` +
			(how === "auto" && sec > 0 ? ` ／ ${sec.toFixed(1)} 秒` : "") +
			`</p>`,
	];
	if (nUndo === 0 && how === "auto") {
		lines.push(`<p>一度も行き止まりませんでした。</p>`);
	}
	lines.push(`
    <div class="ovl-buttons">
      <button class="btn btn-primary" data-act="fresh-close">もういちど</button>
      <button class="btn" data-act="cancel">とじる</button>
    </div>`);
	showOverlay(lines.join(""));
}

/* ---- ライト／ダーク ---- */

function applyThemeMode(mode) {
	document.documentElement.dataset.mode = mode;
	// 明暗スイッチ（role="switch"）: 暗い画面のとき on
	elBtnTheme.setAttribute("aria-checked", mode === "dark" ? "true" : "false");
	// PWA として起動したときのステータスバー色を、style.css の --bg に合わせる
	const meta = document.querySelector('meta[name="theme-color"]');
	if (meta) {
		const bg = getComputedStyle(document.documentElement)
			.getPropertyValue("--bg")
			.trim();
		if (bg) meta.setAttribute("content", bg);
	}
}

function registerServiceWorker() {
	// オフライン起動用。file:// や非対応ブラウザでは何もしない
	if (!("serviceWorker" in navigator)) return;
	if (location.protocol !== "https:" && location.hostname !== "localhost")
		return;
	navigator.serviceWorker.register("./sw.js").catch(() => {
		/* 登録できなくてもゲームは動く */
	});
}

function initTheme() {
	let mode = null;
	try {
		mode = localStorage.getItem(THEME_KEY);
	} catch (e) {
		/* 読めなければ既定へ */
	}
	if (mode !== "light" && mode !== "dark") {
		// Artifact 等のホストがテーマを示していればそれに、なければ OS 設定に合わせる
		const host = document.documentElement.getAttribute("data-theme");
		if (host === "light" || host === "dark") mode = host;
		else if (
			window.matchMedia &&
			window.matchMedia("(prefers-color-scheme: light)").matches
		)
			mode = "light";
		else mode = "dark";
	}
	applyThemeMode(mode);
}

/* ---- 初期化 ---- */

async function loadDigits() {
	let bcd;
	if (typeof window.PI_BCD_BASE64 === "string") {
		const bin = atob(window.PI_BCD_BASE64);
		bcd = new Uint8Array(bin.length);
		for (let i = 0; i < bin.length; i++) bcd[i] = bin.charCodeAt(i);
	} else {
		const res = await fetch("pi_bcd.bin");
		if (!res.ok) throw new Error(`pi_bcd.bin が読めません (${res.status})`);
		bcd = new Uint8Array(await res.arrayBuffer());
	}
	if (bcd.length !== TOTAL_DIGITS / 2)
		throw new Error("pi_bcd.bin のサイズが違います");
	digits = new Uint8Array(TOTAL_DIGITS);
	for (let i = 0; i < bcd.length; i++) {
		digits[2 * i] = bcd[i] >> 4;
		digits[2 * i + 1] = bcd[i] & 0x0f;
	}
	if (Array.from(digits.slice(0, 8)).join("") !== "31415926") {
		throw new Error("円周率データの先頭が 3141 5926 になっていません");
	}
}

function bindEvents() {
	elBoard.addEventListener("pointerdown", onPointerDown);
	elBoard.addEventListener("pointermove", onPointerMove);
	elBoard.addEventListener("pointerup", onPointerUp);
	elBoard.addEventListener("pointercancel", onPointerUp);

	elBtnAuto.addEventListener("click", showAutoDialog);
	elBtnStop.addEventListener("click", stopAuto);
	elBtnUndo.addEventListener("click", onUndo);
	elBtnReset.addEventListener("click", () => {
		if (
			cleared > 0 &&
			!window.confirm("最初からにしますか？いまの進みは消えます。")
		)
			return;
		resetState();
		saveState();
		renderAll();
	});

	elBtnTheme.addEventListener("click", () => {
		const next =
			document.documentElement.dataset.mode === "dark" ? "light" : "dark";
		applyThemeMode(next);
		try {
			localStorage.setItem(THEME_KEY, next);
		} catch (e) {
			/* 保存できなくてもよい */
		}
	});

	elSpeed.addEventListener("input", () => {
		elSpeedLabel.textContent = SPEED_LABELS[Number(elSpeed.value)];
	});

	elOverlay.addEventListener("click", (e) => {
		const act = e.target && e.target.dataset ? e.target.dataset.act : undefined;
		if (!act) return;
		hideOverlay();
		if (act === "resume") startAuto(false);
		if (act === "fresh") startAuto(true);
		if (act === "fresh-close") {
			resetState();
			saveState();
			renderAll();
		}
	});

	document.addEventListener("visibilitychange", () => {
		if (document.visibilityState === "hidden") saveState();
	});
}

async function init() {
	initTheme();
	registerServiceWorker();
	elSpeedLabel.textContent = SPEED_LABELS[Number(elSpeed.value)];
	bindEvents();
	try {
		await loadDigits();
	} catch (err) {
		elStatus.textContent = `データを読み込めませんでした: ${err.message}`;
		elPCap.textContent =
			"ローカルで開くときは python3 -m http.server などのWebサーバ経由で開いてください";
		return;
	}
	resetState();
	loadState();
	renderAll();
}

init();
