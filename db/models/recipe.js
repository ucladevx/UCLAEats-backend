'use strict';
module.exports = (sequelize, DataTypes) => {
  var Recipe = sequelize.define('Recipe', {
    recipe_link: DataTypes.STRING,
    nutrition: DataTypes.JSON,
    deletedAt: DataTypes.DATE,
  }, {
    classMethods: {
      associate: function(models) {
        // associations can be defined here
      }
    },
    paranoid: false
  });

  Recipe.findByRecipeLink = function(link) {
    return this.findAll({
        where: { 
            recipe_link : link,
        }
    });
  }

  Recipe.prototype.getID = function () {
    return this.getDataValue('id');
  }

  Recipe.prototype.getNutrition = function () {
    return this.getDataValue('nutrition');
  }

  return Recipe;
};
