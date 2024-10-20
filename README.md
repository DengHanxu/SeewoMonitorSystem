# SeewoMonitorSystem

由于班主任时不时通过希沃的巡课系统（俗称监控）来查看上课情况，这对学生来说当然不是一个好消息。因此，本反监控系统就是监控希沃，并在有异常情况时立即报告。

> [!CAUTION]
>
> 本项目最后更新于2024年6月，希沃管家相关行为机制可能已经更改，请在安全环境自行测试项目是否任然有效
>
> 在2024年5月左右，希沃管家绑定学校需要管理员密码验证，导致我虚拟机几乎失效

> [!WARNING]
>
> 由于本人已于2024年6月高中毕业，后续缺少测试环境，因此本项目将停止更新。
> 
> 在我毕业大约半个月前，希沃在机缘巧合的情况下已恰好让这个方法失效。
> 至少我认为是巧合，本项目还不至于被曾经干出本机明文存储管理员密码MD5值还什么都不加的开发团队注意到。
> 
> 具体表现为，那次希沃的更新会保持`media_capture.exe`在后台运行，由于连续1分钟网络上传流量低被`RubbishCleaner.exe`终止进程。
> 新版希沃管家发现`media_capture.exe`不在了就去启动它，导致红点常驻和不停播放声音。
>
> 然而有趣的是，那次希沃更新虽然让本项目失效，但却让我[另一个项目](https://github.com/DengHanxu/BanSeewo)活了过来，因为那次更新后希沃对注册表的防范减弱了。
> 所以现在能够直接禁用希沃管家及其附属程序。


# 原理

希沃巡课系统主要依赖3个程序，`media_capture.exe`，`screenCapture.exe`，`rtcRemoteDesktop.exe`，而`media_capture.exe`就是负责获取摄像头数据的。
因此，不断查询当前进程列表并检查是否有`media_capture`就能大致确定（[这种方法并不完全准确](#局限性)）是否有老师正在看监控。

# 主要构成
- [SeewoMonitor](#SeewoMonitor)
- [Sound](#Sound)
- [RubbishCleaner](#RubbishCleaner)

## SeewoMonitor

SeewoMonitor目前有以下两个版本，负责监控进程并以指示块的形式报告情况

### SeewoMonitor
这是第一个版本，以大约`1次/秒`的速度检测`media_capture.exe`。
当检测到`media_capture.exe`在运行时，就认为监控系统正在运行，并在屏幕上方正中偏右2像素的位置（这其实是个失误，原计划是上方正中间）显示一个4x4像素的红色方块。
当`media_capture.exe`结束运行时，就认为本次监控结束，红色方块消失。

### SeewoMonitor2
  

这是`SeewoMonitor`升级版，这个版本除了检测在[原理](#原理)中提到的三个程序之外，还会监控上传网速，以大约`0.5轮/秒`的速度检测。
下图解释了SeewoMonitor2管理的4个色块的位置和触发条件。
![](docs/SeewoMonitor2Example.png)

## Sound

监控`media_capture.exe`并且播放声音来告知情况。
当开始运行时，播放Windows硬件插入的系统提示音；当结束运行时，播放Windows硬件拔出的系统提示音。
为了确保提示音能够播放，该程序会检测系统音量，如果系统音量低于设定阈值（默认`-10.5dB`），就先拉高系统音量到阈值再播放提示音，提示音播放完成再调回系统原音量；
如果当前系统音量大于设定阈值，就不改变音量。
但是，无论哪种情况，该程序都会解除静音并且不会恢复静音。

## RubbishCleaner

监控[原理](#原理)中提到的3个程序和上传网速，如果上传网速低持续1分钟，就尝试终止之前提到的3个程序。
监控程序不会主动结束进程，因此需要本程序

>[!IMPORTANT]
>此程序必须要能够成功调用`Nsudo.exe`才能发挥作用（建议加环境变量或者直接丢到System32里），因为需要提权。如果你有其他提权方案，自行更改此程序源码。
>有关`Nsudo.exe`，请参阅 [Nsudo](https://github.com/M2TeamArchived/NSudo)

# 使用本项目
## 打包成exe

1. 运行`pip.bat`安装依赖库
2. 使用`pyinstaller SeewoMonitor2.py -F -w`命令打包

> [!CAUTION]
> 使用`pyinstaller`打包的exe会被`WindowsDeferder`等报毒为特洛伊木马，程序本身并没有病毒
> 
> 要使用`RubbishCleaner.exe`，请注意`Nsudo.exe`

## 添加自启动（可选）

> [!IMPORTANT]
> 执行此操作前请确保`冰点还原`处于关闭状态，打开`explorer`，如果`C`盘是下图所示状态，则表明`C`盘被冻结，添加的自启动重启就会失效。
> 
> ![](docs/FreezedC.png)
> 
> 如果`冰点还原`是开启状态，你需要先关闭`冰点还原`。

具体如何添加自启动自行搜索引擎搜索。

# 局限性

[原理](#原理)中提到的3个程序有时候会自己启动，导致误报。不过1分钟后就会被[RubbishCleaner](#RubbishCleaner)清除。
目前尚不清楚相关机制。
