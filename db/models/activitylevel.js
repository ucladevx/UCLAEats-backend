'use strict';
module.exports = (sequelize, DataTypes) => {
  var ActivityLevel = sequelize.define('ActivityLevel', {
    level: DataTypes.JSON
  }, {
    classMethods: {
      associate: function(models) {
        // associations can be defined here
      }
    },
    paranoid: true
  });

  ActivityLevel.prototype.getActivityLevel = function () {
    return this.getDataValue('level');
  }  
  
  // find the newly entered activity level
  ActivityLevel.findLast = function() {
      return this.findAll({
          limit: 1,
          order: [[ 'createdAt', 'DESC' ]]
      });
  }

  return ActivityLevel;
};