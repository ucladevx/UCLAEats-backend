'use strict';
module.exports = (sequelize, DataTypes) => {
  var Hours = sequelize.define('Hours', {
    hours: DataTypes.JSON,
    deletedAt: DataTypes.DATE,
    hourDate: DataTypes.DATEONLY,
  }, {
    classMethods: {
      associate: function(models) {
        // associations can be defined here
      }
    },
      paranoid:true,
  });

    
    // find a hour by id
   Hours.findByID = function (id) {
        return this.findOne({ where :{ id } });
    }

    // date is a string with format YYYY-MM-DD
    // Hours has no dateID other than deleted date
    Hours.findAllByDate = function(date) {
        return this.findAll({
            where: {
                hourDate: date,
            }
        });
    }

    // find all Hours Within a date range
    Hours.findByAllDateRange = function(startDate, endDate) {
        return this.findAll({
            where: {
                hourDate: {
                    $between: [startDate, endDate],
                }
            }
        });
    }

    Hours.Delete = function (id) {
        return this.destroy({
            where:{
                id: id,
            },
        });
    }

    Hours.prototype.getID = function () {
        return this.getDataValue('id');
    }

    Hours.prototype.getHours = function () {
        return this.getDataValue('hours');
    }

    Hours.prototype.getDate = function () {
        return this.getDataValue('updatedAt');
    }


    Hours.findLast = function() {
	    return this.findAll({
	        limit: 1,
    	    order: [[ 'createdAt', 'DESC' ]]
	    });
    }
    
  return Hours;
};
