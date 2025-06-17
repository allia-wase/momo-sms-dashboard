document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/transactions")
    .then(res => res.json())
    .then(data => {
      renderChart(data);
      renderTable(data);
    });
});

function renderChart(data) {
  const counts = {};
  data.forEach(tx => counts[tx.type] = (counts[tx.type] || 0) + 1);

  new Chart(document.getElementById('transactionChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(counts),
      datasets: [{
        label: 'Transaction Count',
        data: Object.values(counts),
        backgroundColor: 'rgba(54, 162, 235, 0.6)'
      }]
    }
  });
}

function renderTable(data) {
  const tbody = document.querySelector("#transactionTable tbody");
  data.forEach(tx => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${tx.type}</td><td>${tx.amount}</td><td>${tx.date}</td>`;
    tbody.appendChild(row);
  });
}
