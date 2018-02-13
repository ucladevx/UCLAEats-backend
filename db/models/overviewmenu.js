'use strict';
const moment = require('moment');
module.exports = (Sequelize, DataTypes) => {
    const OverviewMenu = Sequelize.define('OverviewMenu', {
        overviewMenu: DataTypes.JSON,
        deletedAt: DataTypes.DATE,
        menuDate: DataTypes.DATEONLY,
    }, {
        classMethods: {
            associate: function(models) {
            // associations can be defined here
            }
        },
        paranoid:true,

    });

    // OverviewMenu.Create = function 

    // find a OverviewMenu by id
    OverviewMenu.findByID = function (id) {
        return this.findOne({ where :{ id } });
    }

    // date is a string with format YYYY-MM-DD
    OverviewMenu.findAllByDate = function(date) {
        return this.findAll({
            where: { 
                menuDate : date,
                // updatedAt: { 
                //     $between: [startDate, endDate],
                // }
            }
        });
    }

    // find all OverviewMenus Within a date range
    OverviewMenu.findAllByDateRange = function(startDate, endDate) {
        return this.findAll({
            where: {
                menuDate: {
                    $between: [startDate, endDate],
                }
            }
        });
    }

    OverviewMenu.Delete = function (id) {
        return this.destroy({
            where:{
                id: id,
            },
        });
    }

    OverviewMenu.prototype.getID = function () {
        return this.getDataValue('id');
    }

    OverviewMenu.prototype.getOverviewMenu = function () {
        return this.getDataValue('overviewMenu');
    }

    OverviewMenu.prototype.getDate = function () {
        return this.getDataValue('updatedAt');
    }

    return OverviewMenu;
};
