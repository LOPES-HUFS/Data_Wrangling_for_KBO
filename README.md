# KBO_Data_Wrangling
KBO 자료를 수집하고 분석합니다.

## 필요한 패키지

Pipenv로 가상환경을 구성하고 있습니다. 다음 링크를 참고해서 Pipenv을 설치합니다.

https://pipenv.readthedocs.io/en/latest/

## 윈도우에서 크롬드라이버 및 selenium 설치

먼저 아나콘다로 파이썬을 설치합니다. https://www.anaconda.com/download/#windows
파이썬을 설치한 이후 conda prompt에서 아래 코드를 통해 pipenv와 셀레니움 크롬드라이버를 설치합니다.

```
conda create -n "myenv" python=3.7.2
activate myenv
conda install -c conda-forge --name myenv selenium 
conda install -c clinicalgraphics selenium-chromedriver
pip install pipenv
```

## 우분투에서 크롬 설치 및 selenium 설치

```
sudo apt-get install chromium-chromedriver
sudo apt-get install python3-selenium
```

다음 위치에 설치됩니다.
/usr/lib/chromium-browser/chromedriver

## 맥에서 크롬드라이버 및 selenium 설치 

터미널에서 아래의 코드를 통해 selenium chromedriver를 설치하실 수 있습니다. 

```
brew cask install chromedriver
```

자세한 내용은 아래의 링크를 참고하여 셀레니움 크롬드라이버를 설치합니다.

http://www.epistemology.pe.kr/2018/09/25/1153


## 사용법

이 프로젝트를 포그합니다. 이 프로젝트 폴더로 갑니다.
그런 다음 다음과 같이 가상환경을 시작합니다.

```
pipenv shell
pipenv install
```
