# QL_DIYBOT
写点有用且好玩的bot模块

# 注意事项: 
	
	机器人模块的使用环境是青龙bot + diybot
	
# 1.cxjc.py 和 cxjc_kill.py

	作用: 发送/cx 给机器人查询现在执行的任务列表，点击前面的链接即可强制结束进程.
	安装: 文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy),重启机器人即可生效.
	
# 2.Router.py 
	
	作用: 梅林路由器专用，发送/routerinfo 给机器人查询路由器ip等信息
	安装: 1.Routerinfo.js填上路由器相关信息,并将文件放到青龙
		  2.Router.py第17行的文件路径(默认是/ql/scripts/)
		  3.将修改后的Router.py文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy)
		  4.重启机器人即可生效		 
	
# 3.RouterResetIP.py

	作用: 梅林路由器专用，发送/routerip 给机器人通知路由器重新拨号换IP.
	安装: 1.修改RouterResetIP.js填上路由器相关信息,并将文件放到青龙
		  2.修改RouterResetIP.py第17行的文件路径(默认是/ql/scripts/)
		  3.将修改后的RouterResetIP.py文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy)
		  4.重启机器人即可生效

# 4.Bean_ccwav.py

	作用: 调用资产查询脚本查询对应CK的资产信息. 支持/ccbean 和 /ccbean CK序号 两种格式.
	安装: 1.修改Bean_ccwav.py第69行的bot_jd_bean_change.js路径，这个文件我放在QLScript2仓库了
		  2.文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy),重启机器人即可生效.
		  
	特殊变量: BEANCHANGE_BOTDISABLELIST 可以关闭某些查询的项目提高速度	
	export BEANCHANGE_BOTDISABLELIST="过期京豆&查优惠券&汪汪乐园&京东赚赚&京东秒杀&东东农场&极速金币&京喜牧场&京喜工厂&京东工厂&领现金&喜豆查询&金融养猪&东东萌宠"
	
# 5.bean.py

	作用: 增强原有的/bean,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(有些人需要放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.

# 6.chart.py

	作用: 增强原有的/chart,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(有些人需要放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.