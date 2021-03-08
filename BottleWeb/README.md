### 中期报告

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

