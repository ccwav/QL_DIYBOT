# QL_DIYBOT
写点有用且好玩的bot模块

# 注意事项: 
	
	机器人模块的使用环境是青龙bot + diybot,V4 + diybot
	
# 1.jbot\diy\cxjc.py 和 jbot\diy\cxjc_kill.py

	作用: 发送/cx 给机器人查询现在执行的任务列表，点击前面的链接即可强制结束进程.
	安装: 文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy),重启机器人即可生效.
	
# 2.jbot\diy\Router.py 
	
	作用: 梅林路由器专用，发送/routerinfo 给机器人查询路由器ip等信息
	安装: 1.Routerinfo.js填上路由器相关信息,并将文件放到青龙
		  2.Router.py第17行的文件路径(默认是/ql/scripts/),安装nodejs依赖ssh2
		  3.将修改后的Router.py文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy)
		  4.重启机器人即可生效		 
	
# 3.jbot\diy\RouterResetIP.py

	作用: 梅林路由器专用，发送/routerip 给机器人通知路由器重新拨号换IP.
	安装: 1.修改RouterResetIP.js填上路由器相关信息,并将文件放到青龙
		  2.修改RouterResetIP.py第17行的文件路径(默认是/ql/scripts/),安装nodejs依赖ssh2
		  3.将修改后的RouterResetIP.py文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy)
		  4.重启机器人即可生效

# 4.jbot\diy\Bean_ccwav.py

	(甘露殿狗哥测试了V4可以正常使用........)
	作用: 调用资产查询脚本查询对应CK的资产信息. 支持/ccbean 和 /ccbean CK序号 两种格式.
	安装: 1.修改Bean_ccwav.py第69行的bot_jd_bean_change.js路径，这个文件我放在Script里面了
		  2.文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy),重启机器人即可生效.
		  3.增加bot_jd_bean_change_QL.js，显示青龙备注名字,青龙专用
		  
	特殊变量: BEANCHANGE_BOTDISABLELIST 可以关闭某些查询的项目提高速度,按需删减
	export BEANCHANGE_BOTDISABLELIST="过期京豆&汪汪赛跑&查优惠券&汪汪乐园&京东赚赚&京东秒杀&东东农场&极速金币&京喜牧场&京喜工厂&京东工厂&领现金&喜豆查询&金融养猪&东东萌宠"

# 5.jbot\user\ccbean_Global.py (全局版本)
	
	Bean_ccwav.py的全局版本，tg任何群使用cb CK序号或cb ptpin两种格式查询资产.
	安装: 1.ccbean_Global.py第41行的bot_jd_bean_change.js路径，这个文件我放在QLScript2仓库了
		  2.文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.
		  3.增加bot_jd_bean_change_QL.js，显示青龙备注名字,青龙专用
		  
	特殊变量: BEANCHANGE_BOTDISABLELIST 可以关闭某些查询的项目提高速度,按需删减
	export BEANCHANGE_BOTDISABLELIST="过期京豆&查优惠券&汪汪乐园&京东赚赚&京东秒杀&东东农场&极速金币&京喜牧场&京喜工厂&京东工厂&领现金&喜豆查询&金融养猪&东东萌宠"	 
	
# 6.jbot\user\bean_Global.py (全局版本)
	
	Bean.py的全局版本，bb CK序号查询资产.
	安装: 文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.

# 7.jbot\user\chart_Global.py (全局版本)
	
	chart.py的全局版本，bc CK序号查询资产.
	安装: 文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.
		  
# 8.jbot\bot\bean.py

	作用: 增强原有的/bean,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(有些人需要放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.

# 9.jbot\bot\chart.py

	作用: 增强原有的/chart,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(有些人需要放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.
	
# 10.jbot\diy\CheckCK.py (青龙专用)

	作用: 导出现有的CK信息,命令是/cck
	安装: 1.CheckCK.py第20行的文件路径	 
		  2.将修改后的CheckCK.py文件放于ql\jbot\diy(有些人需要放在ql\repo\dockerbot\jbot\diy)
		  3.重启机器人即可生效
		  
# 11.jbot\user\beaninfo_Global.py (全局版本)	
	bd CK序号查询当日资产详情，
	安装: 1.修改beaninfo_Global.py第40行的bot_jd_bean_info.js路径，这个文件我放在QLScript2仓库了
		  2.文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.
		  3.增加bot_jd_bean_info_QL.js，显示青龙备注名字,青龙专用
		  
	特殊变量: export BOTShowTopNum="10" 限制显示的查询内容，隐藏X京豆以下信息


# 12.一些原版的bug修复:
	jbot\utils.py: 修复user文件夹脚本载入时login.py没有优先载入导致部分全局命令不生效的问题.
	jbot\user\reply_msg.py: 修复re命令重复发两次的问题
	
# 13.jbot\user\jxjd_Global.py (全局版本)	
	解析京东 京喜 京东极速版口令为网址,用法是jx 口令 或者 选中他人口令回复jx
	安装: 文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.

# 14.jbot\user\weather_Global.py (全局版本)	
	查询天气，例如 深圳天气
	安装: 文件放于ql\jbot\user(有些人需要放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.
				
