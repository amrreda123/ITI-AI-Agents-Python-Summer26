// ==========================================================================
// SmartDoc AI — Frontend Application Logic
// ==========================================================================

let allDocuments = [];
let currentDocModalId = null;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initSearchAndFilter();
  initForms();
  initFileUpload();
  initAgentChat();
  initModal();
  loadDocuments();
});

// --- Tab Navigation ---
function initTabs() {
  const navItems = document.querySelectorAll(".nav-item");
  const tabContents = document.querySelectorAll(".tab-content");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const tabMeta = {
    "docs-tab": { title: "Document Repository", subtitle: "Manage, analyze, and query your knowledge base" },
    "create-tab": { title: "Add & Upload Documents", subtitle: "Insert JSON records or upload raw text files" },
    "agent-tab": { title: "Read-Only AI Agent", subtitle: "Ask the autonomous agent to inspect and summarize documents" },
    "api-tab": { title: "Interactive API Documentation", subtitle: "Inspect OpenAPI contracts, Swagger UI, and ReDoc" },
  };

  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      const targetTab = item.dataset.tab;
      if (!targetTab) return;

      navItems.forEach((nav) => nav.classList.remove("active"));
      tabContents.forEach((tab) => tab.classList.remove("active"));

      item.classList.add("active");
      const activeContent = document.getElementById(targetTab);
      if (activeContent) activeContent.classList.add("active");

      if (tabMeta[targetTab]) {
        pageTitle.textContent = tabMeta[targetTab].title;
        pageSubtitle.textContent = tabMeta[targetTab].subtitle;
      }
    });
  });

  // Quick create button in header
  const quickCreateBtn = document.getElementById("quick-create-btn");
  if (quickCreateBtn) {
    quickCreateBtn.addEventListener("click", () => {
      document.getElementById("nav-create-btn").click();
    });
  }
}

// --- Load Documents from API ---
async function loadDocuments() {
  try {
    const res = await fetch("/documents");
    if (!res.ok) throw new Error("Failed to fetch documents");

    allDocuments = await res.json();
    renderDocumentsTable(allDocuments);
    updateStats(allDocuments);
  } catch (err) {
    showToast("Error loading documents: " + err.message, "error");
  }
}

