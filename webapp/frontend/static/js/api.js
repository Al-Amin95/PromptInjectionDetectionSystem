async function postJson(url, data) {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return resp.json();
}

async function getJson(url) {
  const resp = await fetch(url);
  return resp.json();
}
