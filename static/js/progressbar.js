setInterval(check_progress, 1000)

function check_progress()
{
  $.get('/get_progress', function(prog) {
    $('.progress-bar').width(prog + '%');
  })
}
