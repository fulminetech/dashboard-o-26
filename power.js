const express = require('express')
const app = express()
const { exec } = require('child_process');
var ks = require('node-key-sender');

app.use(cors({ origin: "*" }));

const shutdown = "gnome-session-quit --power-off"
const reboot = "gnome-session-quit --reboot"

function restartserver(arg) {
    exec(arg, (err, stdout, stderr) => {
        // handle err if you like!
        console.log(`[ RESTARTING ${stdout} ]`);
        console.log(`[ Error: ${err} ${stderr} ]`);
    });
}

app.get("/restart/:param", (req, res) => {
    const a = req.params.param;
    a == "stats" ? restartserver(restartstats) : restartstats
    a == "compression" ? restartserver(restartcompression) : restartcompression
    a == "raw" ? restartserver(restartraw) : restartraw
    a == "reboot" ? restartserver(reboot) : reboot
    a == "shutdown" ? restartserver(shutdown) : shutdown
});

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