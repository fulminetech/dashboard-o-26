const { Model, DataTypes } = require('sequelize')
const sequelize = require('./database')
// class User extends Model  { }

class Batch extends Model {
    // static classLevelMethod() {
    //     return 'foo';
    // }
    // instanceLevelMethod() {
    //     return 'bar';
    // }
    // getFullname() {
    //     return [this.firstname, this.lastname].join(' ');
    // }
}

Batch.init({
    batchname: {
        type: DataTypes.STRING
    },
    opertaor: {
        type: DataTypes.STRING
    },
    rotation: {
        type: DataTypes.INTEGER
    },
    recipe: {
        type: DataTypes.STRING
    }, 
}, {
    sequelize,
    modelName: 'batch',
    timestamps: true
})

module.exports = Batch;