const search = instantsearch({
  appId: '1AWHE68HXJ',
  apiKey: '1ad3c77c0558e6fbb2f1946f8c302eef',
  indexName: 'blog',
  searchParameters: {
    hitsPerPage: 10,
  },
  urlSync: {
    trackedParameters: ['query', 'attribute:*', 'page'],
  },
});

search.addWidget(
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  })
);

const dateString = time =>
  new Date(time * 1000).toLocaleString();
const Time = ({ date }) =>
  `<time datetime=${date} class="muted">
    ${dateString(date)}
   </time>`;

const stripHighlight = text =>
  text.replace(/<\/?mark>/g, '');
const Tag = ({ tag, highlighted }) =>
  `<a href="/tags#${tag}" onclick="refineTag(${tag});">#${highlighted}</a>`;
const Tags = ({ tags }) =>
  tags
    .map(({ value }) =>
      Tag({
        tag: stripHighlight(value),
        highlighted: value,
      })
    )
    .join(', ');

const Text = ({ text, url }) =>
  `<p><a href="${url}" class="invisible">${text}</a></p>`;

const Hit = ({
  _highlightResult: {
    tags,
    text: { value: text },
    title: { value: title },
  },
  url,
  posted_at: date,
}) => `
<article>
  <h3><a href="${url}">${title}</a></h3>
  ${Time({ date })}
  ${Tags({ tags })}
  ${Text({ text, url })}
  <a href="${url}">read more</a>
</article>
`;

search.addWidget(
  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      empty: 'No results',
      allItems: ({ hits, query }) => {
        if (
          query.length > 0 ||
          window.showResultsByDefault
        ) {
          document.getElementById(
            'pagination'
          ).hidden = false;
          return hits.map(Hit).join('');
        }
        document.getElementById('pagination').hidden = true;
      },
    },
  })
);

search.addWidget(
  instantsearch.widgets.pagination({
    container: '#pagination',
  })
);

search.start();
