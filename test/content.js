// 자막창 생성 및 설정
const subtitleDiv = document.createElement('div');
subtitleDiv.style.position = 'fixed';
subtitleDiv.style.top = '10px';
subtitleDiv.style.right = '10px';
subtitleDiv.style.width = '300px';
subtitleDiv.style.height = 'auto';
subtitleDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
subtitleDiv.style.border = '1px solid black';
subtitleDiv.style.zIndex = '10000';
subtitleDiv.style.padding = '10px';
subtitleDiv.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.5)';
subtitleDiv.style.color = 'white';
subtitleDiv.style.display = 'block';
subtitleDiv.style.borderRadius = '10px';

// 자막 헤더 추가
const subtitleHeader = document.createElement('div');
subtitleHeader.textContent = 'SSS (Smart Subtitle System)';
subtitleHeader.style.margin = '0';
subtitleHeader.style.fontSize = '16px';
subtitleHeader.style.fontWeight = 'bold';
subtitleHeader.style.marginBottom = '10px'; // 헤더 아래에 한 줄 공백 추가
subtitleDiv.appendChild(subtitleHeader);

// 자막 표시 영역 생성
const subtitleBox = document.createElement('div');
subtitleBox.style.width = '300px';
subtitleBox.style.height = '150px';
subtitleBox.style.backgroundColor = 'white';
subtitleBox.style.border = '1px solid black';
subtitleBox.style.marginBottom = '10px'; // 영역 아래에 여백 추가
subtitleBox.style.overflowY = 'auto'; // 세로 스크롤 가능하도록 설정
subtitleBox.style.overflowX = 'hidden'; // 가로 스크롤 숨김
subtitleDiv.appendChild(subtitleBox);

// 자막 텍스트 표시
const subtitleText = document.createElement('p');
subtitleText.id = 'subtitleText';
subtitleText.style.margin = '0';
subtitleText.style.padding = '10px'; // 내부 여백 추가
subtitleText.style.color = 'black'; // 텍스트 색상을 검정으로 설정
subtitleText.style.fontSize = '16px'; // 자막 텍스트 크기를 2배로 설정
subtitleBox.appendChild(subtitleText);

// 언어 선택 레이블 추가
const languageLabel = document.createElement('span');
languageLabel.textContent = 'Language: ';
languageLabel.style.marginRight = '5px';
languageLabel.style.fontSize = '20px'; // 글자 크기 조정
subtitleDiv.appendChild(languageLabel);

// 언어 선택 드롭다운 메뉴 생성
const languageSelect = document.createElement('select');
languageSelect.style.marginTop = '10px';
languageSelect.style.marginRight = '5px'; // 오른쪽 여백 추가
languageSelect.style.border = '1px solid black';
languageSelect.style.backgroundColor = 'white';
languageSelect.style.color = 'black';

// 옵션 추가
const koreanOption = document.createElement('option');
koreanOption.value = 'ko';
koreanOption.textContent = '한국어';
languageSelect.appendChild(koreanOption);

const englishOption = document.createElement('option');
englishOption.value = 'en';
englishOption.textContent = 'English';
languageSelect.appendChild(englishOption);

const chineseOption = document.createElement('option');
chineseOption.value = 'zh';
chineseOption.textContent = '中国话';
languageSelect.appendChild(chineseOption);

const japaneseOption = document.createElement('option');
japaneseOption.value = 'ja';
japaneseOption.textContent = 'にほんご';
languageSelect.appendChild(japaneseOption);

// 전역 변수로 현재 선택된 언어를 저장
let currentLanguage = 'ko';  // 기본 언어를 한국어로 설정
let isFirstLoad = true; // 자막이 처음 로드되는지 확인하는 변수

// 언어 선택 변경 이벤트
languageSelect.addEventListener('change', (event) => {
  currentLanguage = event.target.value;  // 선택된 언어로 업데이트
  fetchPythonSubtitles(currentLanguage);  // 언어 변경에 따른 자막 가져오기
  console.log(`Selected language: ${currentLanguage}`);
});

// 종료 버튼 생성
const closeButton = document.createElement('button');
closeButton.textContent = '종료';
closeButton.style.marginTop = '10px';
closeButton.style.border = '1px solid black';
closeButton.style.backgroundColor = 'gray';
closeButton.style.color = 'white';

// 종료 버튼 클릭 이벤트
closeButton.addEventListener('click', () => {
  subtitleDiv.style.display = 'none'; // 자막 창을 숨김
});

// 자막창 요소에 언어 선택과 종료 버튼 추가
subtitleDiv.appendChild(languageSelect);
subtitleDiv.appendChild(closeButton);

// 페이지에 추가
document.body.appendChild(subtitleDiv);

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
function fetchPythonSubtitles(language = 'ko') {  // 기본 언어를 한국어로 설정
  if (isFirstLoad) {
    displaySubtitles('Loading...');  // 자막을 처음 요청할 때만 "Loading..." 메시지 표시
  }
  
  fetch(`http://localhost:8080/get_subtitle?lang=${language}`)
    .then(response => response.text())
    .then(text => {
      displaySubtitles(text);  // 자막을 가져와서 표시
      isFirstLoad = false;  // 첫 로딩 이후로는 "Loading..." 메시지를 표시하지 않음
    })
    .catch(error => {
      console.error('Error fetching subtitles:', error);
      displaySubtitles('Error loading subtitles');  // 에러 발생 시 표시할 메시지
    });
}

// 현재 페이지의 URL을 가져와 서버에 전송
const currentUrl = window.location.href;
sendUrlToServer(currentUrl);

// 페이지 로드 시 자막 주기적으로 업데이트 시작
window.addEventListener('load', () => {
  fetchPythonSubtitles(currentLanguage);  // 처음에는 현재 선택된 언어로 자막 가져오기
  setInterval(() => fetchPythonSubtitles(currentLanguage), 5000); // 5초마다 현재 언어로 자막 가져오기
});
