document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  const searchBtn = document.getElementById("search-btn");
  const orderSelect = document.getElementById("order-select");
  const viewBtns = document.querySelectorAll(".view-btn");

  function getCurrentParams() {
    const params = new URLSearchParams(window.location.search);
    return {
      search: params.get("search") || "",
      order_by: params.get("order_by") || "pokemon_id",
      view_type: params.get("view_type") || "cards",
      page: params.get("page") || "1",
    };
  }

  function updateURL(newParams = {}) {
    const currentParams = getCurrentParams();
    const url = new URL(window.location.href);

    // Si hay cambio en búsqueda u orden, resetear página a 1
    if (newParams.search !== undefined || newParams.order_by !== undefined) {
      url.searchParams.set("page", "1");
    } else {
      url.searchParams.set("page", newParams.page || currentParams.page);
    }

    // Actualizar parámetros
    url.searchParams.set(
      "search",
      newParams.search !== undefined ? newParams.search : currentParams.search
    );
    url.searchParams.set(
      "order_by",
      newParams.order_by || currentParams.order_by
    );
    url.searchParams.set(
      "view_type",
      newParams.view_type || currentParams.view_type
    );

    window.location.href = url.toString();
  }

  const MIN_SEARCH_LENGTH = 3;
  const DEBOUNCE_TIME = 800; // Aumentamos el tiempo de espera
  let searchTimeout;
  let lastValidSearch = "";

  function isValidSearch(search) {
    const search_clean = search.trim();
    // Validar longitud y caracteres permitidos (letras, números y espacios)
    return (
      search_clean === "" ||
      (search_clean.length >= MIN_SEARCH_LENGTH &&
        /^[a-zA-Z0-9\s]*$/.test(search_clean))
    );
  }

  // Búsqueda con debounce mejorada
  searchInput?.addEventListener("input", function () {
    clearTimeout(searchTimeout);
    const searchValue = this.value.trim();

    // Validar el input mientras el usuario escribe
    if (!isValidSearch(searchValue)) {
      this.classList.add("is-invalid");
      setTimeout(() => this.classList.remove("is-invalid"), 820);
      return;
    }

    // Solo actualizar lastValidSearch si es válido
    if (isValidSearch(searchValue)) {
      lastValidSearch = searchValue;
      this.classList.remove("is-invalid");
    }

    // Solo hacer la búsqueda si:
    // 1. El campo está vacío (para mostrar todos)
    // 2. La búsqueda tiene la longitud mínima Y es diferente a la búsqueda anterior
    searchTimeout = setTimeout(() => {
      if (
        searchValue === "" ||
        (searchValue.length >= MIN_SEARCH_LENGTH &&
          searchValue !== lastValidSearch)
      ) {
        updateURL({ search: searchValue });
      }
    }, DEBOUNCE_TIME);
  });

  // Mejorar el manejo de teclas
  searchInput?.addEventListener("keyup", function (e) {
    const searchValue = this.value.trim();

    // Si presiona Escape, limpiar la búsqueda
    if (e.key === "Escape") {
      this.value = "";
      updateURL({ search: "" });
      lastValidSearch = "";
      return;
    }

    // Solo actualizar en backspace/delete si el campo queda vacío
    if ((e.key === "Backspace" || e.key === "Delete") && searchValue === "") {
      clearTimeout(searchTimeout);
      updateURL({ search: "" });
      lastValidSearch = "";
    }
  });

  // Mejorar búsqueda con Enter
  searchInput?.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      const searchValue = this.value.trim();

      if (!isValidSearch(searchValue)) {
        this.classList.add("is-invalid");
        setTimeout(() => this.classList.remove("is-invalid"), 820);
        return;
      }

      if (searchValue === "" || searchValue.length >= MIN_SEARCH_LENGTH) {
        updateURL({
          search: searchValue,
          order_by: orderSelect?.value,
          view_type: document.querySelector(".view-btn.active")?.dataset.view,
        });
      }
    }
  });

  // Mejorar click en botón de búsqueda
  searchBtn?.addEventListener("click", function () {
    const searchValue = searchInput.value.trim();

    if (!isValidSearch(searchValue)) {
      searchInput.classList.add("is-invalid");
      setTimeout(() => searchInput.classList.remove("is-invalid"), 820);
      return;
    }

    if (searchValue === "" || searchValue.length >= MIN_SEARCH_LENGTH) {
      updateURL({
        search: searchValue,
        order_by: orderSelect?.value,
        view_type: document.querySelector(".view-btn.active")?.dataset.view,
      });
    }
  });

  // Ordenamiento
  orderSelect?.addEventListener("change", function () {
    updateURL({
      search: searchInput?.value || "",
      order_by: this.value,
      view_type: document.querySelector(".view-btn.active")?.dataset.view,
    });
  });

  // Cambio de vista
  viewBtns.forEach((btn) => {
    btn?.addEventListener("click", function () {
      viewBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      updateURL({
        search: searchInput?.value || "",
        order_by: orderSelect?.value,
        view_type: this.dataset.view,
      });
    });
  });
});

// Hacer updateURL disponible globalmente para la paginación
window.updateURL = function (params) {
  const currentParams = new URLSearchParams(window.location.search);
  const url = new URL(window.location.href);

  // Mantener parámetros existentes
  for (let [key, value] of currentParams.entries()) {
    if (!params.hasOwnProperty(key)) {
      url.searchParams.set(key, value);
    }
  }

  // Actualizar con nuevos parámetros
  for (let [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }

  window.location.href = url.toString();
};
