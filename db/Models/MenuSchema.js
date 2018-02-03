const mongoose = require('mongoose');
mongoose.set('debug', true);

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

MenuSchema.methods.FindByName = function FindByName(menu_name, callback) {
    this.model('Menu').find({name: menu_name}, callback);
};
module.exports.MenuSchema = MenuSchema;
