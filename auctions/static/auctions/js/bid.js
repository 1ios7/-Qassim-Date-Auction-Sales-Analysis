function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  const mm = String(m).padStart(2, "0");
  const ss = String(s).padStart(2, "0");
  return `${mm}:${ss}`;
}

let endAtMs = null;

// عداد لحظي محلي (بدون ضغط سيرفر)
setInterval(() => {
  const cdEl = document.getElementById("countdown");
  if (!cdEl || endAtMs === null) return;

  const remaining = Math.max(0, Math.floor((endAtMs - Date.now()) / 1000));
  cdEl.textContent = fmtTime(remaining);
}, 1000);

async function pollStatus() {
  if (!window.AUCTION_STATUS_URL) return;

  try {
    const res = await fetch(window.AUCTION_STATUS_URL, { cache: "no-store" });
    const data = await res.json();

    const priceEl = document.getElementById("currentPrice");
    if (priceEl) priceEl.textContent = `${data.current_price} ر.س`;

    // نخزن وقت النهاية مرة ونحسب محليًا كل ثانية
    if (typeof data.ends_in_seconds === "number") {
      endAtMs = Date.now() + (data.ends_in_seconds * 1000);
    }

    const bidsBox = document.getElementById("bidsBox");
    if (bidsBox && Array.isArray(data.top_bids)) {
      bidsBox.innerHTML = "";
      data.top_bids.forEach((b) => {
        const row = document.createElement("div");
        row.className = "p-3 rounded-2xl border bg-[#F6F1E9] flex items-center justify-between";
        row.innerHTML = `
          <div class="text-sm font-bold">${b["bidder__username"]}</div>
          <div class="font-extrabold" style="color:#C9A24D">${b.amount} ر.س</div>
        `;
        bidsBox.appendChild(row);
      });

      if (data.top_bids.length === 0) {
        bidsBox.innerHTML = `<div class="p-3 rounded-2xl border bg-[#F6F1E9]">لا توجد مزايدات.</div>`;
      }
    }
  } catch (e) {}
}

// خله أسرع (شبه لحظي) بدون ما يجلد السيرفر مرة
setInterval(pollStatus, 1000);
pollStatus();
