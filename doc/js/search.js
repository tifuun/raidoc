function search(term) {
  results = [];
  for (const page of search_index) {
    score = 0;
    page_name = page[0];
    page_keywords = page[1];

    for (var rank = 0; rank < page_keywords.length; rank++) {
      for (const keyword of page_keywords[rank]) {
        if (!keyword.includes(term)) {
          continue;
        }
        score += (page_keywords.length - rank);
      }
    }

    if (score <= 0) {
      continue;
    }

    for (var i = 0; i < results.length; i++) {
      if (results[i][1] < score) {
        break;
      }
    }

    results.splice(i, 0, [page_name, score]);
  }

  return results;
}

function do_search() {
  term = document.getElementById('searchbox').value;
  console.log(term);
  results = search(term);
  div = document.getElementById("search-results");
  div.innerHTML = "";

  for (const page of results) {
    div.innerHTML += `<a href="${page[0]}">${page[0]}</a><br>`;
  }
}