// --- Render Table ---
function renderDocumentsTable(docs) {
  const tbody = document.getElementById("documents-tbody");
  const emptyState = document.getElementById("empty-state");
  const countBadge = document.getElementById("docs-count-badge");

  tbody.innerHTML = "";
  countBadge.textContent = `${docs.length} items`;

  if (docs.length === 0) {
    emptyState.style.display = "block";
    return;
  }
  emptyState.style.display = "none";

  docs.forEach((doc) => {
    const tr = document.createElement("tr");

    const priorityBadge = `<span class="badge priority-p${doc.priority}">P${doc.priority}</span>`;
    const aiBadge = doc.ai_summary
      ? `<span class="badge summary-badge-yes"><i class="fa-solid fa-check"></i> Summarized</span>`
      : `<span class="badge summary-badge-no"><i class="fa-solid fa-minus"></i> Pending</span>`;

    tr.innerHTML = `
      <td><strong>#${doc.id}</strong></td>
      <td><strong>${escapeHtml(doc.title)}</strong></td>
      <td>${priorityBadge}</td>
      <td>${aiBadge}</td>
      <td class="text-muted">${doc.description ? escapeHtml(doc.description) : "<em>No description</em>"}</td>
      <td class="text-right">
        <button class="btn btn-secondary btn-sm mr-1" onclick="openDocModal(${doc.id})">
          <i class="fa-solid fa-eye"></i> View & AI
        </button>
        <button class="btn btn-danger btn-sm" onclick="deleteDocument(${doc.id})">
          <i class="fa-solid fa-trash"></i>
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// --- Update Stats ---
function updateStats(docs) {
  const totalElem = document.getElementById("stat-total-docs");
  const analyzedElem = document.getElementById("stat-analyzed-docs");

  const total = docs.length;
  const analyzed = docs.filter((d) => d.ai_summary && d.ai_summary.trim() !== "").length;

  if (totalElem) totalElem.textContent = total;
  if (analyzedElem) analyzedElem.textContent = analyzed;
}

// --- Search and Filter ---
function initSearchAndFilter() {
  const searchInput = document.getElementById("global-search");
  const priorityFilter = document.getElementById("priority-filter");
  const refreshBtn = document.getElementById("refresh-docs-btn");

  function applyFilters() {
    const query = (searchInput.value || "").toLowerCase().trim();
    const priorityVal = priorityFilter.value;

    const filtered = allDocuments.filter((doc) => {
      const matchQuery =
        !query ||
        doc.title.toLowerCase().includes(query) ||
        (doc.content && doc.content.toLowerCase().includes(query)) ||
        (doc.description && doc.description.toLowerCase().includes(query));

      const matchPriority = priorityVal === "all" || doc.priority.toString() === priorityVal;

      return matchQuery && matchPriority;
    });

    renderDocumentsTable(filtered);
  }

  if (searchInput) searchInput.addEventListener("input", applyFilters);
  if (priorityFilter) priorityFilter.addEventListener("change", applyFilters);
  if (refreshBtn) refreshBtn.addEventListener("click", loadDocuments);
}

// --- Forms (Create Document) ---
function initForms() {
  const form = document.getElementById("create-doc-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("doc-title").value.trim();
    const priority = parseInt(document.getElementById("doc-priority").value, 10);
    const description = document.getElementById("doc-desc").value.trim() || null;
    const content = document.getElementById("doc-content").value.trim();

    const payload = { title, content, priority, description };

    try {
      const res = await fetch("/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : "Creation failed");
      }

      const created = await res.json();
      showToast(`Document #${created.id} created successfully! (201 Created)`, "success");
      form.reset();
      document.getElementById("doc-priority").value = "3";
      await loadDocuments();
      document.getElementById("nav-docs-btn").click();
    } catch (err) {
      showToast("Error creating document: " + err.message, "error");
    }
  });
}

// --- File Upload ---
function initFileUpload() {
  const dropzone = document.getElementById("upload-dropzone");
  const fileInput = document.getElementById("file-input");
  const chooseFileBtn = document.getElementById("choose-file-btn");
  const uploadBtn = document.getElementById("upload-file-btn");
  const fileInfo = document.getElementById("selected-file-info");
  const filenameElem = document.getElementById("selected-filename");
  const clearFileBtn = document.getElementById("clear-file-btn");

  let selectedFile = null;

  if (chooseFileBtn && fileInput) {
    chooseFileBtn.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("click", (e) => {
      if (e.target !== clearFileBtn && !clearFileBtn.contains(e.target)) {
        fileInput.click();
      }
    });
  }

  if (dropzone) {
    ["dragenter", "dragover"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach((eventName) => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files.length > 0) {
        handleFileSelected(e.dataTransfer.files[0]);
      }
    });
  }

  if (fileInput) {
    fileInput.addEventListener("change", () => {
      if (fileInput.files.length > 0) {
        handleFileSelected(fileInput.files[0]);
      }
    });
  }

  function handleFileSelected(file) {
    if (!file.name.endsWith(".txt") && file.type !== "text/plain") {
      showToast("Only .txt files are supported!", "error");
      return;
    }
    selectedFile = file;
    filenameElem.textContent = file.name;
    fileInfo.style.display = "inline-flex";
    uploadBtn.disabled = false;
  }

  if (clearFileBtn) {
    clearFileBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      selectedFile = null;
      fileInput.value = "";
      fileInfo.style.display = "none";
      uploadBtn.disabled = true;
    });
  }

  if (uploadBtn) {
    uploadBtn.addEventListener("click", async () => {
      if (!selectedFile) return;

      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Uploading...`;

        const res = await fetch("/documents/upload", {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Upload failed");
        }

        const doc = await res.json();
        showToast(`File uploaded as Document #${doc.id}!`, "success");

        // Reset
        selectedFile = null;
        fileInput.value = "";
        fileInfo.style.display = "none";
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = `<i class="fa-solid fa-upload"></i> Process & Upload (/documents/upload)`;

        await loadDocuments();
        document.getElementById("nav-docs-btn").click();
      } catch (err) {
        showToast("Upload error: " + err.message, "error");
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = `<i class="fa-solid fa-upload"></i> Process & Upload (/documents/upload)`;
      }
    });
  }
}

