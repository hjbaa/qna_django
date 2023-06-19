$(document).ready(function() {
  $('.mark-correct-btn').click(function() {
    const button = $(this);
    const answerId = button.data("answer-id");

    $.ajax({
      type: 'POST',
      url: `${window.location.origin}/mark_correct/`,
      data: {
        'answer_id': answerId,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: 'json',
      success: function(data) {
        if (data.success) {
          const { unmarked_ans, unmarked_answer_icon_path, correct_answer_icon_path } = data;
          const prevButton = $(`.mark-correct-btn[data-answer-id='${unmarked_ans}']`);

          button.find('img').attr('src', correct_answer_icon_path);

          if (prevButton) {
            prevButton.find('img').attr('src', unmarked_answer_icon_path);
          }
        } else {
          alert(data.error);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        alert(`Request failed: ${errorThrown}`);
      }
    });
  });
});
