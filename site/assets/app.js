(function () {
  "use strict";
  var raw = document.getElementById("demo-data");
  var data;
  try {
    data = JSON.parse(raw.textContent);
  } catch (e) {
    showError("The bundled demonstration data could not be read.");
    return;
  }
  if (
    !data ||
    !data.summary ||
    !Array.isArray(data.results) ||
    data.provenance !== "deterministic_fixture"
  ) {
    showError(
      "The demonstration data is missing or has an unexpected provenance.",
    );
    return;
  }
  var results = data.results;
  var activeFilter = "all";
  var query = "";
  var selected = null;
  function $(id) {
    return document.getElementById(id);
  }
  function showError(message) {
    var el = document.getElementById("case-list");
    if (el) el.textContent = message;
  }
  function pct(value) {
    return (Number(value) * 100).toFixed(1) + "%";
  }
  function appendText(parent, tag, text, className) {
    var el = document.createElement(tag);
    el.textContent = String(text);
    if (className) el.className = className;
    parent.appendChild(el);
    return el;
  }
  function exact(row) {
    return !!row.exact_match;
  }
  function isVisible(row) {
    if (activeFilter === "failure" && exact(row)) return false;
    if (activeFilter === "pass" && !exact(row)) return false;
    var hay = (row.id + " " + row.category).toLowerCase();
    return hay.indexOf(query) !== -1;
  }
  function paintMetric(name, number) {
    var t = $("metric-" + name),
      bar = $("bar-" + name);
    if (t) t.textContent = pct(number);
    if (bar) bar.style.width = Math.max(0, Math.min(100, number * 100)) + "%";
  }
  paintMetric("parse", data.summary.parse_success_rate);
  paintMetric("schema", data.summary.schema_compliance_rate);
  paintMetric("fields", data.summary.field_accuracy);
  paintMetric("exact", data.summary.case_exact_match_rate);
  $("count-all").textContent = String(results.length);
  $("count-fail").textContent = String(
    results.filter(function (r) {
      return !exact(r);
    }).length,
  );
  function renderList() {
    var body = $("case-list");
    body.replaceChildren();
    var visible = results.filter(isVisible);
    $("visible-count").textContent =
      visible.length + " / " + results.length + " cases";
    const current = visible.find((row) => row.id === selected) || visible[0];
    selected = current ? current.id : null;
    $("case-detail").hidden = !current;
    if (current) renderDetail(current);
    if (!current) {
      const cell = body.insertRow().insertCell();
      cell.colSpan = 3;
      cell.textContent = "No cases match these filters.";
      return;
    }
    visible.forEach(function (r) {
      var tr = document.createElement("tr");
      tr.dataset.id = r.id;
      if (r.id === selected) tr.className = "selected";
      const first = tr.insertCell();
      const button = appendText(first, "button", r.id, "case-id");
      button.type = "button";
      button.setAttribute(
        "aria-label",
        "Inspect " + r.id + " " + r.category.replace(/_/g, " "),
      );
      button.setAttribute("aria-controls", "case-detail");
      button.setAttribute("aria-pressed", String(r.id === selected));
      appendText(first, "span", r.category.replace(/_/g, " "), "case-category");
      appendText(tr, "td", pct(r.field_accuracy), "table-right");
      var last = document.createElement("td");
      appendText(
        last,
        "span",
        exact(r) ? "PASS" : "FAIL",
        "tag" + (exact(r) ? "" : " fail"),
      );
      tr.appendChild(last);
      tr.addEventListener("click", function () {
        selected = r.id;
        for (const row of body.rows) {
          const active = row.dataset.id === selected;
          row.classList.toggle("selected", active);
          row
            .querySelector("button")
            .setAttribute("aria-pressed", String(active));
        }
        renderDetail(r);
      });
      body.appendChild(tr);
    });
  }
  function renderDetail(r) {
    $("detail-id").textContent = r.id;
    $("detail-description").textContent =
      "Fixture category: " +
      r.category.replace(/_/g, " ") +
      ". This is seeded test output, not an observed model response.";
    $("detail-parse").textContent = r.parse_success ? "PASS" : "FAIL";
    $("detail-schema").textContent = r.schema_valid ? "PASS" : "FAIL";
    $("detail-accuracy").textContent = pct(r.field_accuracy);
    var status = $("detail-status");
    status.textContent = exact(r) ? "ALL FIELDS MATCH" : "RECORDED FAILURE";
    status.className = "tag" + (exact(r) ? "" : " fail");
    var content = $("detail-evidence");
    content.replaceChildren();
    var errors = r.errors || [],
      mismatches = r.mismatches || [];
    if (!errors.length && !mismatches.length) {
      appendText(
        content,
        "p",
        "No errors or field mismatches in this seeded fixture output.",
        "empty-diagnostic",
      );
      return;
    }
    errors.forEach(function (error) {
      appendText(content, "p", "Parse/schema error: " + error, "evidence-line");
    });
    mismatches.forEach(function (item) {
      var p = document.createElement("p");
      p.className = "evidence-line";
      appendText(p, "strong", item.name + ": ");
      p.appendChild(
        document.createTextNode(
          "expected " +
            JSON.stringify(item.expected) +
            ", recorded " +
            JSON.stringify(item.actual) +
            ".",
        ),
      );
      if (item.evidence !== null && item.evidence !== undefined) {
        appendText(p, "span", " Evidence: " + String(item.evidence));
      }
      content.appendChild(p);
    });
  }
  Array.prototype.forEach.call(
    document.querySelectorAll("[data-filter]"),
    function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.dataset.filter;
        Array.prototype.forEach.call(
          document.querySelectorAll("[data-filter]"),
          function (other) {
            var yes = other === button;
            other.classList.toggle("active", yes);
            other.setAttribute("aria-pressed", String(yes));
          },
        );
        renderList();
      });
    },
  );
  $("case-search").addEventListener("input", function (e) {
    query = e.target.value.trim().toLowerCase();
    renderList();
  });
  const initial = results.find((r) => !exact(r)) || results[0];
  selected = initial ? initial.id : null;
  renderList();
})();
