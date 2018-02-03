const Models = require("./models");

let Menu = Models.Menu;

json_obj = {
    test1: "value1",
    test2: "value2"
};
let new_menu = new Menu({
    name: "Awesome_Menu",
    created_at: Date.now(),
    updated_at: Date.now(),
    menu: json_obj,
});

new_menu.Create(function(err) {
    if (err) {
        console.error(err);
    }
    new_menu.Create( function(err) {
        if (err) {
            console.error(err);
        }
        new_menu.FindByName("Awesome_Menu", function(err, menus) {
            if (err) {
                console.error(err);
            }
            menus.forEach(function(menu) {
                console.log(menu);
            });
        });
    });
});
