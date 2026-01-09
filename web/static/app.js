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

const inputFields = ["A", "B", "C", "X", "Y", "Z", "E_n", "F_n", "steps"];

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
  scenarioDescription.textContent = scenario.description;
  setFormValues(scenario.inputs);
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

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.textContent = "";
  summary.textContent = "Running simulation...";

  const payload = {};
  inputFields.forEach((key) => {
    const value = document.getElementById(key).value;
    payload[key] = key === "steps" ? Number.parseInt(value, 10) : Number.parseFloat(value);
  });

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

scenarioSelect.addEventListener("change", (event) => {
  const selected = scenarios.find((scenario) => scenario.id === event.target.value);
  if (selected) {
    setScenario(selected);
  }
});

populateScenarios();
renderLineChart(chartCanvas, []);
