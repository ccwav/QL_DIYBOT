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
//路由器重拨号命令
let strcommond="service restart_wan"

!(async() => {
await conn.on('ready', function () {	
    conn.exec(strcommond, function (err, stream) {
        if (err)
            throw err;
        stream.on('close', function (code, signal) {
            conn.end();
        }).on('data', function (data) {						
            console.log("重拨结果:"+":"+data.toString().replace("\n","").replace("Done","成功"));
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