let loadedConfig = null;

async function loadConfig() {
  const res = await fetch("/config");
  const config = await res.json();

  loadedConfig = {
    keyword_threshold: config.keyword_threshold ?? 0.75,
    max_keywords: config.max_keywords ?? 20
  };
  console.log(`loadedConfig: ${loadedConfig}`)

  document.getElementById("threshold").value =
    loadedConfig.keyword_threshold;
  document.getElementById("maxKeywords").value =
    loadedConfig.max_keywords;

  updateSaveButton();
}

function currentConfigFromInputs() {
  return {
    keyword_threshold: parseFloat(
      document.getElementById("threshold").value
    ),
    max_keywords: parseInt(
      document.getElementById("maxKeywords").value
    )
  };
}

function hasConfigChanges() {
  if (!loadedConfig) return false;
  const current = currentConfigFromInputs();

  return (
    current.keyword_threshold !== loadedConfig.keyword_threshold ||
    current.max_keywords !== loadedConfig.max_keywords
  );
}

function updateSaveButton() {
  document.getElementById("saveConfigBtn").disabled =
    !hasConfigChanges();
}

async function saveConfig() {
  const config = currentConfigFromInputs();

  await fetch("/config", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config)
  });

  // Update baseline after successful save
  loadedConfig = { ...config };
  updateSaveButton();
}

async function runPipeline() {
  await fetch("/run", { method: "POST" });
}

async function loadCSV() {
  const res = await fetch("/data");
  const text = await res.text();

  const rows = text.trim().split("\n").map(r => r.split(","));
  renderTable(rows);
}

function renderTable(rows) {
  const table = document.getElementById("table");
  table.innerHTML = "";

  rows.forEach((row, i) => {
    const tr = document.createElement("tr");
    row.forEach(cell => {
      const el = document.createElement(i === 0 ? "th" : "td");
      el.textContent = cell;
      tr.appendChild(el);
    });
    table.appendChild(tr);
  });
}

document.getElementById("threshold")
  .addEventListener("input", updateSaveButton);

document.getElementById("maxKeywords")
  .addEventListener("input", updateSaveButton);

document.getElementById("saveConfigBtn").onclick = saveConfig;

document.getElementById("run").onclick = async () => {
  // Optional: auto-save if dirty before running
  if (hasConfigChanges()) {
    await saveConfig();
  }
  await runPipeline();
  await loadCSV();
};

loadConfig()