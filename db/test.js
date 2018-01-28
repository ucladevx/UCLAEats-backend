const mongoose = require("mongoose");
mongoose.connect("mongodb://localhost:27017/menudb");
const db = mongoose.connection;
const Schema = mongoose.Schema;

db.on("error", console.error.bind(console, "Connection error:"));
db.once("open", function(callback){
	console.log("Connection Succeeded."); 
    /* Once the database connection has succeeded, the code in db.once is executed. */
});

var AnimalSchema = new Schema({
    name: String
  , type: String
});

// we want to use this on an instance of Animal
AnimalSchema.methods.findSimilarType = function findSimilarType (cb) {
  return this.find({ type: this.type }, cb);
};

var Animal = mongoose.model('Animal', AnimalSchema);
var dog = new Animal({ name: 'Rover', type: 'dog' });

// dog is an instance of Animal
dog.findSimilarType(function (err, dogs) {
  if (err) {
      console.error(error);
  }
  dogs.forEach(function(value) {
        console.log(value);
  });
})
