// 자막을 표시하는 함수
function displaySubtitles(text) {
  const subtitleText = document.querySelector('#subtitleText');
  if (subtitleText) {
    subtitleText.textContent = text;
  }
}

// Python 서버로 YouTube URL을 전송하는 함수
function sendUrlToServer(url) {
  fetch('http://localhost:8080/process_url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `url=${encodeURIComponent(url)}`,
  })
  .then(response => response.text())
  .then(data => {
    console.log("Server response:", data);
  })
  .catch(error => {
    console.error('Error sending URL to server:', error);
  });
}

// Python 서버로부터 자막을 가져와 표시하는 함수
function fetchPythonSubtitles() {
  fetch(`http://localhost:8080/get_subtitle?lang=${selectedLanguage}`)
    .then(response => response.text())
    .then(text => {
      displaySubtitles(text);
    })
    .catch(error => {
      console.error('Error fetching subtitles:', error);
    });
}

// 현재 페이지의 URL을 가져와 서버에 전송
const currentUrl = window.location.href;
sendUrlToServer(currentUrl);

// 페이지 로드 시 자막 주기적으로 업데이트 시작
window.addEventListener('load', () => {
  setInterval(fetchPythonSubtitles, 5000); // 5초마다 Python 서버에서 자막 가져오기
});
