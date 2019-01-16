# python_chatbot
python chatbot サンプル

## 推奨環境
* Python 3.6
* MySql 5.7

## 設定コマンド

### 必要なライブラリのインストール
```
pip install django==1.11.2
pip install pandas
pip install janome
pip install xlwt
```

### DB初期設定
```
create database chatbotdemo;  
create user 'demochat'@'localhost' identified by 'demochat';  
grant all on chatbotdemo.* to 'demochat'@'localhost' identified by 'demochat'; 
```
↓  
`manage.py migrate`

### 起動コマンド
`manage.py runserver 0.0.0.0:8000`


### アクセスURL
http://localhost:8000/demo/demochat/

--------------

## 動作に必要なファイル

◯ チャットボットのアイコン用に下記ファイルをローカルに配置する  
```
demo/static/img/ico_user.jpg  
demo/static/img/ico_robot.jpg  
demo/static/img/ico_send.jpg  
```
