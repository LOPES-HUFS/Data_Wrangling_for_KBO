# KBO_Data_Wrangling

이 스크립트는 KBO 자료를 수집하고 분석하고자 만들었습니다.

## 크롬 설치

크롬을 이용해서 자료를 수집하기 때문에 만약 크롬이 설치되어 있지 않다면 다음 링크를 참고하여 크롬을 설치합니다.

[Chrome 다운로드 및 설치 - 컴퓨터 - Google Chrome 고객센터](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=ko)

## `Pipenv` 설치

이 스크립트는 `Pipenv`로 python 가상환경을 구성해서 작성했습니다. 만약 `Pipenv`이 설치되어 있지 않으면, 다음 링크를 참고해서 `Pipenv`을 설치합니다.

https://pipenv.readthedocs.io/en/latest/

## 크롬드라이버 및 selenium 설치

크롬 브라우져를 조작하기 위해서는 크롬 드라이버가 필요합니다.  

### 윈도우에서 크롬드라이버 및 selenium 설치

먼저 아나콘다로 파이썬을 설치합니다. https://www.anaconda.com/download/#windows
파이썬을 설치한 이후 conda prompt에서 아래 코드를 통해 pipenv와 셀레니움을 설치합니다.
크롬드라이버는 http://chromedriver.chromium.org/downloads 링크에서 최신 버전을 다운 받아
이 프로젝트 폴더(pipfile.lock 파일이 있는 폴더)에 압축을 풀어주시면 됩니다. 

```
conda create -n "myenv" python=3.7.2
activate myenv
conda install -c conda-forge --name myenv selenium 
pip install pipenv
```

## 우분투에서 크롬 설치 및 selenium 설치

```
sudo apt-get install chromium-chromedriver
sudo apt-get install python3-selenium
```

참고로 `chromium-chromedriver`는 다음 위치에 설치됩니다.

/usr/lib/chromium-browser/chromedriver

## 맥에서 크롬드라이버 및 selenium 설치 

터미널에서 아래의 코드를 통해 selenium chromedriver를 설치하실 수 있습니다. 

```
brew cask install chromedriver
```

자세한 내용은 아래의 링크를 참고하여 셀레니움 크롬드라이버를 설치합니다.

http://www.epistemology.pe.kr/2018/09/25/1153


## 사용법

이 프로젝트를 포그합니다. 이 프로젝트의 깃허브를 클론하거나 다운로드 합니다. 
다운로드 된 압축파일을 압축해제 해줍니다. 맥이나 우분투의 경우 터미널에서
이 프로젝트 폴더로 갑니다. 윈도우 또한 마찬가지로 conda prompt에서 이 프로젝트 폴더로 이동해 줍니다.
그 이후 다음과 같은 코드로 가상환경을 시작합니다.

```
pipenv shell
pipenv install
```
