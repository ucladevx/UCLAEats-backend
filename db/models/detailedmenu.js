'use strict';
module.exports = (sequelize, DataTypes) => {
    var DetailedMenu = sequelize.define('DetailedMenu', {
        detailedMenu: DataTypes.JSON,
        deletedAt: DataTypes.DATE
    }, {
        classMethods: {
            associate: function(models) {
                // associations can be defined here
            }
        },
        paranoid:true,
    });

    // find a DetailedMenu by id
    DetailedMenu.findByID = function (id) {
        return this.findOne({ where :{ id } });
    }

    // find all DetailedMenus Within a date range
    DetailedMenu.findByDateRange = function(startDate, endDate) {
        return this.findAll({
            where: {
                updatedAt: {
                    $between: [startDate, endDate],
                }
            }
        });
    }

    DetailedMenu.Delete = function (id) {
        return this.destroy({
            where:{
                id: id,
            },
        });
    }

    DetailedMenu.prototype.getID = function () {
        return this.getDataValue('id');
    }

    DetailedMenu.prototype.getDetailedMenu = function () {
        return this.getDataValue('DetailedMenu');
    }

    DetailedMenu.prototype.getDate = function () {
        return this.getDataValue('updatedAt');
    }
    
    return DetailedMenu;
};
