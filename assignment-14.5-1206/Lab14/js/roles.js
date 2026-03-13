const roleSelect = document.getElementById('roleSelect');
const loginButton = document.getElementById('loginBtn');
const currentRole = document.getElementById('currentRole');
const logoutButton = document.getElementById('logoutBtn');
const permissionItems = document.querySelectorAll('[data-permission]');

const ROLE_KEY = 'lab14_role';

function applyPermissions(role) {
  currentRole.textContent = role || 'Not logged in';

  permissionItems.forEach((item) => {
    const permission = item.dataset.permission;

    // Admin sees all, editor sees view+edit, user sees only view.
    const visible =
      role === 'Admin' ||
      (role === 'Editor' && permission !== 'admin') ||
      (role === 'User' && permission === 'view');

    item.classList.toggle('hidden', !visible);
  });
}

function login() {
  const role = roleSelect.value;
  localStorage.setItem(ROLE_KEY, role);
  applyPermissions(role);
}

function logout() {
  localStorage.removeItem(ROLE_KEY);
  applyPermissions('');
}

loginButton.addEventListener('click', login);
logoutButton.addEventListener('click', logout);

const savedRole = localStorage.getItem(ROLE_KEY);
if (savedRole) {
  roleSelect.value = savedRole;
  applyPermissions(savedRole);
} else {
  applyPermissions('');
}
