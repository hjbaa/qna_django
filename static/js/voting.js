$(document).ready(function() {
  $('.vote-button').click(function() {
    const button = $(this);
    const voteAction = button.data('vote-action');
    const contentType = button.data('content-type');
    const objectId = button.data('object-id');

    $.ajax({
      type: 'POST',
      url: `${window.location.origin}/vote/`,
      data: {
        'content_type': contentType,
        'object_id': objectId,
        'vote_action': voteAction,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: 'json',
      success: function (data) {
        if (data.success) {
          const button = $(`.vote-button[data-content-type="${contentType}"][data-object-id="${objectId}"][data-vote-action="${voteAction}"]`);
          const ratingButton = $(`.rating-button[data-content-type="${contentType}"][data-object-id="${objectId}"]`);
          ratingButton.text(data.rating);

          const anotherButtonAction = voteAction === 'upvote' ? 'downvote' : 'upvote';
          const anotherButton = $(`.vote-button[data-content-type="${contentType}"][data-object-id="${objectId}"][data-vote-action="${anotherButtonAction}"]`);
          const { upvote_icon_black, upvote_icon_blue, downvote_icon_black, downvote_icon_blue } = data;
          const anotherButtonIcon = voteAction === 'upvote' ? downvote_icon_black : upvote_icon_black;

          anotherButton.removeClass('btn-outline-primary').addClass('btn-outline-secondary');
          anotherButton.find('img').attr('src', anotherButtonIcon);
          changeButtonIcon(button, voteAction, data);
          button.toggleClass('btn-outline-secondary btn-outline-primary');
        } else {
          alert(data.error);
        }
      },
      error: function (xhr, textStatus, errorThrown) {
        alert(`Voting request failed: ${errorThrown}`);
      }
    });
  });
});

function changeButtonIcon(button, action, data) {
  const buttonIcon = button.find('img');
  const { upvote_icon_black, upvote_icon_blue, downvote_icon_black, downvote_icon_blue } = data;

  if (action === 'upvote') {
    buttonIcon.attr('src', buttonIcon.attr('src').includes(upvote_icon_black) ? upvote_icon_blue : upvote_icon_black);
  } else {
    buttonIcon.attr('src', buttonIcon.attr('src').includes(downvote_icon_black) ? downvote_icon_blue : downvote_icon_black);
  }
}
