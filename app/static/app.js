const appointmentList = document.getElementById("appointment-list");
const totalAppointments = document.getElementById("total-appointments");
const lateAppointments = document.getElementById("late-appointments");
const followUpsSent = document.getElementById("follow-ups-sent");
const rescheduledAppointments = document.getElementById("rescheduled-appointments");
const form = document.getElementById("appointment-form");
const formMessage = document.getElementById("form-message");
const refreshButton = document.getElementById("refresh-button");
const referenceTimeInput = document.getElementById("reference-time");
const referenceLabel = document.getElementById("reference-label");

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

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatLocalDateTime(date) {
  const year = date.getFullYear();
  const month = `${date.getMonth() + 1}`.padStart(2, "0");
  const day = `${date.getDate()}`.padStart(2, "0");
  const hours = `${date.getHours()}`.padStart(2, "0");
  const minutes = `${date.getMinutes()}`.padStart(2, "0");
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function currentReferenceTime() {
  return referenceTimeInput.value || formatLocalDateTime(new Date());
}

function timingClass(appointment) {
  if (appointment.is_late) {
    return "status-pill alert";
  }
  if (appointment.status === "follow_up_sent") {
    return "status-pill accent";
  }
  if (appointment.status === "rescheduled") {
    return "status-pill calm";
  }
  return "status-pill";
}

function renderActions(appointment) {
  if (appointment.needs_follow_up) {
    return `
      <div class="appointment-actions">
        <button type="button" data-action="follow-up" data-channel="text" data-appointment-id="${appointment.id}">Trigger MCP text</button>
        <button type="button" data-action="follow-up" data-channel="call" data-appointment-id="${appointment.id}" class="secondary-button">Trigger MCP call</button>
      </div>
    `;
  }

  if (appointment.can_reschedule) {
    return `
      <form class="inline-form" data-action="reschedule" data-appointment-id="${appointment.id}">
        <label>
          New appointment time
          <input type="datetime-local" name="new_scheduled_at" required>
        </label>
        <button type="submit">Confirm reschedule</button>
      </form>
    `;
  }

  return `
    <div class="appointment-actions">
      <span class="status-copy">${escapeHtml(appointment.timing_status)}</span>
    </div>
  `;
}

function renderAppointmentCard(appointment) {
  const card = document.createElement("article");
  card.className = "appointment-card";

  card.innerHTML = `
    <div class="card-topline">
      <div>
        <p class="customer-name">${escapeHtml(appointment.customer_name)}</p>
        <h3>${escapeHtml(appointment.appointment_type)}</h3>
      </div>
      <span class="${timingClass(appointment)}">${escapeHtml(appointment.status_label)}</span>
    </div>
    <p class="contact-line">${escapeHtml(appointment.phone_number)} · prefers ${escapeHtml(appointment.preferred_channel)}</p>
    <div class="appointment-meta">
      <span class="pill">Scheduled: ${escapeHtml(appointment.scheduled_for_label)}</span>
      <span class="pill">${escapeHtml(appointment.timing_status)}</span>
      <span class="pill">Follow-ups: ${escapeHtml(appointment.follow_up_count)}</span>
      <span class="pill">Reschedules: ${escapeHtml(appointment.reschedule_count)}</span>
    </div>
    <p class="activity-note">${escapeHtml(appointment.latest_activity)}</p>
    ${appointment.notes ? `<p class="notes-line">Notes: ${escapeHtml(appointment.notes)}</p>` : ""}
    ${renderActions(appointment)}
  `;

  card.querySelectorAll("button[data-action='follow-up']").forEach((button) => {
    button.addEventListener("click", async () => {
      try {
        await request(`/api/appointments/${appointment.id}/follow-up`, {
          method: "POST",
          body: JSON.stringify({
            channel: button.dataset.channel,
            reference_time: currentReferenceTime(),
          }),
        });
        formMessage.textContent = `MCP ${button.dataset.channel} follow-up sent to ${appointment.customer_name}.`;
        await loadDashboard();
      } catch (error) {
        formMessage.textContent = error.message;
      }
    });
  });

  const rescheduleForm = card.querySelector("form[data-action='reschedule']");
  if (rescheduleForm) {
    rescheduleForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const newScheduledAt = rescheduleForm.new_scheduled_at.value;

      try {
        await request(`/api/appointments/${appointment.id}/reschedule`, {
          method: "POST",
          body: JSON.stringify({
            new_scheduled_at: newScheduledAt,
            reference_time: currentReferenceTime(),
          }),
        });
        formMessage.textContent = `${appointment.customer_name} has been rescheduled.`;
        await loadDashboard();
      } catch (error) {
        formMessage.textContent = error.message;
      }
    });
  }

  return card;
}

async function loadDashboard() {
  const referenceTime = currentReferenceTime();
  const dashboard = await request(`/api/dashboard?time=${encodeURIComponent(referenceTime)}`);
  totalAppointments.textContent = dashboard.total_appointments;
  lateAppointments.textContent = dashboard.late_appointments;
  followUpsSent.textContent = dashboard.follow_ups_sent;
  rescheduledAppointments.textContent = dashboard.rescheduled_appointments;
  referenceLabel.textContent = `Simulation clock: ${dashboard.reference_time_label}`;

  appointmentList.innerHTML = "";

  if (!dashboard.appointments.length) {
    appointmentList.innerHTML = `<p class="empty-state">No appointments yet. Add one to start tracking late arrivals.</p>`;
    return;
  }

  dashboard.appointments.forEach((appointment) => {
    appointmentList.appendChild(renderAppointmentCard(appointment));
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formMessage.textContent = "";

  const payload = {
    customer_name: form.customer_name.value,
    phone_number: form.phone_number.value,
    appointment_type: form.appointment_type.value,
    scheduled_at: form.scheduled_at.value,
    preferred_channel: form.preferred_channel.value,
    notes: form.notes.value,
  };

  try {
    await request("/api/appointments", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    form.reset();
    formMessage.textContent = "Appointment created.";
    await loadDashboard();
  } catch (error) {
    formMessage.textContent = error.message;
  }
});

refreshButton.addEventListener("click", loadDashboard);
referenceTimeInput.addEventListener("change", loadDashboard);

if (!referenceTimeInput.value) {
  referenceTimeInput.value = formatLocalDateTime(new Date());
}

loadDashboard().catch((error) => {
  formMessage.textContent = error.message;
});
