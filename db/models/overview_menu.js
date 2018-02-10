'use strict';
module.exports = (Sequelize, DataTypes) => {
    const OverviewMenu = Sequelize.define('OverviewMenu', {
        overviewMenu: DataTypes.JSON,
        deletedAt: DataTypes.DATE,
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

    // find all OverviewMenus Within a date range
    OverviewMenu.findByDateRange = function(startDate, endDate) {
        return this.findAll({
            where: {
                updatedAt: {
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
