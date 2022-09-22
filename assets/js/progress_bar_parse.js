// get cycle count for np5
var node = document.getElementById('np5_cycle_status');
htmlContent = node.innerHTML,
textContent = node.textContent;
cycle_count = textContent.split(" ")[4]

var percentage = cycle_count / 2190 * 100
$('#np5-progress-bar').css('width', percentage+'%').attr('aria-valuenow', percentage);
$('#np5-progress-bar').text(Math.round(percentage) + '%');

// get cycle count for np6
var node = document.getElementById('np6_cycle_status');
htmlContent = node.innerHTML,
textContent = node.textContent;
cycle_count = textContent.split(" ")[4]

var percentage = cycle_count / 2190 * 100
$('#np6-progress-bar').css('width', percentage+'%').attr('aria-valuenow', percentage);
$('#np6-progress-bar').text(Math.round(percentage) + '%');

