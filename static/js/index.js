let page = 1; // 현재 페이지를 담을 변수
let maxPage = 2; // 최대 페이지 수를 받아와서 담을 변수

$(document).ready(() => {
  listing(page); // 준비되면 첫번째 페이지 불러오기
});

function listing(page) {
  // 페이지를 불러오는 함수
  $.ajax({
    type: 'GET',
    url: '/api/articles',
    data: { page }, // 요청 uri 뒤에 ?page=페이지수 추가
    success: (res) => {
      maxPage = res.max_page;

      const listOfArticles = $('#listOfArticles');

      res.articles.forEach((article) => {
        const { postedByNick, postedBy, title, content, image, _id } = article;

        const tempHTML = `
            <div class="col">
              <div class="card">
                <a href="/article/${_id}">
                  <img
                    src="${image}"
                    class="card-img-top"
                    alt="thumbnail"
                  />
                </a>
                <div class="card-body">
                  <h5 class="card-title">${title}</h5>
                  <p class="card-text">
                    ${
                      content.length > 20
                        ? content.slice(0, 20) + '...'
                        : content
                    }
                  </p>
                  <p class="card-text">
                    ${postedByNick}(${postedBy})
                  </p>
                </div>
              </div>
            </div>
          `;

        listOfArticles.append(tempHTML);
      });
    },
  });
}

// 무한 스크롤
setInterval(() => {
  if (
    $(window).scrollTop() >=
      $(document).height() - $(window).height() - $(window).height() * 0.2 &&
    page < maxPage
  ) {
    listing(++page);
  }
}, 750);
