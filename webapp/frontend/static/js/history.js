const searchInp = document.getElementById("searchInput");
const predFilter = document.getElementById("predictionFilter");
const rows = Array.from(
  document.querySelectorAll("#historyTableBody tr[data-prompt]"),
);
const pageSz = 10;
let curPage = 1;

function applyFilters() {
  const search = searchInp.value.toLowerCase();
  const filterVal = predFilter.value;

  return rows.filter((row) => {
    const matchesSearch = row.dataset.prompt.includes(search);
    const matchesFilter =
      filterVal === "all" || row.dataset.prediction === filterVal;
    return matchesSearch && matchesFilter;
  });
}

function render() {
  const visible = applyFilters();
  rows.forEach((r) => (r.style.display = "none"));

  const totalPages = Math.max(1, Math.ceil(visible.length / pageSz));
  curPage = Math.min(curPage, totalPages);

  const start = (curPage - 1) * pageSz;
  visible.slice(start, start + pageSz).forEach((r) => (r.style.display = ""));

  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  const container = document.getElementById("pagination");
  container.innerHTML = "";

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    if (i === curPage) btn.classList.add("active");
    btn.addEventListener("click", () => {
      curPage = i;
      render();
    });
    container.appendChild(btn);
  }
}

if (rows.length) {
  searchInp.addEventListener("input", () => {
    curPage = 1;
    render();
  });
  predFilter.addEventListener("change", () => {
    curPage = 1;
    render();
  });
  render();
}
