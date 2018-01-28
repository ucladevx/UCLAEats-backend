const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const MenuSchema = new Schema ({
    name: String,
    created_at: Date,
    updated_at: Date,
    menu: Object,
});

MenuSchema.methods.Create = function Create(callback) {
    this.save(callback);
};

MenuSchema.methods.FindByName = function FindByName(name, callback) {
    return this.find({name: name}, callback);
};

module.exports.MenuSchema = MenuSchema;
