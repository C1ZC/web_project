document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const orderSelect = document.getElementById('order-select');
    const viewBtns = document.querySelectorAll('.view-btn');
    
    // Función para obtener los parámetros actuales de la URL
    function getCurrentParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            search: params.get('search') || '',
            order_by: params.get('order_by') || 'pokemon_id',
            view_type: params.get('view_type') || 'cards',
            page: params.get('page') || '1'
        };
    }

    // Función para actualizar la URL manteniendo la página actual
    function updateURL(newParams) {
        const currentParams = getCurrentParams();
        const url = new URL(window.location.href);
        
        // Si estamos cambiando la búsqueda o el orden, volver a página 1
        if (newParams.search !== currentParams.search || 
            newParams.order_by !== currentParams.order_by) {
            url.searchParams.set('page', '1');
        } else {
            // Mantener la página actual
            url.searchParams.set('page', currentParams.page);
        }

        // Actualizar resto de parámetros
        if (newParams.search) url.searchParams.set('search', newParams.search);
        if (newParams.order_by) url.searchParams.set('order_by', newParams.order_by);
        if (newParams.view_type) url.searchParams.set('view_type', newParams.view_type);

        window.location.href = url.toString();
    }

    // Búsqueda con debounce
    let searchTimeout;
    searchInput?.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            updateURL({
                search: this.value,
                order_by: orderSelect.value,
                view_type: document.querySelector('.view-btn.active')?.dataset.view
            });
        }, 500);
    });

    // Búsqueda con botón
    searchBtn?.addEventListener('click', function() {
        updateURL({
            search: searchInput.value,
            order_by: orderSelect.value,
            view_type: document.querySelector('.view-btn.active')?.dataset.view
        });
    });

    // Ordenamiento
    orderSelect?.addEventListener('change', function() {
        updateURL({
            search: searchInput?.value || '',
            order_by: this.value,
            view_type: document.querySelector('.view-btn.active')?.dataset.view
        });
    });

    // Cambio de vista
    viewBtns.forEach(btn => {
        btn?.addEventListener('click', function() {
            viewBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updateURL({
                search: searchInput?.value || '',
                order_by: orderSelect?.value,
                view_type: this.dataset.view
            });
        });
    });

    // Permitir búsqueda con Enter
    searchInput?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            updateURL({
                search: this.value,
                order_by: orderSelect?.value,
                view_type: document.querySelector('.view-btn.active')?.dataset.view
            });
        }
    });
});