// --- Delete Document ---
async function deleteDocument(docId) {
  if (!confirm(`Are you sure you want to permanently delete Document #${docId}?`)) return;

  try {
    const res = await fetch(`/documents/${docId}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete document");

    showToast(`Document #${docId} deleted successfully.`, "info");
    await loadDocuments();
  } catch (err) {
    showToast("Delete error: " + err.message, "error");
  }
}

// --- Modal & AI Analysis ---
function initModal() {
  const modal = document.getElementById("doc-modal");
  const closeBtns = [document.getElementById("close-modal-btn"), document.getElementById("modal-close-footer-btn")];
  const analyzeBtn = document.getElementById("modal-analyze-btn");

  closeBtns.forEach((btn) => {
    if (btn) btn.addEventListener("click", () => (modal.style.display = "none"));
  });

  if (analyzeBtn) {
    analyzeBtn.addEventListener("click", () => {
      if (currentDocModalId) {
        triggerAIAnalysis(currentDocModalId);
      }
    });
  }
}

async function openDocModal(docId) {
  currentDocModalId = docId;
  const modal = document.getElementById("doc-modal");

  try {
    const res = await fetch(`/documents/${docId}`);
    if (!res.ok) throw new Error("Document not found");

    const doc = await res.json();

    document.getElementById("modal-doc-title").textContent = `#${doc.id} - ${doc.title}`;
    document.getElementById("modal-doc-content").textContent = doc.content;

    const priorityBadge = document.getElementById("modal-priority-badge");
    priorityBadge.className = `badge priority-badge priority-p${doc.priority}`;
    priorityBadge.textContent = `Priority ${doc.priority}`;

    // Reset AI Box
    document.getElementById("modal-ai-loading").style.display = "none";
    if (doc.ai_summary) {
      document.getElementById("modal-ai-empty").style.display = "none";
      document.getElementById("modal-ai-result").style.display = "block";
      document.getElementById("ai-summary-text").textContent = doc.ai_summary;
      document.getElementById("ai-category").textContent = "Extracted";
      document.getElementById("ai-suggested-priority").textContent = `Priority: ${doc.priority}`;
      document.getElementById("ai-keypoints-list").innerHTML = "<li>Extracted directly from database storage.</li>";
    } else {
      document.getElementById("modal-ai-empty").style.display = "block";
      document.getElementById("modal-ai-result").style.display = "none";
    }

    modal.style.display = "flex";
  } catch (err) {
    showToast(err.message, "error");
  }
}

async function triggerAIAnalysis(docId) {
  const loadingBox = document.getElementById("modal-ai-loading");
  const resultBox = document.getElementById("modal-ai-result");
  const emptyBox = document.getElementById("modal-ai-empty");
  const analyzeBtn = document.getElementById("modal-analyze-btn");

  emptyBox.style.display = "none";
  resultBox.style.display = "none";
  loadingBox.style.display = "flex";
  analyzeBtn.disabled = true;

  try {
    const res = await fetch(`/documents/${docId}/analyze`, { method: "POST" });
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || "Analysis request failed");
    }

    const data = await res.json();

    loadingBox.style.display = "none";
    resultBox.style.display = "block";

    document.getElementById("ai-category").textContent = data.category || "general";
    document.getElementById("ai-suggested-priority").textContent = `Suggested Priority: ${data.suggested_priority || 3}`;
    document.getElementById("ai-summary-text").textContent = data.summary;

    const keypointsList = document.getElementById("ai-keypoints-list");
    keypointsList.innerHTML = "";
    (data.key_points || []).forEach((pt) => {
      const li = document.createElement("li");
      li.textContent = pt;
      keypointsList.appendChild(li);
    });

    showToast("Gemini Analysis completed and saved to database!", "success");
    await loadDocuments();
  } catch (err) {
    loadingBox.style.display = "none";
    emptyBox.style.display = "block";
    showToast("AI Analysis failed: " + err.message, "error");
  } finally {
    analyzeBtn.disabled = false;
  }
}

