@echo off
echo �x�ɓ͂��쐬���J�n���܂�
powershell -NoProfile -ExecutionPolicy Unrestricted C:/Program` Files/WORK/chatbot_demo/tools/excel_test.ps1 %1 %2 %3 >> .\excel_action.log 2>&1
echo �x�ɓ͂��쐬���I�����܂��B
exit