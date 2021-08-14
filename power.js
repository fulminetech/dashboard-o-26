const express = require('express')
const app = express()
const { exec } = require('child_process');
var cors = require('cors')
var path = require('path');
var ks = require('node-key-sender');

const restart1Command = "/opt/dashboard-o-26/restart.sh"

app.use(cors({ origin: "*" }));

const shutdown = "gnome-session-quit --power-off"
const reboot = "gnome-session-quit --reboot"
const shutdown_force = "gnome-session-quit --power-off --force"
const killchrome = "ps aux | grep -i chromium | awk {'print $2'} | xargs kill -9"

var count

function restartserver(arg) {
    exec(arg, (err, stdout, stderr) => {
        // handle err if you like!
        console.log(`[ RESTARTING ${stdout} ]`);
        console.log(`[ Error: ${err} ${stderr} ]`);
    });
}

app.get("/restart/:param", (req, res) => {

    console.log(count)
    if(count > 300) {
        restartserver(shutdown_force)
    }

    const a = req.params.param;
    a == "reboot" ? restartserver(reboot) : reboot
    a == "shutdown" ? restartserver(shutdown) : shutdown
    a == "main_5000" ? count++ && restartprodmodbus() : shutdown
});

function restartprodmodbus() {
    console.log(`[ RESTARTING: ${restart1Command} ]`);
    
    exec(restart1Command, (err, stdout, stderr) => {
        console.log(`${stdout}`);
    });
}

app.get("/desktop", (req, res) => {
    // ks.sendCombination(['control', 'shift', 'v']);
    // ks.sendCombination(['alt', 'tab']);
    // ks.sendCombination(['control','d']);
    ks.sendCombination(['control', 'alt', 'down']);
    // ks.sendCombination(['control','alt', 'down']);
    // ks.sendCombination(['control','alt', 'down']);
    res.sendFile(path.join(__dirname + "/html_/login.html"));
});

const server = app.listen(3001, () => console.log('Server ready'))