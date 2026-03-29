const habitList = document.getElementById("habit-list");
const totalHabits = document.getElementById("total-habits");
const completedNow = document.getElementById("completed-now");
const bestStreak = document.getElementById("best-streak");
const form = document.getElementById("habit-form");
const formMessage = document.getElementById("form-message");
const refreshButton = document.getElementById("refresh-button");

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Something went wrong.");
  }
  return data;
}

function renderHabitCard(habit) {
  const card = document.createElement("article");
  card.className = "habit-card";

  const details = habit.description
    ? `<p>${habit.description}</p>`
    : `<p>No description yet. Keep it tiny and sustainable.</p>`;

  card.innerHTML = `
    <div>
      <h3>${habit.name}</h3>
      ${details}
    </div>
    <div class="habit-meta">
      <span class="pill">${habit.frequency}</span>
      <span class="pill">Current streak: ${habit.current_streak}</span>
      <span class="pill">Current period: ${habit.current_period_label}</span>
    </div>
    <div class="habit-actions">
      <span>${habit.is_complete_now ? "Marked complete" : "Still open for this period"}</span>
      <button type="button" data-habit-id="${habit.id}">
        ${habit.is_complete_now ? "Completed" : "Complete now"}
      </button>
    </div>
  `;

  const button = card.querySelector("button");
  button.disabled = habit.is_complete_now;
  button.addEventListener("click", async () => {
    await request(`/api/habits/${habit.id}/complete`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    await loadDashboard();
  });

  return card;
}

async function loadDashboard() {
  const dashboard = await request("/api/dashboard");
  totalHabits.textContent = dashboard.total_habits;
  completedNow.textContent = dashboard.completed_for_current_period;
  bestStreak.textContent = dashboard.best_streak;

  habitList.innerHTML = "";

  if (!dashboard.habits.length) {
    habitList.innerHTML = `<p class="empty-state">No habits yet. Add one to get started.</p>`;
    return;
  }

  dashboard.habits.forEach((habit) => {
    habitList.appendChild(renderHabitCard(habit));
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.textContent = "";

  const payload = {
    name: form.name.value,
    description: form.description.value,
    frequency: form.frequency.value,
  };

  try {
    await request("/api/habits", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    form.reset();
    formMessage.textContent = "Habit created.";
    await loadDashboard();
  } catch (error) {
    formMessage.textContent = error.message;
  }
});

refreshButton.addEventListener("click", loadDashboard);

loadDashboard().catch((error) => {
  formMessage.textContent = error.message;
});
