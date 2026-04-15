const SITE_PASSWORD = "Hello3838";
const COOKIE_NAME = "theophysics_auth";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 90; // 90 days

function loginPage(error = "") {
  return new Response(
    `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Theophysics — Sign In</title>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&family=Oswald:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root { --bg:#050505; --surface:#0a0a0a; --border:#222; --text:#e0e0e0; --gold:#d4af37; --red:#c94040; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); min-height:100vh; display:flex; align-items:center; justify-content:center; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:.8rem; padding:2.5rem; max-width:380px; width:90%; text-align:center; }
.card h1 { font-family:'Crimson Text',serif; font-size:1.6rem; color:white; margin-bottom:.25rem; }
.card .sub { font-size:.8rem; color:#999; margin-bottom:1.5rem; }
.card .eq { font-family:'Crimson Text',serif; font-size:.9rem; color:var(--gold); opacity:.5; margin-bottom:1.5rem; }
input[type=password] { width:100%; padding:.7rem 1rem; background:#111; border:1px solid var(--border); border-radius:.4rem; color:var(--text); font-family:'Inter',sans-serif; font-size:.9rem; outline:none; transition:border-color .2s; }
input[type=password]:focus { border-color:var(--gold); }
button { width:100%; margin-top:.75rem; padding:.7rem; background:var(--gold); color:#050505; border:none; border-radius:.4rem; font-family:'Oswald',sans-serif; font-size:.85rem; letter-spacing:.1em; text-transform:uppercase; cursor:pointer; transition:background .2s; }
button:hover { background:#e8c84a; }
.error { color:var(--red); font-size:.8rem; margin-top:.75rem; }
.footer { font-size:.7rem; color:#555; margin-top:1.25rem; }
</style>
</head>
<body>
<div class="card">
  <h1>Theophysics</h1>
  <div class="sub">Family Access</div>
  <div class="eq">&chi; = f(G, M, E, S, T, K, R, Q, F, C)</div>
  <form method="POST">
    <input type="password" name="password" placeholder="Enter password" autofocus>
    <button type="submit">Enter</button>
  </form>
  ${error ? `<div class="error">${error}</div>` : ""}
  <div class="footer">David Lowe &middot; POF 2828</div>
</div>
</body>
</html>`,
    {
      status: error ? 401 : 200,
      headers: { "Content-Type": "text/html;charset=UTF-8" },
    }
  );
}

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  const cookies = request.headers.get("Cookie") || "";

  // Check if already authenticated
  const authed = cookies.split(";").some(
    (c) => c.trim() === `${COOKIE_NAME}=authenticated`
  );

  if (authed) {
    return context.next();
  }

  // Handle login form submission
  if (request.method === "POST") {
    const form = await request.formData();
    const password = form.get("password");

    if (password === SITE_PASSWORD) {
      const response = new Response(null, {
        status: 302,
        headers: {
          Location: url.pathname,
          "Set-Cookie": `${COOKIE_NAME}=authenticated; Path=/; Max-Age=${COOKIE_MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
        },
      });
      return response;
    }

    return loginPage("Wrong password. Try again.");
  }

  // Show login page
  return loginPage();
}
