document.addEventListener("DOMContentLoaded", function () {
  const ad = document.getElementById("ad").value;
  const me = document.getElementById("username").value;
  const commentsDiv = document.getElementById("comments");
  const commentForm = document.getElementById("comment-form");

  function loadComments() {
    fetch(`/comment/${ad}`)
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then(({ comments }) => {
        commentsDiv.innerHTML = "";
        comments?.forEach(({ username, content, time }) => {
          displayComment(username, content, time);
        });
        if (comments.length)
          document.getElementById(
            "comment-tab"
          ).innerText = `${comments.length} Comments`;
      })
      .catch((error) =>
        console.error("There was a problem with the fetch operation:", error)
      );
  }

  function displayComment(username, comment, time = new Date()) {
    const timeDiff = moment(time).fromNow();
    const commentElement = document.createElement("div");
    commentElement.className = "comment col-md-4";
    commentElement.innerHTML = `<div class='bg-secondary-subtle comment-box rounded p-2'><b>${username}</b><small class='float-end'>${timeDiff}</small><div>${comment}</div></div>`;
    commentsDiv.appendChild(commentElement);
  }

  commentForm?.addEventListener("submit", function (e) {
    e.preventDefault();

    const content = document.getElementById("content").value;

    if (ad && content) {
      fetch("/comment/create", {
        method: "POST",
        body: JSON.stringify({ ad, content }),
        headers: { "Content-Type": "application/json;charset=UTF-8" },
      })
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
        })
        .then((data) => {
          displayComment(me, content);
          commentForm.reset();
        })
        .catch((error) =>
          console.error("There was a problem with the fetch operation:", error)
        );
    }
  });

  loadComments();
});
