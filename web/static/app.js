document.getElementById("scanForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const dockerHost = document.getElementById("dockerHost").value.trim();
  const composeFile = document.getElementById("composeFile").files[0];
  const projectName = document.getElementById("projectName").value.trim();

  const statusEl = document.getElementById("status");

  if (!composeFile) {
    statusEl.textContent = "請先選擇 docker-compose.yml 檔案";
    return;
  }

  statusEl.textContent = "診斷中，請稍候...";
  setLoading(true);

  const formData = new FormData();
  formData.append("compose_file", composeFile);
  formData.append("docker_host", dockerHost);
  formData.append("project_name", projectName);

  try {
    const res = await fetch("/api/scan", { method: "POST", body: formData });
    if (!res.ok) {
      const err = await res.json();
      alert("錯誤：" + (err.detail || "未知錯誤"));
      return;
    }
    const data = await res.json();
    renderResults(data);
    statusEl.textContent = "診斷完成，結果如下 ↓";
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    statusEl.textContent = "顯示結果時發生錯誤：" + err.message;
  } finally {
    setLoading(false);
  }
});

function setLoading(on) {
  document.getElementById("loading").classList.toggle("hidden", !on);
  if (on) {
    document.getElementById("results").classList.add("hidden");
  }
  document.getElementById("scanBtn").disabled = on;
}

function renderResults(data) {
  // Compose issues
  const composeIssues = data.compose?.issues || [];
  renderList("composeIssues", composeIssues, "未發現 Compose 設定問題");

  // Container status
  const status = data.containers?.status || {};
  const grid = document.getElementById("containerStatus");
  grid.innerHTML = "";
  if (Object.keys(status).length === 0) {
    grid.innerHTML = "<p style='color:#94a3b8;font-size:0.9rem'>無法取得 container 狀態</p>";
  } else {
    const div = document.createElement("div");
    div.className = "container-grid";
    for (const [svc, state] of Object.entries(status)) {
      const chip = document.createElement("span");
      chip.className = `container-chip state-${state in knownStates ? state : "unknown"}`;
      chip.textContent = `${svc}: ${state}`;
      div.appendChild(chip);
    }
    grid.appendChild(div);
  }
  renderList("containerIssues", data.containers?.issues || [], null);

  // Port conflicts
  const conflicts = data.ports?.conflicts || [];
  renderList("portConflicts", conflicts, "未發現 Port 衝突");

  // Log findings
  const findings = data.logs?.findings || [];
  const findingsEl = document.getElementById("logFindings");
  findingsEl.innerHTML = "";
  if (findings.length === 0) {
    findingsEl.innerHTML = "<ul><li class='ok'>未發現已知錯誤</li></ul>";
  } else {
    for (const f of findings) {
      const div = document.createElement("div");
      div.className = "finding";
      const serviceTag = f.service ? `<span style="color:#f43f5e">[${f.service}]</span> ` : "";
      const suggestions = (f.suggestions || [])
        .map(s => `<li>${s}</li>`).join("");
      div.innerHTML = `
        <div class="title">${serviceTag}${f.title}</div>
        <div class="explanation">${f.explanation}</div>
        <ul class="suggestions">${suggestions}</ul>
      `;
      findingsEl.appendChild(div);
    }
  }

  document.getElementById("results").classList.remove("hidden");
}

function renderList(id, items, emptyMsg) {
  const el = document.getElementById(id);
  el.innerHTML = "";
  if (items.length === 0 && emptyMsg) {
    el.innerHTML = `<li class="ok">${emptyMsg}</li>`;
  } else {
    for (const item of items) {
      const li = document.createElement("li");
      li.textContent = item;
      el.appendChild(li);
    }
  }
}

const knownStates = { running: 1, exited: 1, restarting: 1, unhealthy: 1 };
