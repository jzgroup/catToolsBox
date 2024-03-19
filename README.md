# catToolsBox
猫咪工具箱
![cankao.png](images%2Fcankao.png)
### 使用方式

##### 1.APP启动(目前仅支持MAC)
路径:dist/猫咪工具箱.app \
（win的话，打包一下就好了，当然（可能要处理下路径问题，自启动问题等几个兼容问题））


##### 2.命令行启动

添加第三方库
```shell
pip install - r requirements.txt
```
运行main文件
```shell
python3 main.py
```

### 打包
不管是win还是mac，使用命令就可以，配置在spec都配置好了
```shell
pyinstaller main.spec 
```

### 功能介绍
不介绍，有空在介绍