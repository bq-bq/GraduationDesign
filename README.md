#### 毕业设计 

##### 项目目标

- 实现一个可移植的Python项目，目的是在Android系统中能够使用Python项目来获取并且修改后台数据。使得项目管理员能够在没有PC的情况下能够方便地处理后端数据。
- 使用或者参考Android中的工具QPython/QPython3进行Python项目的编译

##### 项目计划

|   时间    |                             计划                             |
| :-------: | :----------------------------------------------------------: |
| 1.18-1.22 | 阅读Python中的[Bottle教程](http://www.bottlepy.org/docs/dev/index.html)，通过Bottle进行网页编写 |
| 1.23-2.11 | 查看[QPython及其相关教程](https://github.com/qpython-android/qpython)，了解Android平台上使用Python项目的方法 |
|   2.12-   |      在Android平台中调用QPython进行项目编写，进行Coding      |

##### 目前进度

+ 阅读相关文档，对工具进行熟悉
+ 在Android平台中尝试使用QPython运行简易的Python项目
+ 使用Bottle进行简易的Demo编写，熟悉bottle框架的使用



##### 遇到问题

- QPython是一个使用Java编写的一个Android项目，虽然可以支持部分的Python库的使用，例如：numpy，bottle等，但是由于底层是使用Java，所以大部分的使用C，C++实现的Python库比较难进行使用

- 因为QPython是一个现成的安卓APP，所以需要较长时间查看其源码，理清其底部逻辑

  

***

### 中期报告 3.8

#### 目前已经完成的工作

- 实现了本地PyWeb服务器的编写

- 使用了bootstrap框架（便于进行网页样式的修改），编写简易的服务器主页

- 在PC端和Android端均进行了服务器的编译和运行

- 服务器外观如下：

  - PC端服务器：

    <img src=".\src\pc_test.png" alt="PC端服务器" style="zoom:40%;" />

  - 移动端服务器

    <img src=".\src\android_test.png" alt="Android端服务器" style="zoom:40%;" />

#### 后期拟完成的研究工作

- 在该项目中，增加访问数据库的功能（因为移动端比较难以开启数据库，主要对远程数据库进行读取）
- 完善项目以及页面的编写

#### 存在问题及其解决方法

- 因为移动端可以使用的Python库较少，底层使用C/C++的库大多用不了，需要选择合适，轻便的Python库进行使用。
- 在移动端使用QPython时，经常会出现无法找到文件的情况，每次都需要将文件/文件夹复制到QPython的根目录下才可以正常地运行。



#### 运行方法

- PC端 ：

  在BottleWeb目录下运行下列指令，即可在localhost的8888端口打开该服务器

  ```
  py main.py
  ```

- Android端：

  - 将static文件夹和views文件夹移动到QPython文件的根目录下，如下图：
    	<img src=".\src\sample.png" style="zoom:40%;" />

  - 然后打开main.py文件，在QPython中进行运行，如下图：

    <img src=".\src\run.png" style="zoom:40%;" />

------

### 中期报告 4.1

#### 目前已完成的工作

- 因为原来HW_2020_09的servo中core使用的pyramid，waitress，container库在QPython均无法使用，修改为website中的core2。并且进行一部分函数的修改，使得服务器能够正常地运行。
- 在安卓系统中，使用QPython进行服务器的搭建以及尝试运行。（目前可以在安卓系统中打开服务器并且在pc端获取该页面）

#### 后期拟完成的研究工作

- 相关的数据库的操作
- 进行毕业论文的编写

#### 运行示例

- Android平台的运行

  <img src=".\src\android_run.png" style="zoom:50%;" />

- Android本地的网页

  <img src=".\src\android_website.png" style="zoom:50%;" />

- PC端获取的网页

  <img src=".\src\pc_website.png" style="zoom:50%;" />