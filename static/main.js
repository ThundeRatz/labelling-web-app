let editor;

$(document).ready(() => {
  editor = new BBoxAnnotator({
    id: '#bbox-annotator',
    url: $('#bbox-annotator').data('link'),
    input_method: 'fixed',
    border_width: 1,
    width: 1280,
    height: 960,
    onchange: annotation => {},
    onload: () => {
        $('#loading-image').hide();
    }
  });
});

let submits = 0;

const doPost = data => {
  $.ajax({
    type: 'POST',
    url: 'post_label',
    contentType: 'application/json;charset=utf-8',
    dataType: 'json',
    data: JSON.stringify(data),
    success: data => {
      location.reload(true);
      submits++;
      localStorage.setItem('submission_count', submits);
      $('#submission-count').text(submits);
    },
    error: msg => {
      alert('Submitting failed');
      $('#submit-button').prop('disabled', false);
    },
  });
};

const initSubmits = () => {
  let submitStr = localStorage.getItem('submission_count');
  if (submitStr == undefined) {
    localStorage.setItem('submission_count', 0);
  } else {
    submits = parseInt(submitStr);
  }
  $('#submission-count').text(submits);
};

const sendBoxes = () => {
  if (editor.entries.length == 0) {
    alert('Create selections before submitting');
    return;
  }
  let labels = [];
  for (let i = 0; i < editor.entries.length; i++) {
    let box = editor.entries[i];
    labels.push({
      x: (box['left'] + box['width'] / 2) / 1280,
      y: (box['top'] + box['height'] / 2) / 960,
      width: box['width'] / 1280,
      height: box['height'] / 960,
    });
  }

  $('#submit-button').prop('disabled', true);
  doPost({ labels: labels, image_id: $('#bbox-annotator').data('id') });
};

initSubmits();
