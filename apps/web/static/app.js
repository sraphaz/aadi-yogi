const questionEl = document.getElementById("question");
const askBtn = document.getElementById("ask-btn");
const statusEl = document.getElementById("status");
const answerBox = document.getElementById("answer-box");
const answerText = document.getElementById("answer-text");
const providerLine = document.getElementById("provider-line");
const cautionBox = document.getElementById("caution-box");
const citationsBox = document.getElementById("citations-box");
const citationsList = document.getElementById("citations-list");
const sourcesBox = document.getElementById("sources-box");
const sourcesList = document.getElementById("sources-list");

function hideResults() {
  [answerBox, cautionBox, citationsBox, sourcesBox].forEach((el) => el.classList.add("hidden"));
}

async function askQuestion() {
  const question = questionEl.value.trim();
  if (question.length < 3) {
    statusEl.textContent = "Escreva uma pergunta com pelo menos 3 caracteres.";
    return;
  }

  hideResults();
  askBtn.disabled = true;
  statusEl.textContent = "Consultando fontes e preparando resposta...";

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, top_k: 5 }),
    });

    if (!response.ok) {
      throw new Error(`Erro ${response.status}`);
    }

    const data = await response.json();
    answerText.textContent = data.answer;
    providerLine.textContent = `Provedor: ${data.provider} · Modelo: ${data.model}`;
    answerBox.classList.remove("hidden");

    if (data.caution) {
      cautionBox.textContent = data.caution;
      cautionBox.classList.remove("hidden");
    }

    citationsList.innerHTML = "";
    (data.citations || []).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item.replace(/^-\s*/, "");
      citationsList.appendChild(li);
    });
    citationsBox.classList.remove("hidden");

    sourcesList.innerHTML = "";
    (data.retrieved_chunks || []).forEach((chunk) => {
      const card = document.createElement("article");
      card.className = "source-card";
      card.innerHTML = `
        <h3>${chunk.source_id} · score ${chunk.score.toFixed(2)}</h3>
        <p>${chunk.excerpt}</p>
      `;
      sourcesList.appendChild(card);
    });
    sourcesBox.classList.remove("hidden");

    statusEl.textContent = "Resposta pronta.";
  } catch (error) {
    statusEl.textContent = "Falha ao consultar a API. Verifique se o servidor está ativo.";
    console.error(error);
  } finally {
    askBtn.disabled = false;
  }
}

askBtn.addEventListener("click", askQuestion);
questionEl.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    askQuestion();
  }
});

fetch("/health")
  .then((response) => response.json())
  .then((data) => {
    const llm = data.llm_configured ? "LLM ativo" : "modo fallback (sem LLM)";
    const index = data.vector_index ? "índice vetorial ok" : "índice vetorial ausente";
    statusEl.textContent = `API online · ${llm} · ${index}`;
  })
  .catch(() => {
    statusEl.textContent = "API offline.";
  });
