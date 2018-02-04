const _ = require('underscore');

module.exports = (Sequelize, db) => {
    const Menu = db.define('menu', {
        // id: {
        //     type: Sequelize.INTEGER,
        //     autoIncrement: true,
        //     primaryKey: true,
        // },

        // name: {
        //     type: Sequelize.STRING,
        //     allowNull: false,
        // },

        // created_at: {
        //     type: Sequelize.DATE,
        //     defaultValue: Sequelize.NOW,
        //     allowNull: false,
        // },

        // updated_at: {
        //     type:Sequelize.DATE,
        //     allowNull: false,
        // },

        menu: {
            type:Sequelize.JSON,
            allowNull: false,
        },
    });

    Menu.findByID = function(id) {
        return this.findOne({where: {id} });
    };
}

