if (window.ChartDataLabels) {
  Chart.register(window.ChartDataLabels);
}

async function loadHistForCharts() {
  const hist = await getJson("/api/history");
  return hist;
}

function isInj(rec) {
  return rec.prediction.indexOf("INJECT") !== -1;
}

const gridStyle = {
  color: "#232733",
  drawBorder: false,
};

const noGrid = { display: false };

const tickStyle = {
  color: "#9aa0ac",
  font: { size: 11 },
};

const bottomLegend = {
  position: "bottom",
  labels: {
    color: "#c7cbd6",
    usePointStyle: true,
    pointStyle: "rect",
    boxWidth: 10,
    boxHeight: 10,
    padding: 16,
  },
};

const barLabelStyle = {
  color: "#e6e8ee",
  anchor: "end",
  align: "top",
  font: { size: 11, weight: "600" },
};

let trendChartInstance = null;

async function buildTrendChart(canvasId, rangeMinutes) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  let hist = await loadHistForCharts();

  if (rangeMinutes) {
    const cutoff = Date.now() - rangeMinutes * 60 * 1000;
    hist = hist.filter((r) => new Date(r.timestamp + "Z").getTime() >= cutoff);
  }

  const byMinute = {};
  hist.forEach((r) => {
    const minKey = r.timestamp.slice(0, 16);
    if (!byMinute[minKey]) byMinute[minKey] = { safeCnt: 0, injCnt: 0 };
    if (isInj(r)) byMinute[minKey].injCnt += 1;
    else byMinute[minKey].safeCnt += 1;
  });

  const minutes = Object.keys(byMinute).sort();
  const labels = minutes.map((m) => m.slice(11, 16));

  if (trendChartInstance) {
    trendChartInstance.destroy();
    trendChartInstance = null;
  }

  trendChartInstance = new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Safe",
          data: minutes.map((m) => byMinute[m].safeCnt),
          backgroundColor: "#22c55e",
          borderRadius: 4,
          maxBarThickness: 18,
        },
        {
          label: "Injection",
          data: minutes.map((m) => byMinute[m].injCnt),
          backgroundColor: "#ef4444",
          borderRadius: 4,
          maxBarThickness: 18,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: noGrid, ticks: tickStyle },
        y: {
          beginAtZero: true,
          ticks: { ...tickStyle, precision: 0 },
          grid: gridStyle,
        },
      },
      plugins: { legend: bottomLegend, datalabels: { display: false } },
    },
  });
}

async function buildPieChart(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const hist = await loadHistForCharts();
  const safeCnt = hist.filter((r) => !isInj(r)).length;
  const injCnt = hist.length - safeCnt;

  new Chart(canvas, {
    type: "pie",
    data: {
      labels: ["Safe", "Injection"],
      datasets: [
        {
          data: [safeCnt, injCnt],
          backgroundColor: ["#22c55e", "#ef4444"],
          borderColor: "#101218",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: bottomLegend,
        datalabels: {
          color: "#0b0e17",
          font: { weight: "700", size: 12 },
          formatter: (value, ctx) => {
            const total = ctx.chart.data.datasets[0].data.reduce(
              (a, b) => a + b,
              0,
            );
            if (!total) return "";
            return Math.round((value / total) * 100) + "%";
          },
        },
      },
    },
  });
}

async function buildConfidenceChart(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const hist = await loadHistForCharts();
  const buckets = { "50-70%": 0, "70-90%": 0, "90-100%": 0 };

  hist.forEach((r) => {
    if (r.confidence < 70) buckets["50-70%"] += 1;
    else if (r.confidence < 90) buckets["70-90%"] += 1;
    else buckets["90-100%"] += 1;
  });

  new Chart(canvas, {
    type: "pie",
    data: {
      labels: Object.keys(buckets),
      datasets: [
        {
          data: Object.values(buckets),
          backgroundColor: ["#f59e0b", "#2f6df6", "#22c55e"],
          borderColor: "#101218",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: bottomLegend,
        datalabels: {
          color: "#0b0e17",
          font: { weight: "700", size: 12 },
          formatter: (value, ctx) => {
            const total = ctx.chart.data.datasets[0].data.reduce(
              (a, b) => a + b,
              0,
            );
            if (!total) return "";
            return Math.round((value / total) * 100) + "%";
          },
        },
      },
    },
  });
}

const STOPWORDS = new Set([
  "the",
  "a",
  "an",
  "is",
  "are",
  "was",
  "were",
  "be",
  "been",
  "to",
  "of",
  "and",
  "or",
  "in",
  "on",
  "at",
  "for",
  "with",
  "as",
  "this",
  "that",
  "it",
  "its",
  "you",
  "your",
  "i",
  "my",
  "me",
  "we",
  "our",
  "they",
  "them",
  "he",
  "she",
  "his",
  "her",
  "do",
  "does",
  "did",
  "can",
  "could",
  "will",
  "would",
  "should",
  "have",
  "has",
  "had",
  "not",
  "if",
  "so",
  "but",
  "from",
  "by",
  "about",
  "into",
  "up",
  "out",
]);

async function buildKeywordChart(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const hist = await loadHistForCharts();
  const cnts = {};

  hist.filter(isInj).forEach((r) => {
    const words = r.prompt.toLowerCase().match(/[a-z']{3,}/g) || [];
    words.forEach((w) => {
      if (STOPWORDS.has(w)) return;
      cnts[w] = (cnts[w] || 0) + 1;
    });
  });

  const topWords = Object.entries(cnts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  const labels = topWords.map((w) => w[0]);
  const values = topWords.map((w) => w[1]);

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels.length ? labels : ["No injection prompts tested yet"],
      datasets: [
        {
          label: "Occurrences",
          data: values.length ? values : [0],
          backgroundColor: "#ef4444",
          borderRadius: 4,
          maxBarThickness: 26,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      scales: {
        x: {
          beginAtZero: true,
          ticks: { ...tickStyle, precision: 0 },
          grid: gridStyle,
        },
        y: { ticks: tickStyle, grid: noGrid },
      },
      plugins: {
        legend: { display: false },
        datalabels: { ...barLabelStyle, anchor: "end", align: "right" },
      },
    },
  });
}

function buildHourlyHeatmap(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  loadHistForCharts().then((hist) => {
    const hourCnts = new Array(24).fill(0);
    hist.forEach((r) => {
      const hr = new Date(r.timestamp).getUTCHours();
      hourCnts[hr] += 1;
    });
    const maxCnt = Math.max(1, ...hourCnts);

    container.innerHTML = "";
    hourCnts.forEach((cnt, hr) => {
      const bar = document.createElement("div");
      bar.className = "hour-bar";
      bar.title = `${hr}:00 - ${cnt} prompts`;
      const fill = document.createElement("div");
      fill.className = "hour-bar-fill";
      fill.style.height = `${(cnt / maxCnt) * 100}%`;
      bar.appendChild(fill);
      container.appendChild(bar);
    });
  });
}

const rangeSelectEl = document.getElementById("rangeSelect");
const initialRange = rangeSelectEl ? Number(rangeSelectEl.value) : 0;

buildTrendChart("trendChart", initialRange || null);
buildPieChart("pieChart");
buildConfidenceChart("confidenceChart");
buildKeywordChart("keywordChart");
buildHourlyHeatmap("hourlyHeatmap");

if (rangeSelectEl) {
  rangeSelectEl.addEventListener("change", () => {
    const minutes = Number(rangeSelectEl.value);
    buildTrendChart("trendChart", minutes || null);
  });
}