// --- AI Agent Chat ---
function initAgentChat() {
  const form = document.getElementById("agent-chat-form");
  const input = document.getElementById("agent-message-input");
  const messagesContainer = document.getElementById("chat-messages");
  const clearBtn = document.getElementById("clear-chat-btn");
  const chips = document.querySelectorAll(".prompt-chips .chip");

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      input.value = chip.dataset.prompt;
      input.focus();
    });
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      messagesContainer.innerHTML = `
        <div class="chat-bubble bot">
          <div class="bubble-header">
            <span class="bot-badge"><i class="fa-solid fa-shield-halved"></i> SmartDoc Agent</span>
            <span class="time">Just now</span>
          </div>
          <div class="bubble-body">
            Chat cleared. Ready for your next document query!
          </div>
        </div>
      `;
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const message = input.value.trim();
      if (!message) return;

      appendUserBubble(message);
      input.value = "";

      const loadingBubble = appendLoadingBubble();
      messagesContainer.scrollTop = messagesContainer.scrollHeight;

      try {
        const res = await fetch("/agent/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message }),
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Agent request failed");
        }

        const agentData = await res.json();
        loadingBubble.remove();
        appendBotBubble(agentData.answer, agentData.steps_taken, agentData.tools_called);
      } catch (err) {
        loadingBubble.remove();
        appendBotBubble(`⚠️ Error communicating with Agent: ${err.message}`, 0, []);
      }

      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
  }

  function appendUserBubble(text) {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble user";
    bubble.innerHTML = `
      <div class="bubble-header">
        <span>You</span>
        <span class="time">${getCurrentTime()}</span>
      </div>
      <div class="bubble-body">${escapeHtml(text)}</div>
    `;
    messagesContainer.appendChild(bubble);
  }

  function appendLoadingBubble() {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble bot";
    bubble.innerHTML = `
      <div class="bubble-header">
        <span class="bot-badge"><i class="fa-solid fa-spinner fa-spin"></i> SmartDoc Agent</span>
        <span class="time">Reasoning...</span>
      </div>
      <div class="bubble-body"><em>Agent is evaluating tools and inspecting documents...</em></div>
    `;
    messagesContainer.appendChild(bubble);
    return bubble;
  }

  function appendBotBubble(answer, steps, tools) {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble bot";

    const toolsFormatted = (tools && tools.length > 0)
      ? tools.map((t) => `<code>${t}</code>`).join(", ")
      : "<em>Direct Answer</em>";

    bubble.innerHTML = `
      <div class="bubble-header">
        <span class="bot-badge"><i class="fa-solid fa-robot"></i> SmartDoc Agent</span>
        <span class="time">${getCurrentTime()}</span>
      </div>
      <div class="bubble-body">${escapeHtml(answer).replace(/\n/g, "<br/>")}</div>
      <div class="bubble-meta">
        <span><i class="fa-solid fa-shoe-prints"></i> Steps: ${steps}</span>
        <span><i class="fa-solid fa-toolbox"></i> Tools: ${toolsFormatted}</span>
      </div>
    `;
    messagesContainer.appendChild(bubble);
  }
}

// --- Utilities ---
function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  const icon =
    type === "success"
      ? "fa-circle-check"
      : type === "error"
      ? "fa-circle-exclamation"
      : "fa-circle-info";

  toast.innerHTML = `
    <i class="fa-solid ${icon}"></i>
    <span>${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
