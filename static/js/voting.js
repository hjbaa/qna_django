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
          // Update the rating on the page
          const ratingButton = $('.rating-button[data-content-type="' + content_type + '"][data-object-id="' + object_id + '"]');
          ratingButton.text(data.rating);
          button.toggleClass('btn-outline-secondary')
          button.toggleClass('btn-outline-primary')
        } else {
          // Show error message if voting failed
          alert(data.error);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        // Show error message if request failed
        alert('Voting request failed: ' + errorThrown);
      }
    });
  });
});
