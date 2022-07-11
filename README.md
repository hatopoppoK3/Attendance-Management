# Attendance-Management
勤怠管理に関する趣味アプリケーション.

## 概要
勤怠時間を打刻するWebアプリケーション.  
開発言語はPythonとし, フレームワークとしてFlaskを採用した.  
データベースについてはGoogle Cloud Datastoreを採用し, Google App Engineにデプロイする.

## 開発環境
* Windows Subsystem for Linux 2 Ubuntu 18.04
* Python 3.7.4
* Flask 2.0.1

## 動作環境
* Google App Engine Standard for Python
* Google Cloud Datastore

## 命名規則
flaskでアプリケーションを作るときはHTMLと埋め込み変数の命名規則で悩んでいる気がするので、ここで明示.
1. Pythonファイル
   * 関数名 : Snake case
   * ローカル変数 : Snake case
   * グローバル変数 : Screaming snake case
   * クラス名 : Upper camel case
   * 埋め込み変数 : Lower camel case
2. Javascriptファイル
   * 関数名 : Lower camel case
   * ローカル変数 : Lower camel case
   * グローバル変数 : Screaming snake case
3. HTMLファイル
   * id名 : Lower camel case
   * クラス名 : Kebab case
   * name : Lower camel case
   * 埋め込み変数 : Lower camel case

## アラートのカテゴリについて
* info : ログイン等の更新動作が正常に完了した場合
* success : 新規作成・削除等の動作が正常に完了した場合
* warning : ログイン情報等に誤りがあり完了しなかった場合
* alert : 動作が正常終了しなかった場合

## 値のフォーマットについて
* sessionID : 任意長のの16進数
* 日付(datetime) : YYYY-mm-dd HH:MM:SS:ffffff
* 

