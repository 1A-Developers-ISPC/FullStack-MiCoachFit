// Elementos del DOM
const monthAndYear = document.getElementById("monthAndYear");
const calendarDays = document.getElementById("calendarDays");
const fechaInput = document.getElementById("fecha");
const sessionForm = document.getElementById("sessionForm");

// Fecha actual
let currentDate = new Date();

const monthNames = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

const dayNames = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];

// ------------------------
// Datos de disponibilidad de ejemplo
// amarillo = cupos disponibles, azul = cupos llenos
const availabilityData = {
    5: "available",
    10: "full",
    15: "available"
};

// ------------------------
// Función para renderizar el calendario
function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    monthAndYear.textContent = `${monthNames[month]} ${year}`;
    calendarDays.innerHTML = "";

    // Encabezados de los días de la semana
    dayNames.forEach(d => {
        const dayHeader = document.createElement("div");
        dayHeader.classList.add("day-name");
        dayHeader.textContent = d;
        calendarDays.appendChild(dayHeader);
    });

    // Primer día del mes
    const firstDay = new Date(year, month, 1).getDay();
    const start = (firstDay === 0 ? 7 : firstDay) - 1; // lunes primero
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Rellenar espacios vacíos al inicio
    for (let i = 0; i < start; i++) {
        const empty = document.createElement("div");
        calendarDays.appendChild(empty);
    }

    // Crear días del mes
    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("calendar-day");
        dayDiv.textContent = day;

        // Destacar el día actual
        const today = new Date();
        if (
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            dayDiv.classList.add("today");
        }

        // ------------------------
        // Indicador de disponibilidad
        if (availabilityData[day]) {
            const circle = document.createElement("span");
            circle.classList.add("availability", availabilityData[day]);
            dayDiv.appendChild(circle);
        }

        // Seleccionar día al hacer clic
        dayDiv.addEventListener("click", () => {
            fechaInput.value = `${day} ${monthNames[month]} ${year}`;
        });

        calendarDays.appendChild(dayDiv);
    }
}

// ------------------------
// Navegación de meses
document.getElementById("prevMonth").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
});

document.getElementById("nextMonth").addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
});

// ------------------------
// Render inicial
renderCalendar(currentDate);

// ------------------------
// Manejo del formulario de sesión
if (sessionForm) {
    sessionForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Sesión guardada correctamente ✅");
        sessionForm.reset();
    });
}


// Mensaje Bienvenida

const params = new URLSearchParams(location.search);
const u = params.get('user');
if (u) document.getElementById('welcome').textContent = `Bienvenido, ${decodeURIComponent(u)}`;