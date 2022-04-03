var Client = require('ssh2').Client;
var conn = new Client();
var strreturn=""
//路由器ip
var RouterIP='192.168.1.1'
//ssh端口
var RouterSSHProt=22
//ssh用户名密码
var RouterSSHUser="ccwav"
var RouterSSHPsw="AABBCCDD"

!(async() => {
await conn.on('ready', function () {
	var intseq=0;
	var strTemp="设备名称|外网地址|内网地址|内存信息";
	var sstrTitle=strTemp.split('|');
    conn.exec("nvram get computer_name&&curl ip.sb&&nvram get lan_ipaddr&&top -n 1 -b |grep ^Mem", function (err, stream) {
        if (err)
            throw err;
        stream.on('close', function (code, signal) {
            conn.end();
        }).on('data', function (data) {						
            console.log(sstrTitle[intseq]+":"+data.toString().replace("\n","").replace("Mem: ",""));
			intseq++;
        }).stderr.on('data', function (data) {
            console.log('STDERR: ' + data);
        });
    });
}).connect({
    host: RouterIP,
    port: RouterSSHProt,
    username: RouterSSHUser,
    password: RouterSSHPsw
});


})()