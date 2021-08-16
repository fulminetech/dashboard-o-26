const { exec } = require('child_process');
const killchrome = "killall chromium-browser"
const restart1Command = "/opt/dashboard-o-26/killall.sh"

exec(killchrome, (err, stdout, stderr) => {
    console.log(`[ RESTARTING ${stdout} ]`);
    console.log(`${stdout}`);
});