import { scenarios } from "./scenarios.js";
import { runSimulation } from "./api.js";
import { renderLineChart } from "./chart.js";

const form = document.getElementById("axiom-form");
const scenarioSelect = document.getElementById("scenario");
const scenarioDescription = document.getElementById("scenario-description");
const chartCanvas = document.getElementById("chart");
const componentsBody = document.getElementById("components-body");
const summary = document.getElementById("summary");
const errorMessage = document.getElementById("error");
const instantScore = document.getElementById("instant-score");
const instantAbc = document.getElementById("instant-abc");
const instantXyz = document.getElementById("instant-xyz");
const instantEFactor = document.getElementById("instant-e-factor");
const instantHint = document.getElementById("instant-hint");

const inputFields = ["A", "B", "C", "X", "Y", "Z", "E_n", "F_n", "steps"];
let currentScenario = null;

function setFormValues(values) {
  inputFields.forEach((key) => {
    const input = document.getElementById(key);
    if (input && values[key] !== undefined) {
      input.value = values[key];
    }
  });
}

function populateScenarios() {
  scenarioSelect.innerHTML = "";
  scenarios.forEach((scenario, index) => {
    const option = document.createElement("option");
    option.value = scenario.id;
    option.textContent = scenario.name;
    if (index === 0) {
      option.selected = true;
    }
    scenarioSelect.appendChild(option);
  });

  if (scenarios.length) {
    setScenario(scenarios[0]);
  }
}

function setScenario(scenario) {
  currentScenario = scenario;
  scenarioDescription.textContent = scenario.description;
  setFormValues(scenario.inputs);
  updateInstantSnapshot();
}

function formatSummary(summaryData) {
  if (!summaryData) {
    return "";
  }

  const growth = summaryData.growth_rate * 100;
  return `Initial: ${summaryData.initial_intelligence.toFixed(4)} · Final: ${summaryData.final_intelligence.toFixed(4)} · Growth: ${growth.toFixed(1)}%`;
}

function updateTable(steps) {
  componentsBody.innerHTML = "";

  if (!steps.length) {
    const row = document.createElement("tr");
    row.innerHTML = '<td colspan="4" class="empty">No data available.</td>';
    componentsBody.appendChild(row);
    return;
  }

  steps.forEach((step) => {
    const components = step.intelligence.components || {};
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${step.step}</td>
      <td>${(components.ABC ?? 0).toFixed(4)}</td>
      <td>${(components.XYZ ?? 0).toFixed(4)}</td>
      <td>${(components.E_factor ?? 0).toFixed(4)}</td>
    `;
    componentsBody.appendChild(row);
  });
}

function parseNumber(value) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function clamp(value, min, max) {
  if (value === null) {
    return null;
  }
  if (max === null) {
    return Math.max(min, value);
  }
  return Math.min(max, Math.max(min, value));
}

function computeInstantSnapshot(inputs) {
  const clamped = {
    A: clamp(inputs.A, 0, 1),
    B: clamp(inputs.B, 0, 1),
    C: clamp(inputs.C, 0, 1),
    X: clamp(inputs.X, 0, 1),
    Y: clamp(inputs.Y, 0, 1),
    Z: clamp(inputs.Z, 0, null),
    E_n: clamp(inputs.E_n, 0, null),
    F_n: clamp(inputs.F_n, -1, null),
  };

  const values = Object.values(clamped);
  if (values.some((value) => value === null)) {
    return null;
  }

  const abc = clamped.A * clamped.B * clamped.C;
  const xyz = clamped.X * clamped.Y * clamped.Z;
  const eFactor = clamped.E_n * (1 + clamped.F_n);
  return {
    score: abc * xyz * eFactor,
    abc,
    xyz,
    eFactor,
  };
}

function updateInstantSnapshot() {
  const inputs = {
    A: parseNumber(document.getElementById("A").value),
    B: parseNumber(document.getElementById("B").value),
    C: parseNumber(document.getElementById("C").value),
    X: parseNumber(document.getElementById("X").value),
    Y: parseNumber(document.getElementById("Y").value),
    Z: parseNumber(document.getElementById("Z").value),
    E_n: parseNumber(document.getElementById("E_n").value),
    F_n: parseNumber(document.getElementById("F_n").value),
  };

  const snapshot = computeInstantSnapshot(inputs);
  if (!snapshot) {
    instantScore.textContent = "--";
    instantAbc.textContent = "--";
    instantXyz.textContent = "--";
    instantEFactor.textContent = "--";
    instantHint.textContent = "Enter valid numeric inputs to compute the instant score.";
    return;
  }

  instantScore.textContent = snapshot.score.toFixed(4);
  instantAbc.textContent = snapshot.abc.toFixed(4);
  instantXyz.textContent = snapshot.xyz.toFixed(4);
  instantEFactor.textContent = snapshot.eFactor.toFixed(4);
  instantHint.textContent = "Clamped to valid ranges to mirror the core axiom defaults.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";
  summary.textContent = "Running simulation...";

  const payload = {};
  inputFields.forEach((key) => {
    const value = document.getElementById(key).value;
    payload[key] = key === "steps" ? Number.parseInt(value, 10) : Number.parseFloat(value);
  });
  payload.preset = currentScenario?.preset || scenarioSelect.value;

  try {
    const result = await runSimulation(payload);
    const history = result.intelligence_history || result.steps.map((step) => step.intelligence.score);
    renderLineChart(chartCanvas, history, result.steps.map((step) => step.step));
    updateTable(result.steps);
    summary.textContent = formatSummary(result.summary);
  } catch (error) {
    summary.textContent = "";
    errorMessage.textContent = error.message || "Simulation failed.";
  }
});

inputFields
  .filter((key) => key !== "steps")
  .forEach((key) => {
    const input = document.getElementById(key);
    if (input) {
      input.addEventListener("input", updateInstantSnapshot);
    }
  });

scenarioSelect.addEventListener("change", (event) => {
  const selected = scenarios.find((scenario) => scenario.id === event.target.value);
  if (selected) {
    setScenario(selected);
  }
});

populateScenarios();
renderLineChart(chartCanvas, []);
updateInstantSnapshot();
