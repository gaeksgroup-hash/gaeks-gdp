import assert from 'node:assert/strict';

const baseUrl = process.env.GDP_TEST_URL || 'http://127.0.0.1:8787';

class Client {
  cookies = new Map();

  async request(path, { method = 'GET', body, csrf = false } = {}) {
    const headers = { Accept: 'application/json' };
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (this.cookies.size) headers.Cookie = [...this.cookies].map(([key, value]) => `${key}=${value}`).join('; ');
    if (csrf) headers['X-CSRF-Token'] = this.cookies.get('gaeks_csrf') || '';
    const response = await fetch(baseUrl + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
    const setCookies = response.headers.getSetCookie?.() || [];
    for (const header of setCookies) {
      const [pair] = header.split(';', 1);
      const separator = pair.indexOf('=');
      if (separator > 0) this.cookies.set(pair.slice(0, separator), pair.slice(separator + 1));
    }
    const payload = await response.json();
    return { response, payload };
  }

  async expect(path, options, status) {
    const result = await this.request(path, options);
    assert.equal(result.response.status, status, `${path}: ${JSON.stringify(result.payload)}`);
    return result.payload;
  }
}

async function register(client, email, name) {
  await client.expect('/api/auth.php?action=register_request', {
    method: 'POST',
    body: { email, name, captchaToken: 'test-bypass' },
  }, 200);
  const payload = await client.expect('/api/auth.php?action=register_verify', {
    method: 'POST',
    body: { email, name, password: 'Strong-Test-Password-42!', code: '123456' },
  }, 201);
  assert.equal(payload.data.user.email, email);
  assert.ok(client.cookies.has('__Host-gaeks_session'));
  assert.ok(client.cookies.has('gaeks_csrf'));
}

const suffix = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
const alice = new Client();
const bob = new Client();
await register(alice, `alice-${suffix}@example.test`, 'Alice Test');
await register(bob, `bob-${suffix}@example.test`, 'Bob Test');

const me = await alice.expect('/api/auth.php?action=me', {}, 200);
assert.equal(me.data.user.name, 'Alice Test');

const createdCv = await alice.expect('/api/cv.php?action=save', {
  method: 'POST', csrf: true,
  body: { cv: { title: 'CV Alice', data: { fullName: 'Alice' }, completeness: 80, isDraft: false } },
}, 201);
const cvId = createdCv.data.id;
assert.equal(createdCv.data.version, 1);
await bob.expect(`/api/cv.php?action=get&id=${encodeURIComponent(cvId)}`, {}, 404);

const updatedCv = await alice.expect('/api/cv.php?action=save', {
  method: 'POST', csrf: true,
  body: { cv: { id: cvId, version: 1, title: 'CV Alice Updated', data: { fullName: 'Alice A.' }, completeness: 95 } },
}, 200);
assert.equal(updatedCv.data.version, 2);
await alice.expect('/api/cv.php?action=delete', { method: 'POST', csrf: true, body: { id: cvId } }, 200);
const trash = await alice.expect('/api/cv.php?action=list&tab=trash', {}, 200);
assert.equal(trash.data.length, 1);
await alice.expect('/api/cv.php?action=restore', { method: 'POST', csrf: true, body: { id: cvId } }, 200);

const createdPresentation = await alice.expect('/api/presentation.php?action=save', {
  method: 'POST', csrf: true,
  body: { data: { meetingName: 'Quarterly Review', meetingDate: '2026-09-15', slides: [{ title: 'Opening' }] } },
}, 201);
const presentationId = createdPresentation.data.id;
await bob.expect(`/api/presentation.php?action=get&id=${encodeURIComponent(presentationId)}`, {}, 404);
const presentations = await alice.expect('/api/presentation.php?action=list', {}, 200);
assert.equal(presentations.data.length, 1);
await alice.expect('/api/presentation.php?action=status', {
  method: 'POST', csrf: true, body: { id: presentationId, status: 'trashed' },
}, 200);
await alice.expect('/api/presentation.php?action=status', {
  method: 'POST', csrf: true, body: { id: presentationId, status: 'active' },
}, 200);

await alice.expect('/api/cv.php?action=delete_permanent', { method: 'POST', csrf: true, body: { id: cvId } }, 200);
await alice.expect('/api/presentation.php?action=status', {
  method: 'POST', csrf: true, body: { id: presentationId, status: 'delete_permanent' },
}, 200);

await alice.expect('/api/auth.php?action=logout', { method: 'POST', csrf: true, body: {} }, 200);
await alice.expect('/api/auth.php?action=me', {}, 401);

console.log('Backend E2E passed: auth, sessions, CSRF, CV, presentation, ownership, lifecycle, logout.');
