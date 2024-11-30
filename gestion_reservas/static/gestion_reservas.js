document.addEventListener('DOMContentLoaded', () => {
  const momentoInicioInput = document.getElementById('momento_inicio');
  const momentoFinInput = document.getElementById('momento_fin');
  const reservaForm = document.getElementById('crear-reserva-form');
  const reservaIdInput = document.getElementById('reserva-id');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const displayInicio = document.getElementById('display_inicio');
  const displayFin = document.getElementById('display_fin');

  // Función para formatear la fecha al formato 'DD/MM/YYYY, HH:mm'
  const formatearFechaDisplay = (date) => {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${day}/${month}/${year}, ${hours}:${minutes}`;
  };

  // Función para actualizar el campo de fin a una hora después del inicio
  const actualizarMomentoFin = () => {
      const inicioValue = momentoInicioInput.value;
      if (inicioValue) {
          const inicioDate = new Date(inicioValue);
          if (isNaN(inicioDate.getTime())) {
              // Fecha inválida
              momentoFinInput.value = '';
              displayFin.innerText = '';
              return;
          }
          const finDate = new Date(inicioDate.getTime() + 60 * 60 * 1000); // Añade 1 hora

          // Formatea la fecha al formato 'YYYY-MM-DDTHH:MM' para datetime-local
          const year = finDate.getFullYear();
          const month = String(finDate.getMonth() + 1).padStart(2, '0');
          const day = String(finDate.getDate()).padStart(2, '0');
          const hours = String(finDate.getHours()).padStart(2, '0');
          const minutes = String(finDate.getMinutes()).padStart(2, '0');

          const finFormatted = `${year}-${month}-${day}T${hours}:${minutes}`;
          momentoFinInput.value = finFormatted;

          // Actualizar la visualización formateada
          displayFin.innerText = formatearFechaDisplay(finDate);

          // Actualizar la visualización de inicio
          displayInicio.innerText = formatearFechaDisplay(inicioDate);
      } else {
          momentoFinInput.value = '';
          displayInicio.innerText = '';
          displayFin.innerText = '';
      }
  };

  // Escuchar cambios en el campo de inicio
  momentoInicioInput.addEventListener('change', actualizarMomentoFin);

  // Manejar la edición de reservas
  const editarReservaButtons = document.querySelectorAll('.editar-reserva-btn');
  editarReservaButtons.forEach(button => {
      button.addEventListener('click', () => {
          const reservaId = button.getAttribute('data-id');
          const inicio = button.getAttribute('data-momento_inicio');
          const fin = button.getAttribute('data-momento_fin');
          const espacio = button.getAttribute('data-espacio');

          reservaIdInput.value = reservaId;
          momentoInicioInput.value = inicio;
          momentoFinInput.value = fin;
          document.getElementById('espacio').value = espacio;

          const inicioDate = new Date(inicio);
          const finDate = new Date(fin);

          // Actualizar la visualización formateada
          displayInicio.innerText = formatearFechaDisplay(inicioDate);
          displayFin.innerText = formatearFechaDisplay(finDate);

          // Actualizar el campo de fin automáticamente
          actualizarMomentoFin();
      });
  });

  // Manejar el envío del formulario
  reservaForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const reservaId = reservaIdInput.value;
      const url = reservaId ? `/reservas/modificar/${reservaId}/` : '/reservas/crear/';
      const method = reservaId ? 'PUT' : 'POST'; // Asegúrate de que tus vistas manejan estos métodos

      const espacio = document.getElementById('espacio').value;
      const momento_inicio = momentoInicioInput.value;
      const momento_fin = momentoFinInput.value;

      fetch(url, {
          method: method,
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({
              espacio: espacio,
              momento_inicio: momento_inicio,
              momento_fin: momento_fin,
          }),
      })
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              alert(data.error);
              return;
          }
          if (reservaId) {
              alert("Reserva actualizada con éxito!");
          } else {
              alert("Reserva creada con éxito!");
          }
          window.location.reload(); // Recargar la página para actualizar la lista
      })
      .catch(error => {
          console.error('Error:', error);
          alert("Ocurrió un error al procesar la solicitud.");
      });
  });

  // Manejar la eliminación de reservas
  const eliminarReservaButtons = document.querySelectorAll('.eliminar-reserva-btn');
  eliminarReservaButtons.forEach(button => {
      button.addEventListener('click', () => {
          const reservaId = button.getAttribute('data-id');
          if (confirm('¿Estás seguro de que deseas eliminar esta reserva?')) {
              fetch(`/reservas/eliminar/${reservaId}/`, {
                  method: 'DELETE',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken,
                  },
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      alert("Reserva eliminada con éxito!");
                      window.location.reload(); // Recargar la página para actualizar la lista
                  } else {
                      alert('Error al eliminar la reserva.');
                  }
              })
              .catch(error => {
                  console.error('Error al eliminar reserva:', error);
                  alert("Ocurrió un error al eliminar la reserva.");
              });
          }
      });
  });

  // Funcionalidad de desplazamiento horizontal
  const reservasContainer = document.getElementById('reservas-container');
  const scrollLeftBtn = document.getElementById('scroll-left');
  const scrollRightBtn = document.getElementById('scroll-right');

  // Definir la cantidad de desplazamiento (en píxeles)
  const scrollAmount = 300;

  scrollLeftBtn.addEventListener('click', () => {
      reservasContainer.scrollBy({
          top: 0,
          left: -scrollAmount,
          behavior: 'smooth'
      });
  });

  scrollRightBtn.addEventListener('click', () => {
      reservasContainer.scrollBy({
          top: 0,
          left: scrollAmount,
          behavior: 'smooth'
      });
  });

  // Opcional: Mostrar/ocultar botones según el scroll
  const toggleScrollButtons = () => {
      // Mostrar botón izquierdo si no está al inicio
      if (reservasContainer.scrollLeft > 0) {
          scrollLeftBtn.classList.remove('hidden');
      } else {
          scrollLeftBtn.classList.add('hidden');
      }

      // Mostrar botón derecho si no está al final
      if (reservasContainer.scrollLeft + reservasContainer.clientWidth < reservasContainer.scrollWidth) {
          scrollRightBtn.classList.remove('hidden');
      } else {
          scrollRightBtn.classList.add('hidden');
      }
  };

  // Inicializar la visibilidad de los botones
  toggleScrollButtons();

  // Escuchar eventos de scroll para actualizar la visibilidad de los botones
  reservasContainer.addEventListener('scroll', toggleScrollButtons);
  window.addEventListener('resize', toggleScrollButtons);
});