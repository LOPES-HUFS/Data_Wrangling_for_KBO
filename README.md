# KBO_Data_Wrangling

이 스크립트는 KBO 자료를 수집하고 분석하고자 만들었습니다.

## 크롬 설치

크롬을 이용해서 자료를 수집하기 때문에 만약 크롬이 설치되어 있지 않다면 다음 링크를 참고하여 크롬을 설치합니다.

[Chrome 다운로드 및 설치 - 컴퓨터 - Google Chrome 고객센터](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=ko)

## `Pipenv` 설치

이 스크립트는 `Pipenv`로 python 가상환경을 구성해서 작성했습니다. 만약 `Pipenv`이 설치되어 있지 않으면, 다음 링크를 참고해서 `Pipenv`을 설치합니다.

https://pipenv.readthedocs.io/en/latest/

## 크롬드라이버 및 selenium 설치

크롬 브라우져를 조작하기 위해서는 크롬 드라이버가 필요합니다. 또한  

### 윈도우에서 크롬드라이버 및 selenium 설치

먼저 아나콘다로 파이썬을 설치합니다. https://www.anaconda.com/download/#windows
파이썬을 설치한 이후 conda prompt에서 아래 코드를 통해 pipenv와 셀레니움 크롬드라이버를 설치합니다.

```
conda create -n "myenv" python=3.7.2
activate myenv
conda install -c conda-forge --name myenv selenium 
conda install -c clinicalgraphics selenium-chromedriver
pip install pipenv
```

### 우분투에서 크롬 설치 및 selenium 설치

```
sudo apt-get install chromium-chromedriver
sudo apt-get install python3-selenium
```

참고로 `chromium-chromedriver`는 다음 위치에 설치됩니다.

/usr/lib/chromium-browser/chromedriver

### 맥에서 크롬드라이버 및 selenium 설치

맥에서 크롬드라이버를 쉽게 설치하는 방법은 [Homebrew](https://brew.sh/index_ko)으로 설치하는 것입니다. [Homebrew](https://brew.sh/index_ko)에 가서 글 내용을 확인하신 다음 Homebrew를 설치합니다. 홈부르의 명령어인 `brew`을 이용해서 터미널에서 아래처럼 입력하시면 selenium chromedriver를 설치하실 수 있습니다.

```
brew cask install chromedriver
```

조금더 자세한 내용은 아래의 링크를 참고하세요.

http://www.epistemology.pe.kr/2018/09/25/1153


## 사용법

이 프로젝트를 포그합니다. 이 프로젝트 폴더로 갑니다.
그런 다음 다음과 같이 가상환경을 시작합니다.

```
pipenv shell
pipenv install
```
