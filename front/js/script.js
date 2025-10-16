// script.js (versión corregida y con debug)


document.addEventListener('DOMContentLoaded', () => {
  // Credenciales de prueba
  const HARD_USERNAME = 'usuario1';
  const HARD_PASSWORD = 'Pass1234!';
  

  /* -------------------- LOGIN -------------------- */
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('loginError');

    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      loginError.textContent = '';

      // 1) Validaciones HTML del propio navegador
      if (!loginForm.checkValidity()) {
        loginForm.reportValidity();
        return;
      }

      const enteredUser = usernameInput.value.trim();
      const enteredPass = passwordInput.value;

      // 2) Intentamos login contra localStorage (usuarios registrados)
      // let localUsers = null;
      let localUsers = [];
      try {
        localUsers = JSON.parse(localStorage.getItem('users')) || [];
      } catch (err) {
        console.warn('Error parseando users desde localStorage', err);
        localUsers = [];
      }

      const found = localUsers.find(u => (u.username === enteredUser || u.email === enteredUser) && u.password === enteredPass);

      if (found) {
        // login exitoso usando usuario registrado en localStorage
        console.log('Login OK (localStorage):', found.username || found.email);
        window.location.href = 'calendar.html?user=' + encodeURIComponent(found.username || found.email);
        return;
      }

      // 3) Si no está en localStorage, comprobamos las credenciales hardcodeadas (solo ejemplo)
      if (enteredUser === HARD_USERNAME && enteredPass === HARD_PASSWORD) {
        console.log('Login OK (hardcoded)');
        window.location.href = 'calendar.html?user=' + encodeURIComponent(enteredUser);
        return;
      }

      // 4) Si no coincide nada, mostrar error amigable
      loginError.textContent = 'Credenciales incorrectas. Verifica usuario y contraseña.';
      passwordInput.focus();
      console.log('Login falló para:', enteredUser);
    });
  }

  /* -------------------- REGISTRO -------------------- */
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    const firstNameInput = document.getElementById('firstName');
    const lastNameInput = document.getElementById('lastName');
    const dniInput = document.getElementById('dni');
    const emailInput = document.getElementById('email');
    const birthdateInput = document.getElementById('birthdate');
    const roleSelect = document.getElementById('role');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const registerError = document.getElementById('registerError');

    // Limpiar mensajes custom cuando el usuario escribe de nuevo
    const inputsToClear = [firstNameInput, lastNameInput, dniInput, emailInput, passwordInput, confirmPasswordInput];
    inputsToClear.forEach(inp => {
      if (!inp) return;
      inp.addEventListener('input', () => {
        inp.setCustomValidity('');
        registerError.textContent = '';
      });
    });

    // Específicamente limpiar error de confirmPassword cuando cambian password o confirm
    if (passwordInput) passwordInput.addEventListener('input', () => confirmPasswordInput.setCustomValidity(''));
    if (confirmPasswordInput) confirmPasswordInput.addEventListener('input', () => confirmPasswordInput.setCustomValidity(''));

    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      registerError.textContent = '';

      // 1) Validaciones HTML nativas (required, min, max, pattern, etc.)
      if (!registerForm.checkValidity()) {
        registerForm.reportValidity();
        return;
      }

      // 2) Validación JS: contraseñas iguales
      if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.setCustomValidity('Las contraseñas no coinciden.');
        confirmPasswordInput.reportValidity();
        confirmPasswordInput.focus();
        return;
      } else {
        // Asegurarnos de limpiar cualquier custom validity previo
        confirmPasswordInput.setCustomValidity('');
      }

      // 3) Guardar usuario en localStorage (solo para demo, NO en producción)
      const newUser = {
        username: (firstNameInput.value.trim() + '.' + lastNameInput.value.trim()).toLowerCase(), // ejemplo simple
        email: emailInput.value.trim(),
        password: passwordInput.value, // recordá: en producción NUNCA guardar contraseña en texto plano
        dni: dniInput.value,
        role: roleSelect.value,
        createdAt: new Date().toISOString()
      };

      // Recuperar array de users o crear uno nuevo
      let users = [];
      try {
        users = JSON.parse(localStorage.getItem('users')) || [];
      } catch (err) {
        console.warn('Error parseando users:', err);
        users = [];
      }

      // Evitar duplicados por email
      const exists = users.some(u => u.email === newUser.email || u.dni === newUser.dni);
      if (exists) {
        registerError.textContent = 'Ya existe un usuario con ese email o DNI.';
        return;
      }

      users.push(newUser);
      localStorage.setItem('users', JSON.stringify(users));
      console.log('Usuario registrado (localStorage):', newUser);

      // Mensaje y redirección al login
      alert('Registro completado con éxito. Ahora serás redirigido al inicio de sesión.');
      window.location.href = 'login.html';
    });
  }

});
