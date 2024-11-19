document.addEventListener("DOMContentLoaded", function () {
  const crearReservaForm = document.getElementById("crear-reserva-form");
  const reservaIdInput = document.getElementById("reserva-id");
  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  // Función para editar una reserva
  const editarReservaBtns = document.querySelectorAll(".editar-reserva-btn");
  editarReservaBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      const reservaId = this.getAttribute("data-id");
      const momentoInicio = this.getAttribute("data-momento_inicio");
      const momentoFin = this.getAttribute("data-momento_fin");
      const espacio = this.getAttribute("data-espacio");

      // Rellenamos el formulario con los datos de la reserva a editar
      document.getElementById("momento_inicio").value = momentoInicio;
      document.getElementById("momento_fin").value = momentoFin;
      document.getElementById("espacio").value = espacio;
      reservaIdInput.value = reservaId;  // Colocamos el ID en el campo oculto
    });
  });

  // Función para crear o editar una reserva
  crearReservaForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(crearReservaForm);
    const reservaData = {
      momento_inicio: formData.get("momento_inicio"),
      momento_fin: formData.get("momento_fin"),
      espacio: formData.get("espacio"),
    };

    const reservaId = formData.get("reserva-id");

    const url = reservaId ? `/reservas/modificar/${reservaId}/` : "/reservas/crear/";

    fetch(url, {
      method: reservaId ? "PUT" : "POST",  // Usamos PUT para actualizar
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(reservaData),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Error al guardar la reserva");
        }
        return response.json();
      })
      .then(data => {
        if (data.error) {
          alert(data.error);
          return;
        }
        alert(reservaId ? "Reserva actualizada con éxito!" : "Reserva creada con éxito!");
        location.reload(); // Recargar la página para actualizar la lista
      })
      .catch(error => console.error("Error:", error));
  });
  // Función para eliminar una reservai
  const eliminarReservaBtns = document.querySelectorAll(".eliminar-reserva-btn");
  // eliminar reserva
  eliminarReservaBtns.forEach(btn => {
    btn.addEventListener("click", function () {
      // no dataset
      const reservaId = btn.getAttribute("data-id");

      fetch(`/reservas/eliminar/${reservaId}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Error al eliminar la reserva");
          }
          return response.json();
        })
        .then(data => {
          alert("Reserva eliminada con éxito!");
          location.reload(); // Recargar la página para actualizar la lista
        })
        .catch(error => console.error("Error al eliminar reserva:", error));
    });
  });
});


