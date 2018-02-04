'use strict';
module.exports = (Sequelize, DataTypes) => {
    const Menu = Sequelize.define('Menu', {
        menu: DataTypes.JSON
    }, {
        classMethods: {
            associate: function(models) {
            // associations can be defined here
            }
        }
    });

    Menu.findByID = function (id) {
        return this.findOne({ where :{ id } });
    }

    Menu.prototype.getMenu = function () {
        return this.getDataValue('menu');
    }

    return Menu;
};
