(function () {
  'use strict';

  var dataEl = document.getElementById('freebies-data');
  if (!dataEl) {
    return;
  }

  var payload = JSON.parse(dataEl.textContent);
  var tools = payload.tools || [];
  var categories = payload.categories || [];

  var searchEl = document.getElementById('search');
  var categoryEl = document.getElementById('category');
  var resetEl = document.getElementById('reset');
  var gridEl = document.getElementById('grid');
  var countEl = document.getElementById('count');

  categories.forEach(function (cat) {
    var opt = document.createElement('option');
    opt.value = cat.key;
    opt.textContent = cat.label;
    categoryEl.appendChild(opt);
  });

  function normalize(value) {
    return String(value == null ? '' : value).toLowerCase();
  }

  function matches(tool, term, catKey) {
    if (catKey && tool.category !== catKey) {
      return false;
    }
    if (!term) {
      return true;
    }
    var haystack = [
      tool.name,
      tool.description,
      tool.cost,
      tool.platform,
      tool.officialLink,
      tool.steps.join(' ')
    ].join(' ');
    return normalize(haystack).indexOf(normalize(term)) !== -1;
  }

  function card(tool) {
    var article = document.createElement('article');
    article.className = 'card';

    var header = document.createElement('div');
    header.className = 'card-header';

    var title = document.createElement('h3');
    title.textContent = tool.name;

    var chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = tool.category;

    header.appendChild(title);
    header.appendChild(chip);

    var desc = document.createElement('p');
    desc.className = 'desc';
    desc.textContent = tool.description;

    var facts = document.createElement('ul');
    facts.className = 'facts';

    var costItem = document.createElement('li');
    costItem.innerHTML = '<strong>Cost:</strong> ' + escapeHtml(tool.cost);
    var platformItem = document.createElement('li');
    platformItem.innerHTML = '<strong>Platform:</strong> ' + escapeHtml(tool.platform);

    facts.appendChild(costItem);
    facts.appendChild(platformItem);

    var details = document.createElement('div');
    details.className = 'details';

    var stepDetails = document.createElement('details');
    var summary = document.createElement('summary');
    summary.textContent = 'Steps to get started';
    var ol = document.createElement('ol');
    tool.steps.forEach(function (step) {
      var li = document.createElement('li');
      li.textContent = step;
      ol.appendChild(li);
    });
    stepDetails.appendChild(summary);
    stepDetails.appendChild(ol);

    var link = document.createElement('a');
    link.className = 'btn';
    link.href = tool.officialLink;
    link.textContent = 'Official site';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';

    details.appendChild(stepDetails);
    details.appendChild(link);

    article.appendChild(header);
    article.appendChild(desc);
    article.appendChild(facts);
    article.appendChild(details);

    return article;
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function render() {
    var term = searchEl.value.trim();
    var catKey = categoryEl.value;
    var filtered = tools.filter(function (tool) {
      return matches(tool, term, catKey);
    });

    gridEl.innerHTML = '';
    countEl.textContent =
      filtered.length + ' tool' + (filtered.length !== 1 ? 's' : '') + ' matching';

    if (filtered.length === 0) {
      var none = document.createElement('p');
      none.className = 'none';
      none.textContent = 'No tools match your search.';
      gridEl.appendChild(none);
      return;
    }

    var byCat = {};
    filtered.forEach(function (tool) {
      if (!byCat[tool.category]) {
        byCat[tool.category] = [];
      }
      byCat[tool.category].push(tool);
    });

    categories.forEach(function (cat) {
      var items = byCat[cat.key];
      if (!items || items.length === 0) {
        return;
      }
      var section = document.createElement('section');
      var heading = document.createElement('h2');
      heading.textContent = cat.label;
      section.appendChild(heading);
      items.forEach(function (tool) {
        section.appendChild(card(tool));
      });
      gridEl.appendChild(section);
    });
  }

  searchEl.addEventListener('input', render);
  categoryEl.addEventListener('change', render);
  resetEl.addEventListener('click', function () {
    searchEl.value = '';
    categoryEl.value = '';
    render();
  });

  render();
})();
