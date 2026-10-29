(() => {
  const base = window.siteBase || '';
  const q = new URLSearchParams(location.search);
  const local = p => base + p;
  const route = location.pathname.slice(base.length) || '/';
  const legacyID = q.get('p') || q.get('page_id') || q.get('attachment_id');
  if (legacyID) fetch(local('/assets/legacy-urls.json')).then(r => r.json()).then(map => {
    if (map[legacyID]) location.replace(local((q.get('lang') === 'en' && !map[legacyID].startsWith('/wp-content/') && map[legacyID] !== '/forums/' ? '/en' : '') + map[legacyID]) + location.hash);
  });
  if (q.has('s')) location.replace(local('/search/') + '?q=' + encodeURIComponent(q.get('s')));
  if (q.get('lang') === 'en' && !route.startsWith('/en/') && !legacyID) {
    const counterpart = document.querySelector('link[hreflang="en"]');
    if (counterpart) location.replace(local(new URL(counterpart.href).pathname.replace(base, '')));
    else if (route === '/') location.replace(local('/en/'));
  }
  const form = document.getElementById('site-search');
  if (!form) return;
  const input = document.getElementById('query'), results = document.getElementById('search-results'), status = document.getElementById('search-status');
  let data;
  async function search(value) {
    status.textContent = '検索中…'; results.replaceChildren();
    try {
      data ||= await fetch(local('/assets/search.json')).then(r => { if (!r.ok) throw Error(); return r.json(); });
      const words = value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const matches = words.length ? data.filter(p => words.every(w => (p.title + ' ' + p.text).toLocaleLowerCase().includes(w))) : [];
      status.textContent = matches.length + '件見つかりました。';
      for (const p of matches) {
        const a = document.createElement('a'); a.href = local(p.url); a.textContent = p.title;
        const h = document.createElement('h2'); h.append(a);
        const excerpt = document.createElement('p'); excerpt.textContent = p.text.slice(0, 180) + '…';
        const article = document.createElement('article'); article.append(h, excerpt); results.append(article);
      }
    } catch { status.textContent = '検索情報を読み込めませんでした。記事一覧をご利用ください。'; }
  }
  form.addEventListener('submit', e => { e.preventDefault(); history.replaceState(null, '', '?q=' + encodeURIComponent(input.value)); search(input.value); });
  if (q.has('q')) { input.value = q.get('q'); search(input.value); }
})();