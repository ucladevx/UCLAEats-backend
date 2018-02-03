const mongoose = require("mongoose");
mongoose.connect("mongodb://localhost:27017/menudb");
const db = mongoose.connection;
const Schema = mongoose.Schema;
mongoose.set('debug', true);

db.on("error", console.error.bind(console, "Connection error:"));
db.once("open", function(callback){
	console.log("Connection Succeeded."); 
    /* Once the database connection has succeeded, the code in db.once is executed. */
});

var AnimalSchema = new Schema({
    name: String, 
    type: String
});
AnimalSchema.methods.Create = function Create (callback) {
    this.save(callback);
};
AnimalSchema.methods.findSimilarType = function findSimilarType (cb) {
    this.model('Animal').find({ type: this.type }, cb);
};

var Animal = mongoose.model('Animal', AnimalSchema);
var dog1 = new Animal({ name: 'Rover', type: 'dog' });
var dog2 = new Animal({ name: 'Tyler', type: 'dog' });

dog1.Create(function(err) {
    if (err) {
        console.error(err);
    }
    dog2.Create( function (err) {
        if (err) {
            console.error(err);
        }
        dog1.findSimilarType(function (err, dogs) {
            if (err) {
                console.error(err);
            }
            dogs.forEach(function(val) {
                console.log(val);     
            });
        });
    });
});

