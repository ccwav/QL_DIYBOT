# QL_DIYBOT
写点有用且好玩的bot模块

# 注意事项: 
	
	机器人模块的使用环境是青龙bot + diybot,V4 + diybot
	配置文件统一是ql\config\ccbotSetting.json,文件库里有,说明在配置文件里.	
	
# 1.jbot\diy\cxjc.py

	作用: 发送/cx 给机器人查询现在执行的任务列表，点击前面的链接即可强制结束进程.
	安装: 文件放于ql\jbot\diy,重启机器人即可生效.
	
# 2.jbot\diy\Router.py 
	
	作用: 梅林路由器专用，发送/routerinfo 给机器人查询路由器ip等信息
		  发送/routerip 给机器人通知路由器重新拨号换IP.
	安装: 1.Routerinfo.js RouterResetIP.js填上路由器相关信息,并将文件放到青龙,修改配置文件的文件地址.
		  2.安装nodejs依赖ssh2		  
		  3.重启机器人即可生效	

# 3.jbot\diy\ccbean.py (以前的Bean_ccwav.py记得删除)

	(甘露殿狗哥测试了V4可以正常使用........)
	作用: 调用资产查询脚本查询对应CK的资产信息. 支持/ccbean 和 /ccbean CK序号 两种格式.
	安装: 文件放于ql\jbot\diy,修改配置文件的文件地址,重启机器人即可生效.

# 5.jbot\user\ccbean_Global.py (全局版本)
	
	全局版本，tg任何群使用cb CK序号或cb ptpin两种格式查询资产.
	安装: 文件放于ql\jbot\user,修改配置文件的文件地址,重启机器人即可生效.
	
# 6.jbot\user\bean_Global.py (全局版本)
	
	Bean.py的全局版本，bb CK序号查询资产.
	安装: 文件放于ql\jbot\user,重启机器人即可生效.

# 7.jbot\user\chart_Global.py (全局版本)
	
	chart.py的全局版本，bc CK序号查询资产.
	安装: 文件放于ql\jbot\user,重启机器人即可生效.
		  
# 8.jbot\bot\bean.py

	作用: 增强原有的/bean,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(同时放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.

# 9.jbot\bot\chart.py

	作用: 增强原有的/chart,不带序号时弹出按钮
	安装: 文件放于ql\jbot\bot(同时放在ql\repo\dockerbot\jbot\bot),重启机器人即可生效.
	
# 10.jbot\diy\CheckCK.py (青龙专用)

	作用: 导出现有的CK信息,命令是/cck
	安装: 1.CheckCK.py第20行的文件路径	 
		  2.将修改后的CheckCK.py文件放于ql\jbot\diy(同时放在ql\repo\dockerbot\jbot\diy)
		  3.重启机器人即可生效
		  
# 11.jbot\user\beaninfo_Global.py (全局版本)	
	bd CK序号查询当日资产详情，
	安装: 文件放于ql\jbot\user,修改配置文件的文件地址,重启机器人即可生效.

# 12.一些原版的bug修复:
	jbot\utils.py: 修复user文件夹脚本载入时login.py没有优先载入导致部分全局命令不生效的问题.
	安装: 文件放于ql\jbot\(同时放在ql\repo\dockerbot\jbot\),重启机器人即可生效.
	
# 13.jbot\user\jxjd_Global.py (全局版本)	
	解析京东 京喜 京东极速版口令为网址,用法是jx 口令 或者 选中他人口令回复jx
	安装: 文件放于ql\jbot\user(同时放在ql\repo\dockerbot\jbot\user),重启机器人即可生效.

# 14.jbot\user\weather_Global.py (全局版本)	
	查询天气，例如 深圳天气
	安装: 文件放于ql\jbot\user,修改配置文件的文件地址,重启机器人即可生效.
	
# 15.jbot\bot\getfile.py 	
	安装: 文件放于ql\jbot\bot(同时放在ql\repo\dockerbot\jbot\bot),修改配置文件的文件地址,重启机器人即可生效.
	
# 16.jbot\user\jupai.py
	发送举牌小人图片，格式: jp 内容，或者对内容回复jp. 
	安装: 文件放于ql\jbot\user,重启机器人即可生效.
	
				
				
