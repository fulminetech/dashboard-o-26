
const sequelize = require('./database')
const User = require('./Users')

sequelize.sync().then(() => console.log('db ready'))

var CronJob = require('cron').CronJob;
// var job = new CronJob('40 11 * * *', function () {
var job = new CronJob('0 12 * * *', function () {

    reduceexpiry()
    console.log('You will see this message every day at 12pm');
}, null, true, 'Asia/Kolkata');
job.start();


// var users
async function reduceexpiry() {
    const users = await User.findAll();
    const userno = users.length
    // console.log(userno)

    var usersjson = JSON.stringify(users)
    var usersjson1 = JSON.parse(usersjson)

    for (let i = 0; i < userno; i++){
        // console.log(usersjson1[i])
        const requestedid = usersjson1[i].id
        console.log(requestedid)
        // console.log(usersjson1[i].expiry)
        if (usersjson1[i].expiry > 0) {
            console.log(usersjson1[i].expiry)
            const userz = await User.findOne({ where: { id: requestedid } });
            userz.expiry = parseInt(usersjson1[i].expiry-1)
            await userz.save() 
        }        
    }
}