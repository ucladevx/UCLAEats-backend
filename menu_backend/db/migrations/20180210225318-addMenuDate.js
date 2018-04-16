'use strict';

module.exports = {
  up: (queryInterface, Sequelize) => {
    /*
      Add altering commands here.
      Return a promise to correctly handle asynchronicity.

      Example:
      return queryInterface.createTable('users', { id: Sequelize.INTEGER });
    */
      queryInterface.addColumn('OverviewMenus', 'menuDate', Sequelize.DATEONLY);
      queryInterface.addColumn('DetailedMenus', 'menuDate', Sequelize.DATEONLY);
  },

  down: (queryInterface, Sequelize) => {
    /*
      Add reverting commands here.
      Return a promise to correctly handle asynchronicity.

      Example:
      return queryInterface.dropTable('users');
    */
      queryInterface.removeColumn('OverviewMenus', 'menuDate');
      queryInterface.removeColumn('DetailedMenus', 'menuDate');
  }
};
