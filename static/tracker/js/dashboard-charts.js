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

    new Chart(chart, {
      type: "doughnut",
      data: {
        labels: [label, "Remaining"],
        datasets: [
          {
            data: [current, daily],
            borderWidth: 0,
            backgroundColor: [backColor, "#5fbba1ff"],
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