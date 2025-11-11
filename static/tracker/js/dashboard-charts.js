document.addEventListener("DOMContentLoaded", function () {
  const data = window.dashboardData || {};

  const {
    totalCalories,
    calorieGoal,
    caloriePercent,

    totalProtein,
    proteinGoal,
    proteinPercent,

    totalCarbs,
    carbsGoal,
    carbsPercent,

    totalFats,
    fatsGoal,
    fatsPercent,

    caloriesBackColor,
    proteinBackColor,
    carbsBackColor,
    fatsBackColor,
  } = data;

  function makeDonutChart(id, current, goal, label, backColor) {
    const chart = document.getElementById(id);
    if (!chart) return;

    let daily = goal - current
    if (goal - current < 0) {
      daily = 0
    }

    let secColor = "#1B8C7B"
    if (backColor == "#B7B7B7") {
      secColor = "#B7B7B7"
    }

    new Chart(chart, {
      type: "doughnut",
      data: {
        labels: [label, "Remaining"],
        datasets: [
          {
            data: [current, daily],
            borderWidth: 0,
            backgroundColor: [backColor, secColor],
          },
        ],
      },
      options: {
        responsive: true,
        cutout: "80%",
        plugins: {
          legend: { display: false },
        },
      },
    });
  }

  makeDonutChart("calorieChart", totalCalories, calorieGoal, "Calories", caloriesBackColor);
  makeDonutChart("proteinChart", totalProtein, proteinGoal, "Protein", proteinBackColor);
  makeDonutChart("carbsChart", totalCarbs, carbsGoal, "Carbs", carbsBackColor);
  makeDonutChart("fatsChart", totalFats, fatsGoal, "Fats", fatsBackColor);
});