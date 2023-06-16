$(document).ready(function() {
  $('.vote-button').click(function() {
    const button = $(this);
    const vote_action = button.data('vote-action');
    const content_type = button.data('content-type');
    const object_id = button.data('object-id');

    $.ajax({
      type: 'POST',
      url: window.location.origin + '/vote/',
      data: {
        'content_type': content_type,
        'object_id': object_id,
        'vote_action': vote_action,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: 'json',
      success: function(data) {
        if (data.success) {
          const ratingButton = $('.rating-button[data-content-type="' + content_type + '"][data-object-id="' + object_id + '"]');
          ratingButton.text(data.rating);

          let another_button;
          let another_button_icon;

          if (vote_action === 'upvote') {
            another_button = $('.vote-button[data-content-type="' + content_type + '"][data-object-id="' + object_id + '"][data-vote-action="downvote"]');
            another_button_icon = '/static/svg/arrow-down-black.svg';
          } else {
            another_button = $('.vote-button[data-content-type="' + content_type + '"][data-object-id="' + object_id + '"][data-vote-action="upvote"]');
            another_button_icon = '/static/svg/arrow-up-black.svg';
          }

          another_button.removeClass('btn-outline-primary');
          another_button.addClass('btn-outline-secondary');
          another_button.find('img').attr('src', another_button_icon)

          changeButtonIcon(button, vote_action)
          button.toggleClass('btn-outline-secondary btn-outline-primary')
        } else {
          alert(data.error);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        alert('Voting request failed: ' + errorThrown);
      }
    });
  });
});

function changeButtonIcon(button, action) {
  const buttonIcon = button.find('img');
  const arrowUpBlack = '/static/svg/arrow-up-black.svg';
  const arrowUpBlue = '/static/svg/arrow-up-blue.svg';
  const arrowDownBlack = '/static/svg/arrow-down-black.svg';
  const arrowDownBlue = '/static/svg/arrow-down-blue.svg';

  if (action === 'upvote') {
    buttonIcon.attr('src', buttonIcon.attr('src').indexOf(arrowUpBlack) === -1 ? arrowUpBlack : arrowUpBlue);
  } else {
    buttonIcon.attr('src', buttonIcon.attr('src').indexOf(arrowUpBlack) === -1 ? arrowDownBlack : arrowDownBlue);
  }
}

