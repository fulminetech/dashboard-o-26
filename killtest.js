const { exec } = require('child_process');
const killchrome = "killall chromium-browser"

exec(killchrome, (err, stdout, stderr) => {
    console.log(`[ RESTARTING ${stdout} ]`);
    console.log(`${stdout}`);
});