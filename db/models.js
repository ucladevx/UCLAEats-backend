const mongoose = require("mongoose");
const MenuSchemas = require("./Models/MenuSchema");

mongoose.connect("mongodb://localhost:27017/menudb");
const db = mongoose.connection;

db.on("error", console.error.bind(console, "Connection error:"));
db.once("open", function(callback){
	console.log("Connection Succeeded."); 
    /* Once the database connection has succeeded, the code in db.once is executed. */
});

const Menu = mongoose.model("Menu", MenuSchemas.MenuSchema, "menus");

module.exports.Menu = Menu;
