'use strict';
module.exports = (sequelize, DataTypes) => {
    var DetailedMenu = sequelize.define('DetailedMenu', {
        detailedMenu: DataTypes.JSON,
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

    // find a DetailedMenu by id
    DetailedMenu.findByID = function (id) {
        return this.findOne({ where :{ id } });
    }

    // date is a string with format YYYY-MM-DD
    DetailedMenu.findAllByDate = function(date) {
        return this.findAll({
            where: {
                menuDate: date
            }
        });
    }

    // find all DetailedMenus Within a date range
    DetailedMenu.findByAllDateRange = function(startDate, endDate) {
        return this.findAll({
            where: {
                menuDate: {
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
        return this.getDataValue('detailedMenu');
    }

    DetailedMenu.prototype.getDate = function () {
        return this.getDataValue('updatedAt');
    }
    
    return DetailedMenu;
};
