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

  

