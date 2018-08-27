# Robocall Server Installation Instructions
## Prepare
* 電話伺服器主機+HDMI螢幕+mouse+keyboard
* 一條兩芯電話線(A端是RJ11接頭, B端是2-pin 裸線)+電話線打線工具
* 事先安裝好 robocall_server & anydesk

## Instructions
* 網路廠商設定publicIP:2022 map to staticIP:22 
* 聯絡電話負責人, 找到電話線在端子板上位置
* 電話線B端插入到端子板上指定位置(利用打線工具)
* 電話線A端插入伺服器主機 Digium card指定 port
* 安裝AC電源線
* 安裝HDMI螢幕
* 放置主機到機櫃內
* 電源開機
* 設定static IP
* 測試打電話功能 (http://staticIP:8080/robocall?roomId=xxxx&pw=xxxx)
* 測試Anydesk功能
* 取回mouse&keyboard
* 關閉機櫃
* [提醒] 記得修改naviCenter::elevator_pc.py#13 phoneServerIP

