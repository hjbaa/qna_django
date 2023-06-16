$(document).ready(function() {
  $('.mark-correct-btn').click(function() {
    const button = $(this);
    let answer_id = button.data("answer-id");

    $.ajax({
      type: 'POST',
      url: window.location.origin + '/mark_correct/',
      data: {
        'answer_id': answer_id,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: 'json',
      success: function(data) {
        if (data.success) {
          const unmarked = data.unmarked_ans;
          if (unmarked === answer_id) {
            button.find('img').attr('src', '/static/svg/correct-grey.svg');
          } else {
            let prev_button = $("button[data-answer-id='" + unmarked + "']");
            if (prev_button) {
              prev_button.find('img').attr('src', '/static/svg/correct-grey.svg');
            }

            button.find('img').attr('src', '/static/svg/correct-green.svg');
          }

        } else {
          alert(data.error);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        alert('Request failed: ' + errorThrown);
      }
    });
  });
});

function findPreviousCorrect() {

}
