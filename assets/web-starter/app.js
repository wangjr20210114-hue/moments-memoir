const story = window.STORY;
const $ = (selector, root = document) => root.querySelector(selector);
const safe = (value = '') => String(value).replace(/[&<>\"]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));

$('#title').textContent = story.title;
$('#range').textContent = story.range;
$('#intro').textContent = story.intro;
$('#ending-title').textContent = story.endingTitle;
$('#ending-text').textContent = story.endingText;
$('#stats').innerHTML = story.stats.map(([number, label]) => `<div><strong>${safe(number)}</strong><span>${safe(label)}</span></div>`).join('');
$('#chapters').innerHTML = story.chapters.map((chapter) => `
  <article class="chapter" data-no="${safe(chapter.no)}">
    <div class="copy"><p class="eyebrow">CHAPTER ${safe(chapter.no)} · ${safe(chapter.year)}</p><h2>${safe(chapter.title)}</h2><p>${safe(chapter.text)}</p><blockquote>${safe(chapter.quote)}</blockquote><small>${safe(chapter.dates)} · ${safe(chapter.location)}</small></div>
    <button class="media" type="button" aria-label="打开${safe(chapter.title)}"><img src="${safe(chapter.image)}" alt="${safe(chapter.imageAlt)}" loading="lazy" /></button>
  </article>`).join('');

const dialog = $('#detail');
$('#chapters').addEventListener('click', (event) => {
  const button = event.target.closest('.media');
  if (!button) return;
  const chapter = story.chapters.find((item) => item.no === button.closest('.chapter').dataset.no);
  const image = $('img', dialog);
  image.src = chapter.image; image.alt = chapter.imageAlt;
  $('.eyebrow', dialog).textContent = `${chapter.dates} · ${chapter.location}`;
  $('h2', dialog).textContent = chapter.title;
  $('.dialog-text', dialog).textContent = chapter.text;
  $('blockquote', dialog).textContent = chapter.quote;
  dialog.showModal();
});
$('button', dialog).addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
