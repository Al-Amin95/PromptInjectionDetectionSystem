const promptInp = document.getElementById("promptInput");
const charCnt = document.getElementById("charCount");
const testBtn = document.getElementById("testBtn");
const clearBtn = document.getElementById("clearBtn");
const recentList = document.getElementById("recentList");

promptInp.addEventListener("input", () => {
  charCnt.textContent = promptInp.value.length;
});

async function runAnalysis() {
  const txt = promptInp.value.trim();
  if (!txt) {
    alert("Please enter a prompt first.");
    return;
  }

  testBtn.disabled = true;
  testBtn.textContent = "Analysing...";

  try {
    const prediction = await postJson("/api/predict", { prompt: txt });

    if (prediction.error) {
      alert(prediction.error);
      return;
    }

    showAnalysis(prediction);
    showNotes(prediction);
    showShap(prediction.tokens || []);
    showTokenTable(prediction.tokens || []);
    prependRecent(txt, prediction);
  } catch (err) {
    alert("Something went wrong while analysing the prompt.");
  } finally {
    testBtn.disabled = false;
    testBtn.textContent = "Test Prompt";
  }
}

testBtn.addEventListener("click", runAnalysis);

promptInp.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (!testBtn.disabled) runAnalysis();
  }
});

clearBtn.addEventListener("click", () => {
  promptInp.value = "";
  charCnt.textContent = "0";
  promptInp.focus();
});

function showNotes(prediction) {
  const box = document.getElementById("promptNotes");
  if (!box) return;
  box.innerHTML = "";

  const notes = [];
  if (prediction.translation_note) {
    notes.push({ text: prediction.translation_note, cls: "note-info" });
  }
  if (prediction.truncated_warning) {
    notes.push({ text: "✂ " + prediction.truncated_warning, cls: "note-info" });
  }
  if (prediction.shap_error) {
    notes.push({ text: prediction.shap_error, cls: "note-warn" });
  }

  notes.forEach((n) => {
    const div = document.createElement("div");
    div.className = "prompt-note " + n.cls;
    div.textContent = n.text;
    box.appendChild(div);
  });
}

function resetAnalysis() {
  const notesBox = document.getElementById("promptNotes");
  if (notesBox) notesBox.innerHTML = "";

  document.getElementById("predictionValue").textContent = "-";
  document.getElementById("predictionValue").className = "stat-value";

  document.getElementById("confidenceValue").textContent = "0%";
  document.getElementById("confidenceBar").style.width = "0%";
  document.getElementById("safeProbValue").textContent = "0%";
  document.getElementById("safeProbBar").style.width = "0%";
  document.getElementById("injectionProbValue").textContent = "0%";
  document.getElementById("injectionProbBar").style.width = "0%";

  const pillsBox = document.getElementById("tokenPills");
  pillsBox.innerHTML =
    '<span class="page-subtitle">Run a prompt above to see token-level SHAP values here.</span>';

  const tableBody = document.getElementById("tokenTableBody");
  tableBody.innerHTML =
    '<tr><td colspan="5" style="text-align:center; color:var(--text-dim);">Run a prompt above to see token values here.</td></tr>';
}

function prependRecent(promptTxt, prediction) {
  if (!recentList) return;

  const onlyChild =
    recentList.children.length === 1 ? recentList.children[0] : null;
  if (onlyChild && !onlyChild.dataset.timestamp) {
    onlyChild.remove();
  }

  const recentItem = document.createElement("div");
  recentItem.className = "recent-item";
  recentItem.dataset.timestamp =
    prediction.timestamp || new Date().toISOString();

  const dot = document.createElement("span");
  dot.className =
    "dot " + (prediction.is_injection ? "dot-injection" : "dot-safe");

  const label = document.createElement("span");
  label.textContent = promptTxt.slice(0, 60);

  recentItem.appendChild(dot);
  recentItem.appendChild(label);
  attachRecentClickHandler(recentItem);

  recentList.insertBefore(recentItem, recentList.firstChild);
}

function restoreFromRecord(record) {
  promptInp.value = record.prompt || "";
  charCnt.textContent = promptInp.value.length;

  const isInjection = (record.prediction || "").indexOf("INJECT") !== -1;
  const prediction = {
    prediction: record.prediction,
    is_injection: isInjection,
    confidence: record.confidence,
    safe_probability: record.safe_probability,
    injection_probability: record.injection_probability,
  };

  showAnalysis(prediction);
  showNotes(record);
  showShap(record.tokens || []);
  showTokenTable(record.tokens || []);
}

function attachRecentClickHandler(recentItem) {
  recentItem.addEventListener("click", async () => {
    const ts = recentItem.dataset.timestamp;
    if (!ts) return;
    try {
      const hist = await getJson("/api/history");
      const record = hist.find((r) => r.timestamp === ts);
      if (record) restoreFromRecord(record);
    } catch (err) {}
  });
}

document
  .querySelectorAll(".recent-item[data-timestamp]")
  .forEach(attachRecentClickHandler);

function showAnalysis(prediction) {
  const predEl = document.getElementById("predictionValue");
  predEl.textContent = prediction.prediction;
  predEl.className =
    "stat-value " + (prediction.is_injection ? "injection" : "safe");

  document.getElementById("confidenceValue").textContent =
    prediction.confidence + "%";
  document.getElementById("confidenceBar").style.width =
    prediction.confidence + "%";

  document.getElementById("safeProbValue").textContent =
    prediction.safe_probability + "%";
  document.getElementById("safeProbBar").style.width =
    prediction.safe_probability + "%";

  document.getElementById("injectionProbValue").textContent =
    prediction.injection_probability + "%";
  document.getElementById("injectionProbBar").style.width =
    prediction.injection_probability + "%";
}

function showShap(toks) {
  const container = document.getElementById("tokenPills");
  container.innerHTML = "";

  if (!toks.length) {
    container.innerHTML =
      '<span class="page-subtitle">No SHAP values to show for this prompt.</span>';
    return;
  }

  toks.forEach((t) => {
    const pill = document.createElement("span");
    pill.className =
      "token-pill " + (t.direction === "SAFE" ? "safe" : "injection");
    pill.textContent = t.token;
    container.appendChild(pill);
  });
}

function showTokenTable(toks) {
  const body = document.getElementById("tokenTableBody");
  body.innerHTML = "";

  if (!toks.length) {
    body.innerHTML =
      '<tr><td colspan="5" style="text-align:center; color:var(--text-dim);">No token values to show for this prompt.</td></tr>';
    return;
  }

  toks.forEach((t) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${t.token}</td>
      <td>${t.shap_value}</td>
      <td><span class="tag ${t.direction === "SAFE" ? "tag-safe" : "tag-injection"}">${t.direction}</span></td>
      <td>${t.strength}</td>
      <td>${t.explanation}</td>
    `;
    body.appendChild(row);
  });
}
