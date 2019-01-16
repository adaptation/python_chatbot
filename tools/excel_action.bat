@echo off
echo 休暇届け作成を開始します
powershell -NoProfile -ExecutionPolicy Unrestricted C:/Program` Files/WORK/chatbot_demo/tools/excel_test.ps1 %1 %2 %3 >> .\excel_action.log 2>&1
echo 休暇届け作成を終了します。
exit