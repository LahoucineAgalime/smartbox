数据库：mysql  redis

1、安装依赖，见requirements.txt
        2、创建mysql数据库：monitor，字符集：utf8mb4,排序规则：utf8mb4_general_ci
		3、修改smartbox/smartbox/settings.py 中的数据库信息
		4、进入smartbox路径，输入python manage.py makemigrations;python manage.py migrate创建数据表
		5、双击start.bat文件启动服务
		6、打开localhost:8000/admin配置摄像头信息
		7、打开localhost:8000查看页面

