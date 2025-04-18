document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    login(username, password);
});

document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;
    signup(username, password);
});

document.getElementById('to-signup').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('signup-form').classList.remove('hidden');
});

document.getElementById('to-login').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('signup-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
});

async function login(username, password) {
    const messageEl = document.getElementById('login-error');

    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (res.ok) {
        localStorage.setItem('token', data.token);
        window.location.href = "/";

    } else {
        messageEl.textContent = data.error || 'Login failed';
        messageEl.style.color = 'red';
    }
}

async function signup(username, password) {
    const messageEl = document.getElementById('signup-error');

    const res = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
        login(username, password)

    } else {
        messageEl.textContent = data.error || 'Signup failed';
        messageEl.style.color = 'red';
    }
}