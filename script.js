let chart;

async function generateIdea() {

    const problem = document.getElementById("problemInput").value;
    const loader = document.getElementById("loader");

    loader.classList.remove("hidden");

    const res = await fetch("/generate-idea", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({problem})
    });

    const data = await res.json();

    loader.classList.add("hidden");
    document.getElementById("resultBox").classList.remove("hidden");

    document.getElementById("startupName").innerText = data.ideaName;
    document.getElementById("idea").innerText = data.solution;
    document.getElementById("audience").innerText = data.targetAudience;
    document.getElementById("strategy").innerText = data.marketingStrategy;
    document.getElementById("revenue").innerText = data.revenueModel;
    document.getElementById("funding").innerText = data.budget;
    document.getElementById("market").innerText = data.marketTrends;
    document.getElementById("pitch").innerText = data.USP;

    const ctx = document.getElementById("chart");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(data.profitLoss),
            datasets: [{
                label: "Profit/Loss",
                data: Object.values(data.profitLoss)
            }]
        }
    });
}