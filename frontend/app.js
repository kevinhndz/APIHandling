(() => {
  const TOKEN_KEY = 'almacen_token';
  const USER_KEY = 'almacen_user';
  const API_KEY = 'almacen_api_base';
  const $ = (selector) => document.querySelector(selector);
  const apiBase = () => (localStorage.getItem(API_KEY) || 'http://127.0.0.1:8000').replace(/\/+$/, '');
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  function tokenClaims(token) {
    try {
      const encoded = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(decodeURIComponent(Array.from(atob(encoded), (char) => `%${char.charCodeAt(0).toString(16).padStart(2, '0')}`).join('')));
    } catch (_) { return {}; }
  }

  async function request(path, options = {}) {
    const headers = new Headers(options.headers || {});
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) headers.set('token', token);
    if (options.body) headers.set('Content-Type', 'application/json');
    let response;
    try { response = await fetch(`${apiBase()}${path}`, {...options, headers}); }
    catch (_) { throw new Error('No se pudo conectar con la API. Revisa que el servidor esté activo.'); }
    if (response.status === 401 || response.status === 403) {
      if (response.status === 401 && path !== '/login/') {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        window.location.replace('/');
      }
      let message = 'Tu cuenta no tiene permisos para esta operación.';
      try { message = (await response.json()).detail || message; } catch (_) {}
      throw new Error(message);
    }
    if (!response.ok) {
      let message = `Error ${response.status}`;
      try { message = (await response.json()).detail || message; } catch (_) {}
      throw new Error(message);
    }
    if (response.status === 204) return null;
    return response.json();
  }

  const loginForm = $('#login-form');
  if (loginForm) {
    const apiInput = $('#api-base');
    const message = $('#login-message');
    const submit = loginForm.querySelector('button[type="submit"]');
    const storedApi = localStorage.getItem(API_KEY);
    if (storedApi) apiInput.value = storedApi;
    if (localStorage.getItem(TOKEN_KEY)) { window.location.replace('/dashboard.html'); return; }
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const values = new FormData(loginForm);
      submit.disabled = true;
      submit.querySelector('span').textContent = 'Verificando…';
      message.textContent = '';
      localStorage.setItem(API_KEY, (apiInput.value.trim() || 'http://127.0.0.1:8000').replace(/\/+$/, ''));
      try {
        const result = await request('/login/', {method:'POST', body:JSON.stringify({user:values.get('user'), password:values.get('password')})});
        if (!result.token) throw new Error('La respuesta del servidor no incluyó un token.');
        localStorage.setItem(TOKEN_KEY, result.token);
        localStorage.setItem(USER_KEY, JSON.stringify({...result, rol:tokenClaims(result.token).rol}));
        window.location.assign('/dashboard.html');
      } catch (error) { message.textContent = error.message; }
      finally { submit.disabled = false; submit.querySelector('span').textContent = 'Entrar al panel'; }
    });
    return;
  }

  const dashboard = $('#dashboard');
  if (!dashboard) return;
  let user;
  try { user = JSON.parse(localStorage.getItem(USER_KEY) || 'null'); }
  catch (_) { user = null; }
  if (!localStorage.getItem(TOKEN_KEY) || !user) { window.location.replace('/'); return; }
  user.rol = user.rol || tokenClaims(localStorage.getItem(TOKEN_KEY)).rol;
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  $('#denied-logout').addEventListener('click', () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.assign('/');
  });
  if (user.rol !== 'Admin') {
    $('#access-denied').hidden = false;
    $('#dashboard-content').hidden = true;
    $('#access-user').textContent = user.user || 'Usuario';
    return;
  }

  let moduleName = 'products';
  let offset = 0;
  let limit = 10;
  let totalPages = 1;
  let currentRows = [];
  const endpoint = () => moduleName === 'products' ? '/products/' : '/clients/';
  const notice = $('#notice');
  const modal = $('#record-modal');
  const modalForm = $('#record-form');

  $('#current-user').textContent = user.user || 'Usuario';
  $('#current-role').textContent = user.rol || 'Sesión activa';
  $('#user-avatar').textContent = (user.user || 'U').slice(0, 1).toUpperCase();

  function showNotice(text, kind = 'error') {
    notice.textContent = text;
    notice.className = `notice ${kind}`;
    notice.hidden = false;
    window.clearTimeout(showNotice.timer);
    showNotice.timer = window.setTimeout(() => { notice.hidden = true; }, 6000);
  }

  function renderProducts(rows) {
    $('#table-head').innerHTML = '<tr><th>ID</th><th>Producto</th><th>Código</th><th>Existencias</th><th>Disponibilidad</th><th>Acciones</th></tr>';
    $('#table-body').innerHTML = rows.map((item) => `<tr><td class="cell-id">#${esc(item.id)}</td><td class="product-name">${esc(item.nombre)}</td><td>${esc(item.codigo)}</td><td>${esc(item.stock)}</td><td><span class="pill ${Number(item.stock) === 0 ? 'low' : ''}">${Number(item.stock) === 0 ? 'Agotado' : 'En inventario'}</span></td><td class="actions"><button type="button" class="row-action" data-action="edit" data-id="${esc(item.id)}">Editar</button><button type="button" class="row-action danger" data-action="delete" data-id="${esc(item.id)}">Eliminar</button></td></tr>`).join('');
  }

  function renderClients(rows) {
    $('#table-head').innerHTML = '<tr><th>ID</th><th>Cliente</th><th>Correo electrónico</th><th>Usuario asociado</th><th>Acciones</th></tr>';
    $('#table-body').innerHTML = rows.map((item) => `<tr><td class="cell-id">#${esc(item.id)}</td><td class="product-name">${esc(item.nombre)}</td><td>${esc(item.email)}</td><td>${item.id_user == null ? '—' : `#${esc(item.id_user)}`}</td><td class="actions"><button type="button" class="row-action" data-action="edit" data-id="${esc(item.id)}">Editar</button><button type="button" class="row-action danger" data-action="delete" data-id="${esc(item.id)}">Eliminar</button></td></tr>`).join('');
  }

  async function loadData() {
    const refresh = $('#refresh-button');
    refresh.disabled = true;
    notice.hidden = true;
    $('#table-body').innerHTML = '<tr><td colspan="6">Cargando datos…</td></tr>';
    $('#empty-state').hidden = true;
    try {
      const query = new URLSearchParams({salto:String(offset), limite:String(limit)});
      const result = await request(`${endpoint()}?${query}`);
      currentRows = moduleName === 'products' ? (result.data || []) : (Array.isArray(result) ? result : []);
      if (moduleName === 'products') totalPages = Math.max(1, Number(result.total_paginas || 1));
      else totalPages = currentRows.length === limit ? Math.floor(offset / limit) + 2 : Math.floor(offset / limit) + 1;
      if (moduleName === 'products') renderProducts(currentRows); else renderClients(currentRows);
      const empty = currentRows.length === 0;
      $('#empty-state').hidden = !empty;
      $('#table-head').hidden = empty;
      $('#result-count').textContent = moduleName === 'products' ? `${result.total || 0} ${Number(result.total) === 1 ? 'producto' : 'productos'}` : `${currentRows.length ? `${offset + 1}–${offset + currentRows.length}` : '0'} clientes mostrados`;
      $('#page-indicator').textContent = `Página ${Math.floor(offset / limit) + 1}`;
      $('#prev-page').disabled = offset === 0;
      $('#next-page').disabled = Math.floor(offset / limit) + 1 >= totalPages;
    } catch (error) {
      $('#table-body').innerHTML = '';
      $('#table-head').hidden = true;
      $('#empty-state').hidden = true;
      showNotice(error.message);
      $('#result-count').textContent = 'No se pudieron cargar los datos';
    } finally { refresh.disabled = false; }
  }

  function selectModule(next) {
    moduleName = next;
    offset = 0;
    const products = next === 'products';
    document.querySelectorAll('.nav-link').forEach((button) => button.classList.toggle('active', button.dataset.module === next));
    const title = products ? 'Productos' : 'Clientes';
    $('#breadcrumb-current').textContent = title;
    $('#page-title').textContent = title;
    $('#page-kicker').textContent = products ? 'INVENTARIO' : 'DIRECTORIO';
    $('#page-description').textContent = products ? 'Administra los productos registrados en tu almacén.' : 'Administra los clientes registrados en el sistema.';
    $('#table-title').textContent = `Listado de ${title.toLowerCase()}`;
    $('#create-button').textContent = products ? '+ Nuevo producto' : '+ Nuevo cliente';
    loadData();
  }

  function openModal(mode, record = null) {
    const products = moduleName === 'products';
    const editing = mode === 'edit';
    $('#modal-title').textContent = `${editing ? 'Editar' : 'Nuevo'} ${products ? 'producto' : 'cliente'}`;
    $('#modal-description').textContent = editing ? 'Actualiza los datos del registro.' : 'Completa los datos para agregar un registro.';
    const fields = products
      ? `<label>Nombre<input name="nombre" minlength="3" maxlength="25" value="${esc(record?.nombre)}" required></label><label>Código<input name="codigo" value="${esc(record?.codigo)}" required></label><label>Existencias<input name="stock" type="number" min="0" value="${esc(record?.stock ?? 0)}" required></label>`
      : editing
        ? `<label>Nombre<input name="nombre" minlength="3" maxlength="30" value="${esc(record?.nombre)}" required></label><label>Correo electrónico<input name="email" type="email" value="${esc(record?.email)}" required></label>`
        : `<label>Nombre<input name="nombre" minlength="3" maxlength="30" required></label><label>Correo electrónico<input name="email" type="email" required></label><label>Usuario<input name="user" minlength="5" maxlength="16" required></label><label>Contraseña<input name="password" type="password" minlength="6" maxlength="20" required></label><label>Rol<select name="rol"><option value="Usuario">Usuario</option><option value="Admin">Admin</option></select></label>`;
    $('#modal-fields').innerHTML = fields;
    modalForm.dataset.mode = mode;
    modalForm.dataset.id = record?.id ?? '';
    modal.showModal();
    $('#modal-fields input').focus();
  }

  $('#create-button').addEventListener('click', () => openModal('create'));
  $('#modal-close').addEventListener('click', () => modal.close());
  $('#modal-cancel').addEventListener('click', () => modal.close());
  $('#refresh-button').addEventListener('click', loadData);
  $('#page-size').addEventListener('change', (event) => { limit = Number(event.target.value); offset = 0; loadData(); });
  $('#prev-page').addEventListener('click', () => { offset = Math.max(0, offset - limit); loadData(); });
  $('#next-page').addEventListener('click', () => { offset += limit; loadData(); });
  document.querySelectorAll('.nav-link').forEach((button) => button.addEventListener('click', () => selectModule(button.dataset.module)));
  $('#logout-button').addEventListener('click', () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.assign('/');
  });

  $('#table-body').addEventListener('click', async (event) => {
    const button = event.target.closest('button[data-action]');
    if (!button) return;
    const record = currentRows.find((row) => String(row.id) === button.dataset.id);
    if (!record) return;
    if (button.dataset.action === 'edit') { openModal('edit', record); return; }
    if (!window.confirm(`¿Eliminar ${moduleName === 'products' ? 'el producto' : 'el cliente'} “${record.nombre}”? Esta acción no se puede deshacer.`)) return;
    button.disabled = true;
    try {
      await request(`${endpoint()}${encodeURIComponent(record.id)}`, {method:'DELETE'});
      showNotice('Registro eliminado correctamente.', 'success');
      if (currentRows.length === 1 && offset > 0) offset = Math.max(0, offset - limit);
      await loadData();
    } catch (error) { showNotice(error.message); button.disabled = false; }
  });

  modalForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const submit = $('#modal-save');
    const formData = new FormData(modalForm);
    const payload = Object.fromEntries(formData.entries());
    if (moduleName === 'products') payload.stock = Number(payload.stock);
    const mode = modalForm.dataset.mode;
    const id = modalForm.dataset.id;
    const method = mode === 'create' ? 'POST' : 'PUT';
    const path = mode === 'create' ? endpoint() : `${endpoint()}${encodeURIComponent(id)}`;
    submit.disabled = true;
    submit.textContent = 'Guardando…';
    try {
      await request(path, {method, body:JSON.stringify(payload)});
      modal.close();
      showNotice(mode === 'create' ? 'Registro creado correctamente.' : 'Cambios guardados correctamente.', 'success');
      await loadData();
    } catch (error) { showNotice(error.message); }
    finally { submit.disabled = false; submit.textContent = 'Guardar'; }
  });

  selectModule('products');
})();
